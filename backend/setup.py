import os
import sys
import subprocess
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Add the parent directory to the Python path to enable absolute imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables from .env file
load_dotenv()

def install_dependencies():
    """Install required Python packages"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False
    return True

def setup_database():
    """Set up PostgreSQL database"""
    print("Setting up database...")
    
    # Get database configuration from environment
    db_url = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/pdf_db")
    print(f"Using DATABASE_URL: {db_url}")
    
    try:
        # Parse database URL
        import urllib.parse as urlparse
        result = urlparse.urlparse(db_url)
        db_name = result.path[1:]  # Remove leading slash
        
        # Connect to PostgreSQL server (without database)
        conn = psycopg2.connect(
            host=result.hostname,
            user=result.username,
            password=result.password,
            port=result.port or 5432
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = {}").format(sql.Literal(db_name)))
        if not cursor.fetchone():
            print(f"Creating database: {db_name}")
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            print(f"Database '{db_name}' created successfully")
        else:
            print(f"Database '{db_name}' already exists")
        
        cursor.close()
        conn.close()
        
        # Now connect to the specific database and create tables
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        # Import and create tables
        from backend.models.pdf_model import create_tables
        create_tables()
        print("Database tables created successfully")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Error setting up database: {e}")
        return False

def setup_directories():
    """Create necessary directories"""
    print("Setting up directories...")
    
    directories = [
        "uploads/pdfs",
        "chroma",
        "logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    return True

def setup_chroma():
    """Initialize ChromaDB"""
    print("Setting up ChromaDB...")
    try:
        from backend.utils.embeddings import embedding_service
        # This will initialize ChromaDB and create the persist directory
        stats = embedding_service.get_collection_stats()
        print("ChromaDB initialized successfully")
        return True
    except Exception as e:
        print(f"Error setting up ChromaDB: {e}")
        return False

def main():
    """Main setup function"""
    print("Setting up RAG Learning Assistant Backend...")
    print("=" * 50)
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        print(".env file not found. Please create it with your configuration.")
        print("   Copy .env.example to .env and fill in your API keys and database credentials.")
        return False
    
    # Run setup steps
    steps = [
        # ("Install dependencies", install_dependencies),
        ("Setup directories", setup_directories),
        ("Setup database", setup_database),
        ("Setup ChromaDB", setup_chroma)
    ]
    
    success = True
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        if not step_func():
            success = False
            break
    
    print("\n" + "=" * 50)
    if success:
        print("Setup completed successfully!")
        print("\nNext steps:")
        print("1. Update your .env file with API keys")
        print("2. Start the server: python -m uvicorn main:app --reload")
        print("3. Access the API at: http://localhost:8000")
        print("4. View API documentation at: http://localhost:8000/docs")
    else:
        print("Setup failed. Please check the error messages above.")
    
    return success

if __name__ == "__main__":
    main()