
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import os
import uuid
from pathlib import Path
from typing import List
from config.database import get_db
from models.pdf_model import PDF, User, TextChunk
from schemas.pdf_schema import PDF as PDFSchema, PDFCreate
from utils.pdf_processor import PDFProcessor
from utils.embeddings import embedding_service

router = APIRouter()

@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Uploads a PDF file, processes it, and saves metadata to PostgreSQL.
    """
    try:
        # Validate file type
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Create upload directory if it doesn't exist
        # upload_dir = Path("uploads/pdfs")
        # upload_dir.mkdir(parents=True, exist_ok=True)
        
        # # Generate unique filename to avoid conflicts
        # file_extension = file.filename.split('.')[-1]
        # unique_filename = f"{uuid.uuid4()}.{file_extension}"
        # file_path = upload_dir / unique_filename
        
        # Always use absolute paths to avoid working directory issues
        BASE_DIR = Path(__file__).resolve().parent.parent  # Go up to backend root
        UPLOAD_DIR = BASE_DIR / "uploads" / "pdfs"
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

        # Use forward slashes for cross-platform safety
        file_extension = file.filename.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = UPLOAD_DIR / unique_filename

        
        # Save file to disk
        with open(str(file_path), "wb") as buffer:
            buffer.write(await file.read())
        
        # Get current user (simplified - in production, use proper auth)
        user_id = 1  # For demo purposes
        
        # Create PDF record in database
        pdf_data = PDFCreate(
            filename=file.filename,
            filepath=str(file_path),
            user_id=user_id
        )
        
        db_pdf = PDF(**pdf_data.dict())
        db.add(db_pdf)
        db.commit()
        db.refresh(db_pdf)
        
        # Initialize pdf_info
        pdf_info = {'page_count': 0, 'file_size': 0}
        
        # Process PDF (extract text, create chunks, generate embeddings)
        try:
            # pdf_processor = PDFProcessor()
            # chunks, pdf_info = pdf_processor.process_pdf(str(file_path), db_pdf.id)
            pdf_processor = PDFProcessor()
            chunks, pdf_info = pdf_processor.process_pdf(str(file_path), db_pdf.id)

            
            # Save text chunks to database
            for chunk in chunks:
                db_chunk = TextChunk(**chunk.dict())
                db.add(db_chunk)
            
            # Generate embeddings
            embedding_ids = embedding_service.create_embeddings_for_chunks([
                {'chunk_text': chunk.chunk_text, 'page_number': chunk.page_number, 'chunk_order': chunk.chunk_order}
                for chunk in chunks
            ])
            
            # Store embeddings in ChromaDB
            embedding_service.store_embeddings([
                {'chunk_text': chunk.chunk_text, 'page_number': chunk.page_number, 'chunk_order': chunk.chunk_order}
                for chunk in chunks
            ], embedding_ids, db_pdf.id)
            
            # Update PDF record as processed
            db_pdf.processed = True
            db_pdf.page_count = pdf_info['page_count']
            db_pdf.file_size = pdf_info['file_size']
            db.commit()
            
            return {
                "success": True,
                "data": {
                    "pdf_id": db_pdf.id,
                    "filename": file.filename,
                    "file_path": str(file_path),
                    "processed": db_pdf.processed,
                    "page_count": pdf_info.get('page_count'),
                    "file_size": pdf_info.get('file_size')
                }
            }
            
        except Exception as processing_error:
            # If processing fails, still return success but log the error
            print(f"PDF processing error: {processing_error}")
            # Continue with the upload, just mark as not processed
            return {
                "success": True,
                "data": {
                    "pdf_id": db_pdf.id,
                    "filename": file.filename,
                    "file_path": str(file_path),
                    "processed": False,
                    "page_count": 0,
                    "file_size": 0
                }
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_pdfs(db: Session = Depends(get_db)):
    """
    Retrieves a list of all uploaded PDFs.
    """
    try:
        # Get all PDFs from database
        pdfs = db.query(PDF).all()
        
        # Convert to schema format
        pdf_schemas = []
        for pdf in pdfs:
            pdf_schemas.append({
                "id": pdf.id,
                "filename": pdf.filename,
                "uploaded_at": pdf.uploaded_at,
                "processed": pdf.processed,
                "page_count": pdf.page_count,
                "file_size": pdf.file_size
            })
        
        return {
            "success": True,
            "data": {
                "pdfs": pdf_schemas,
                "total_count": len(pdf_schemas)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{pdf_id}")
async def get_pdf(pdf_id: int, db: Session = Depends(get_db)):
    """
    Retrieves details of a specific PDF.
    """
    try:
        pdf = db.query(PDF).filter(PDF.id == pdf_id).first()
        
        if not pdf:
            raise HTTPException(status_code=404, detail="PDF not found")
        
        return {
            "success": True,
            "data": {
                "id": pdf.id,
                "filename": pdf.filename,
                "uploaded_at": pdf.uploaded_at,
                "processed": pdf.processed,
                "page_count": pdf.page_count,
                "file_size": pdf.file_size,
                "user_id": pdf.user_id
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{pdf_id}")
async def delete_pdf(pdf_id: int, db: Session = Depends(get_db)):
    """
    Deletes a PDF and all associated data.
    """
    try:
        # Get PDF from database
        pdf = db.query(PDF).filter(PDF.id == pdf_id).first()
        
        if not pdf:
            raise HTTPException(status_code=404, detail="PDF not found")
        
        # Delete embeddings from ChromaDB
        try:
            embedding_service.delete_pdf_embeddings(pdf_id)
        except Exception as e:
            print(f"Warning: Could not delete embeddings: {e}")
        
        # Delete text chunks from database
        db.query(TextChunk).filter(TextChunk.pdf_id == pdf_id).delete()
        
        # Delete file from disk
        try:
            if os.path.exists(str(pdf.filepath)):
                os.remove(str(pdf.filepath))
        except Exception as e:
            print(f"Warning: Could not delete file: {e}")
        
        # Delete PDF record from database
        db.delete(pdf)
        db.commit()
        
        return {
            "success": True,
            "message": "PDF deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{pdf_id}/chunks")
async def get_pdf_chunks(pdf_id: int, db: Session = Depends(get_db)):
    """
    Retrieves text chunks for a specific PDF.
    """
    try:
        # Validate PDF exists
        pdf = db.query(PDF).filter(PDF.id == pdf_id).first()
        if not pdf:
            raise HTTPException(status_code=404, detail="PDF not found")
        
        # Get text chunks
        chunks = db.query(TextChunk).filter(TextChunk.pdf_id == pdf_id).order_by(TextChunk.chunk_order).all()
        
        # Convert to schema format
        chunk_schemas = []
        for chunk in chunks:
            chunk_schemas.append({
                "id": chunk.id,
                "chunk_text": chunk.chunk_text,
                "page_number": chunk.page_number,
                "chunk_order": chunk.chunk_order,
                "embedding_id": chunk.embedding_id
            })
        
        return {
            "success": True,
            "data": {
                "pdf_id": pdf_id,
                "chunks": chunk_schemas,
                "total_chunks": len(chunk_schemas)
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
