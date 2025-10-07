import requests
import json
from typing import List, Dict, Optional
from config.llm_config import llm_config

class YouTubeRecommender:
    """Service for recommending educational YouTube videos"""
    
    def __init__(self):
        self.api_key = llm_config.google_api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
    
    def search_educational_videos(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search for educational videos on YouTube
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of video dictionaries
        """
        try:
            # Search for videos
            search_url = f"{self.base_url}/search"
            params = {
                'q': query + " education tutorial",
                'key': self.api_key,
                'part': 'snippet',
                'maxResults': max_results,
                'type': 'video',
                'order': 'relevance'
            }
            
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            
            search_results = response.json()
            
            # Get video details
            videos = []
            video_ids = [item['id']['videoId'] for item in search_results.get('items', [])]
            
            if video_ids:
                videos = self._get_video_details(video_ids)
            
            return videos
            
        except Exception as e:
            print(f"Error searching YouTube videos: {e}")
            return []
    
    def _get_video_details(self, video_ids: List[str]) -> List[Dict]:
        """Get detailed information for videos"""
        try:
            details_url = f"{self.base_url}/videos"
            params = {
                'key': self.api_key,
                'part': 'snippet,statistics,contentDetails',
                'id': ','.join(video_ids)
            }
            
            response = requests.get(details_url, params=params)
            response.raise_for_status()
            
            video_items = response.json().get('items', [])
            
            videos = []
            for item in video_items:
                video_info = {
                    'title': item['snippet']['title'],
                    'video_id': item['id'],
                    'channel': item['snippet']['channelTitle'],
                    'description': item['snippet']['description'],
                    'thumbnail': item['snippet']['thumbnails']['high']['url'] if 'high' in item['snippet']['thumbnails'] else '',
                    'duration': item['contentDetails']['duration'],
                    'view_count': item['statistics'].get('viewCount', 0),
                    'url': f"https://www.youtube.com/watch?v={item['id']}"
                }
                videos.append(video_info)
            
            return videos
            
        except Exception as e:
            print(f"Error getting video details: {e}")
            return []
    
    def recommend_videos_for_topic(self, topic: str, content_summary: str = "", max_results: int = 5) -> List[Dict]:
        """
        Recommend videos based on topic and content
        
        Args:
            topic: Educational topic
            content_summary: Summary of content for context
            max_results: Maximum number of recommendations
            
        Returns:
            List of recommended video dictionaries
        """
        try:
            # Use LLM to generate search queries
            search_queries = self._generate_search_queries(topic, content_summary)
            
            all_videos = []
            for query in search_queries:
                videos = self.search_educational_videos(query, max_results=2)
                all_videos.extend(videos)
            
            # Remove duplicates and rank videos
            unique_videos = self._remove_duplicate_videos(all_videos)
            
            # Rank videos based on relevance
            ranked_videos = self._rank_videos_by_relevance(unique_videos, topic)
            
            return ranked_videos[:max_results]
            
        except Exception as e:
            print(f"Error recommending videos: {e}")
            return []
    
    def _generate_search_queries(self, topic: str, content_summary: str) -> List[str]:
        """Generate search queries using LLM"""
        try:
            prompt = llm_config.youtube_recommendation_prompt.format(
                topic=topic,
                content=content_summary
            )
            
            # For now, use simple query generation
            # In production, you'd use the LLM to generate better queries
            queries = [
                f"{topic} tutorial",
                f"{topic} explained",
                f"{topic} concepts",
                f"{topic} examples"
            ]
            
            return queries[:3]  # Return first 3 queries
            
        except Exception as e:
            print(f"Error generating search queries: {e}")
            return [f"{topic} tutorial"]
    
    def _remove_duplicate_videos(self, videos: List[Dict]) -> List[Dict]:
        """Remove duplicate videos based on title similarity"""
        unique_videos = []
        seen_titles = set()
        
        for video in videos:
            title_lower = video['title'].lower()
            if title_lower not in seen_titles:
                seen_titles.add(title_lower)
                unique_videos.append(video)
        
        return unique_videos
    
    def _rank_videos_by_relevance(self, videos: List[Dict], topic: str) -> List[Dict]:
        """Rank videos by relevance to the topic"""
        topic_lower = topic.lower()
        
        scored_videos = []
        for video in videos:
            score = 0
            
            # Score based on title relevance
            title_lower = video['title'].lower()
            if topic_lower in title_lower:
                score += 3
            
            # Score based on description relevance
            if 'description' in video:
                desc_lower = video['description'].lower()
                if topic_lower in desc_lower:
                    score += 2
            
            # Score based on view count (popularity)
            view_count = video.get('view_count', 0)
            if view_count > 100000:  # 100K+ views
                score += 1
            elif view_count > 10000:  # 10K+ views
                score += 0.5
            
            # Score based on duration (prefer longer educational videos)
            duration = video.get('duration', '')
            if 'PT10M' in duration or duration == 'P0D':  # 10+ minutes or unknown
                score += 1
            
            video['relevance_score'] = score
            scored_videos.append(video)
        
        # Sort by relevance score
        scored_videos.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return scored_videos
    
    def get_video_embed_html(self, video_url: str, width: int = 560, height: int = 315) -> str:
        """
        Get embed HTML for a video
        
        Args:
            video_url: YouTube video URL
            width: Embed width
            height: Embed height
            
        Returns:
            HTML embed code
        """
        try:
            # Extract video ID from URL
            video_id = self._extract_video_id(video_url)
            
            if video_id:
                return f"""
                <iframe 
                    width="{width}" 
                    height="{height}" 
                    src="https://www.youtube.com/embed/{video_id}" 
                    frameborder="0" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                    allowfullscreen>
                </iframe>
                """
            
            return ""
            
        except Exception as e:
            print(f"Error generating embed HTML: {e}")
            return ""
    
    def _extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL"""
        try:
            # Handle different URL formats
            if 'youtube.com/watch?v=' in url:
                return url.split('v=')[1].split('&')[0]
            elif 'youtu.be/' in url:
                return url.split('youtu.be/')[1].split('?')[0]
            elif 'youtube.com/embed/' in url:
                return url.split('embed/')[1].split('?')[0]
            
            return None
            
        except Exception:
            return None

# Global YouTube recommender instance
youtube_recommender = YouTubeRecommender()