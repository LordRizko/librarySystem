from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import os
from models import Base, User, Book, Borrow, Reservation
import hashlib
import datetime
from datetime import timedelta, datetime
import random

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Database connection string (SQLite for simplicity)
DATABASE_URL = "sqlite:///data/library.db"

# Create engine
engine = create_engine(DATABASE_URL)

# Create session factory
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

def init_db():
    """Initialize the database and create tables"""
    Base.metadata.create_all(engine)
    
    # Check if admin user exists, if not create one
    db_session = Session()
    admin = db_session.query(User).filter(User.is_admin == True).first()
    
    if not admin:
        # Create admin user
        hashed_password = hashlib.sha256("admin123".encode()).hexdigest()
        admin_user = User(
            username="admin",
            email="admin@library.com",
            password=hashed_password,
            full_name="System Administrator",
            is_admin=True
        )
        db_session.add(admin_user)
        db_session.commit()
    
    db_session.close()

def get_session():
    """Get a database session"""
    return Session()

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    """Authenticate a user"""
    db_session = Session()
    hashed_password = hash_password(password)
    user = db_session.query(User).filter(
        User.username == username,
        User.password == hashed_password
    ).first()
    db_session.close()
    return user

def add_sample_data():
    """Add extensive sample data to the database"""
    db_session = Session()
    
    # Check if there are already books in the database
    book_count = db_session.query(Book).count()
    
    if book_count <= 4:  # Only add more books if we have the initial set
        print("Adding sample books...")
        
        # Fiction books
        fiction_books = [
            Book(
                title="Pride and Prejudice",
                author="Jane Austen",
                isbn="9780141439518",
                publication_year=1813,
                publisher="Penguin Classics",
                genre="Fiction",
                description="A romantic novel of manners that follows the character development of Elizabeth Bennet.",
                total_copies=3,
                available_copies=3
            ),
            Book(
                title="The Catcher in the Rye",
                author="J.D. Salinger",
                isbn="9780316769488",
                publication_year=1951,
                publisher="Little, Brown and Company",
                genre="Fiction",
                description="A novel about a teenager's experiences in New York.",
                total_copies=4,
                available_copies=4
            ),
            Book(
                title="One Hundred Years of Solitude",
                author="Gabriel García Márquez",
                isbn="9780060883287",
                publication_year=1967,
                publisher="Harper & Row",
                genre="Fiction",
                description="A landmark of magical realism and one of the most significant works in world literature.",
                total_copies=2,
                available_copies=2
            ),
            Book(
                title="The Alchemist",
                author="Paulo Coelho",
                isbn="9780062315007",
                publication_year=1988,
                publisher="HarperOne",
                genre="Fiction",
                description="A philosophical novel about a young Andalusian shepherd who dreams of finding treasure in Egypt.",
                total_copies=5,
                available_copies=5
            ),
            Book(
                title="Brave New World",
                author="Aldous Huxley",
                isbn="9780060850524",
                publication_year=1932,
                publisher="Harper Perennial",
                genre="Fiction",
                description="A dystopian novel set in a futuristic World State of genetically modified citizens.",
                total_copies=3,
                available_copies=3
            ),
        ]
        
        # Science Fiction & Fantasy
        scifi_fantasy_books = [
            Book(
                title="Dune",
                author="Frank Herbert",
                isbn="9780441172719",
                publication_year=1965,
                publisher="Ace Books",
                genre="Science Fiction",
                description="An epic science fiction novel set in the distant future amidst a feudal interstellar society.",
                total_copies=4,
                available_copies=4
            ),
            Book(
                title="The Hobbit",
                author="J.R.R. Tolkien",
                isbn="9780547928227",
                publication_year=1937,
                publisher="Houghton Mifflin Harcourt",
                genre="Fantasy",
                description="A children's fantasy novel about the adventures of hobbit Bilbo Baggins.",
                total_copies=6,
                available_copies=6
            ),
            Book(
                title="Fahrenheit 451",
                author="Ray Bradbury",
                isbn="9781451673319",
                publication_year=1953,
                publisher="Simon & Schuster",
                genre="Science Fiction",
                description="A dystopian novel about a future American society where books are outlawed.",
                total_copies=3,
                available_copies=3
            ),
            Book(
                title="The Martian",
                author="Andy Weir",
                isbn="9780553418026",
                publication_year=2014,
                publisher="Crown Publishing",
                genre="Science Fiction",
                description="A science fiction novel about an astronaut who becomes stranded alone on Mars.",
                total_copies=5,
                available_copies=5
            ),
            Book(
                title="A Game of Thrones",
                author="George R.R. Martin",
                isbn="9780553593716",
                publication_year=1996,
                publisher="Bantam Spectra",
                genre="Fantasy",
                description="The first novel in A Song of Ice and Fire, a series of fantasy novels.",
                total_copies=4,
                available_copies=4
            ),
        ]
        
        # Non-fiction books
        nonfiction_books = [
            Book(
                title="Sapiens: A Brief History of Humankind",
                author="Yuval Noah Harari",
                isbn="9780062316097",
                publication_year=2014,
                publisher="Harper",
                genre="Non-fiction",
                description="A book that explores the development of Homo sapiens from the Stone Age to the present.",
                total_copies=3,
                available_copies=3
            ),
            Book(
                title="A Brief History of Time",
                author="Stephen Hawking",
                isbn="9780553380163",
                publication_year=1988,
                publisher="Bantam Books",
                genre="Non-fiction",
                description="A book on cosmology intended for general readers with no prior knowledge of physics.",
                total_copies=2,
                available_copies=2
            ),
            Book(
                title="Educated",
                author="Tara Westover",
                isbn="9780399590504",
                publication_year=2018,
                publisher="Random House",
                genre="Non-fiction",
                description="A memoir about a woman who leaves her survivalist family and goes on to earn a PhD.",
                total_copies=4,
                available_copies=4
            ),
            Book(
                title="Thinking, Fast and Slow",
                author="Daniel Kahneman",
                isbn="9780374533557",
                publication_year=2011,
                publisher="Farrar, Straus and Giroux",
                genre="Non-fiction",
                description="A book summarizing research on cognitive biases and heuristics.",
                total_copies=3,
                available_copies=3
            ),
            Book(
                title="The Immortal Life of Henrietta Lacks",
                author="Rebecca Skloot",
                isbn="9781400052189",
                publication_year=2010,
                publisher="Crown Publishing Group",
                genre="Non-fiction",
                description="A book about Henrietta Lacks and the immortal cell line from her cancer cells.",
                total_copies=2,
                available_copies=2
            ),
        ]
        
        # Computer Science & Programming books
        cs_books = [
            Book(
                title="Clean Code",
                author="Robert C. Martin",
                isbn="9780132350884",
                publication_year=2008,
                publisher="Prentice Hall",
                genre="Programming",
                description="A handbook of agile software craftsmanship.",
                total_copies=3,
                available_copies=3
            ),
            Book(
                title="Introduction to Algorithms",
                author="Thomas H. Cormen",
                isbn="9780262033848",
                publication_year=2009,
                publisher="MIT Press",
                genre="Programming",
                description="A comprehensive introduction to modern algorithms.",
                total_copies=2,
                available_copies=2
            ),
            Book(
                title="The Pragmatic Programmer",
                author="Andrew Hunt and David Thomas",
                isbn="9780201616224",
                publication_year=1999,
                publisher="Addison-Wesley",
                genre="Programming",
                description="A guide to being a better programmer.",
                total_copies=3,
                available_copies=3
            ),
            Book(
                title="JavaScript: The Good Parts",
                author="Douglas Crockford",
                isbn="9780596517748",
                publication_year=2008,
                publisher="O'Reilly Media",
                genre="Programming",
                description="A book about the good parts of JavaScript, the subset that's robust and reliable.",
                total_copies=4,
                available_copies=4
            ),
            Book(
                title="Artificial Intelligence: A Modern Approach",
                author="Stuart Russell and Peter Norvig",
                isbn="9780136042594",
                publication_year=2009,
                publisher="Pearson",
                genre="Programming",
                description="A comprehensive introduction to the theory and practice of artificial intelligence.",
                total_copies=2,
                available_copies=2
            ),
        ]
        
        # Add all books
        all_sample_books = fiction_books + scifi_fantasy_books + nonfiction_books + cs_books
        db_session.add_all(all_sample_books)
        db_session.commit()
        print(f"Added {len(all_sample_books)} new sample books")
        
    # Add regular users if few exist
    user_count = db_session.query(User).filter(User.is_admin == False).count()
    
    if user_count <= 1:  # Only the default user exists
        print("Adding sample users...")
        
        # Sample users with various demographics
        sample_users = [
            User(
                username="jsmith",
                email="john.smith@example.com",
                password=hash_password("user456"),
                full_name="John Smith",
                address="456 Oak Avenue, Townsville",
                phone="555-7890",
                is_admin=False,
                registration_date=datetime.now() - timedelta(days=60)
            ),
            User(
                username="mjohnson",
                email="mjohnson@example.com",
                password=hash_password("user789"),
                full_name="Maria Johnson",
                address="789 Maple Road, Cityville",
                phone="555-4567",
                is_admin=False,
                registration_date=datetime.now() - timedelta(days=45)
            ),
            User(
                username="alee",
                email="amy.lee@example.com",
                password=hash_password("userlee"),
                full_name="Amy Lee",
                address="101 Pine Street, Villagetown",
                phone="555-8901",
                is_admin=False,
                registration_date=datetime.now() - timedelta(days=30)
            ),
            User(
                username="rwilson",
                email="rwilson@example.com",
                password=hash_password("user321"),
                full_name="Robert Wilson",
                address="321 Cedar Lane, Hamlet",
                phone="555-2345",
                is_admin=False,
                registration_date=datetime.now() - timedelta(days=25)
            ),
            User(
                username="sgarcia",
                email="sofia.garcia@example.com",
                password=hash_password("user654"),
                full_name="Sofia Garcia",
                address="654 Birch Boulevard, County",
                phone="555-6789",
                is_admin=False,
                registration_date=datetime.now() - timedelta(days=15)
            ),
            User(
                username="dkim",
                email="david.kim@example.com",
                password=hash_password("userdkim"),
                full_name="David Kim",
                address="876 Elm Court, District",
                phone="555-3456",
                is_admin=False,
                registration_date=datetime.now() - timedelta(days=10)
            ),
            User(
                username="jtaylor",
                email="jtaylor@example.com",
                password=hash_password("user987"),
                full_name="James Taylor",
                address="543 Spruce Way, Region",
                phone="555-9012",
                is_admin=False,
                registration_date=datetime.now() - timedelta(days=5)
            ),
            User(
                username="librarian",
                email="librarian@example.com",
                password=hash_password("libpass"),
                full_name="Lisa Librarian",
                address="123 Library Lane, Booktown",
                phone="555-1212",
                is_admin=True,  # Another admin user
                registration_date=datetime.now() - timedelta(days=90)
            ),
        ]
        
        db_session.add_all(sample_users)
        db_session.commit()
        print(f"Added {len(sample_users)} new sample users")
    
    # Create sample borrow and reservation records if few exist
    borrow_count = db_session.query(Borrow).count()
    reservation_count = db_session.query(Reservation).count()
    
    if borrow_count < 10:
        print("Adding sample borrowing activity...")
        
        # Get all books and users for creating sample activity
        all_books = db_session.query(Book).all()
        regular_users = db_session.query(User).filter(User.is_admin == False).all()
        
        # Generate some completed borrows (returned)
        past_borrow_records = []
        
        for _ in range(25):  # Create 25 past borrow records
            random_user = random.choice(regular_users)
            random_book = random.choice(all_books)
            
            # Random dates in the past
            days_ago_borrow = random.randint(5, 90)
            borrow_date = datetime.now() - timedelta(days=days_ago_borrow)
            due_date = borrow_date + timedelta(days=14)  # Standard 14-day loan
            
            # Some returned on time, some late
            if random.random() < 0.8:  # 80% returned on time
                days_until_return = random.randint(3, 14)
            else:  # 20% returned late
                days_until_return = random.randint(15, 21)
            
            return_date = borrow_date + timedelta(days=days_until_return)
            
            # Create the borrow record
            past_borrow = Borrow(
                user_id=random_user.id,
                book_id=random_book.id,
                borrow_date=borrow_date,
                due_date=due_date,
                return_date=return_date,
                is_returned=True
            )
            past_borrow_records.append(past_borrow)
        
        db_session.add_all(past_borrow_records)
        db_session.commit()
        print(f"Added {len(past_borrow_records)} past borrowing records")
        
        # Generate some active borrows (not returned)
        active_borrow_records = []
        
        for _ in range(12):  # Create 12 active borrow records
            random_user = random.choice(regular_users)
            random_book = random.choice([b for b in all_books if b.available_copies > 0])
            
            # Random recent dates
            days_ago_borrow = random.randint(1, 13)
            borrow_date = datetime.now() - timedelta(days=days_ago_borrow)
            due_date = borrow_date + timedelta(days=14)  # Standard 14-day loan
            
            # Create the borrow record
            active_borrow = Borrow(
                user_id=random_user.id,
                book_id=random_book.id,
                borrow_date=borrow_date,
                due_date=due_date,
                is_returned=False
            )
            active_borrow_records.append(active_borrow)
            
            # Update available copies
            random_book.available_copies -= 1
        
        db_session.add_all(active_borrow_records)
        db_session.commit()
        print(f"Added {len(active_borrow_records)} active borrowing records")
    
    if reservation_count < 5:
        print("Adding sample reservation activity...")
        
        # Generate some active reservations
        all_books = db_session.query(Book).all()
        regular_users = db_session.query(User).filter(User.is_admin == False).all()
        
        active_reservation_records = []
        
        # Find books with no available copies for realistic reservations
        books_unavailable = [book for book in all_books if book.available_copies == 0]
        
        # If no books are unavailable, make some unavailable
        if not books_unavailable and all_books:
            for _ in range(min(5, len(all_books))):
                book = random.choice([b for b in all_books if b.available_copies > 0])
                book.available_copies = 0
            db_session.commit()
            books_unavailable = [book for book in all_books if book.available_copies == 0]
        
        for _ in range(8):  # Create 8 active reservations
            if not books_unavailable or not regular_users:
                break
            
            random_user = random.choice(regular_users)
            random_book = random.choice(books_unavailable)
            
            # Random recent dates
            days_ago_reserved = random.randint(1, 5)
            reservation_date = datetime.now() - timedelta(days=days_ago_reserved)
            expiry_date = reservation_date + timedelta(days=3)  # Standard 3-day reservation
            
            # Create the reservation record
            active_reservation = Reservation(
                user_id=random_user.id,
                book_id=random_book.id,
                reservation_date=reservation_date,
                expiry_date=expiry_date,
                fulfilled=False,
                cancelled=False
            )
            active_reservation_records.append(active_reservation)
        
        db_session.add_all(active_reservation_records)
        db_session.commit()
        print(f"Added {len(active_reservation_records)} active reservation records")
        
        # Generate some fulfilled/cancelled reservations
        past_reservation_records = []
        
        for _ in range(15):  # Create 15 past reservation records
            random_user = random.choice(regular_users)
            random_book = random.choice(all_books)
            
            # Random dates in the past
            days_ago_reserved = random.randint(10, 60)
            reservation_date = datetime.now() - timedelta(days=days_ago_reserved)
            expiry_date = reservation_date + timedelta(days=3)
            
            # 70% fulfilled, 30% cancelled
            is_fulfilled = random.random() < 0.7
            is_cancelled = not is_fulfilled
            
            # Create the reservation record
            past_reservation = Reservation(
                user_id=random_user.id,
                book_id=random_book.id,
                reservation_date=reservation_date,
                expiry_date=expiry_date,
                fulfilled=is_fulfilled,
                cancelled=is_cancelled
            )
            past_reservation_records.append(past_reservation)
        
        db_session.add_all(past_reservation_records)
        db_session.commit()
        print(f"Added {len(past_reservation_records)} past reservation records")
    
    db_session.close()