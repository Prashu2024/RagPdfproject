"""
Database initialization script
Creates tables and seeds initial test data
"""
from config.database import Base, engine, SessionLocal
from models.pdf_model import User, PDF, QuizAttempt, UserProgress, TextChunk

def init_database():
    """Initialize database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully!")

def seed_test_user():
    """Create a test user for development"""
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.username == "testuser").first()
        
        if existing_user:
            print(f"✓ Test user already exists (ID: {existing_user.id})")
            return existing_user
        
        # Create test user
        test_user = User(
            username="testuser",
            email="test@example.com"
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print(f"✓ Test user created successfully (ID: {test_user.id})")
        return test_user
        
    except Exception as e:
        print(f"✗ Error creating test user: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def main():
    """Main initialization function"""
    print("\n" + "="*50)
    print("DATABASE INITIALIZATION")
    print("="*50 + "\n")
    
    # Initialize database
    init_database()
    
    # Seed test user
    print("\nSeeding test data...")
    seed_test_user()
    
    print("\n" + "="*50)
    print("INITIALIZATION COMPLETE!")
    print("="*50 + "\n")
    
    print("You can now run the server with:")
    print("  uvicorn main:app --reload")
    print("\nTest user credentials:")
    print("  Username: testuser")
    print("  Email: test@example.com")
    print("  User ID: 1")
    print()

if __name__ == "__main__":
    main()

