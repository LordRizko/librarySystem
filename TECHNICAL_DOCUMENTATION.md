# Library Management System - Technical Documentation

This document provides detailed technical information about the implementation of the Library Management System. It is intended for developers who need to understand the system architecture, database schema, and code organization.

## System Architecture

The Library Management System follows a layered architecture:

1. **Presentation Layer**: Implemented using Streamlit components in `app.py`, `user_pages.py`, and `admin_pages.py`
2. **Business Logic Layer**: Core functionality implemented in page modules and utility functions
3. **Data Access Layer**: Implemented using SQLAlchemy ORM in `db.py` and `models.py`
4. **Database Layer**: SQLite database stored in `data/library.db`

## Database Schema

### Entity Relationship Diagram (Conceptual)

```
User (1) --- (*) Borrow (*) --- (1) Book
 |                                 |
 |                                 |
 v                                 v
(*) Reservation (*) -------------- +
```

### Tables

#### User Table
- `id`: Integer, Primary Key
- `username`: String(50), Unique, Not Null
- `email`: String(100), Unique, Not Null
- `password`: String(100), Not Null (SHA-256 hashed)
- `full_name`: String(100), Not Null
- `address`: String(200), Nullable
- `phone`: String(20), Nullable
- `is_admin`: Boolean, Default False
- `registration_date`: DateTime, Default Now

#### Book Table
- `id`: Integer, Primary Key
- `title`: String(200), Not Null
- `author`: String(100), Not Null
- `isbn`: String(20), Unique
- `publication_year`: Integer
- `publisher`: String(100)
- `genre`: String(50)
- `description`: Text
- `available_copies`: Integer, Default 1
- `total_copies`: Integer, Default 1

#### Borrow Table
- `id`: Integer, Primary Key
- `user_id`: Integer, Foreign Key (users.id), Not Null
- `book_id`: Integer, Foreign Key (books.id), Not Null
- `borrow_date`: DateTime, Default Now
- `due_date`: DateTime, Default (Now + 14 days)
- `return_date`: DateTime, Nullable
- `is_returned`: Boolean, Default False
- `extended_times`: Integer, Default 0

#### Reservation Table
- `id`: Integer, Primary Key
- `user_id`: Integer, Foreign Key (users.id), Not Null
- `book_id`: Integer, Foreign Key (books.id), Not Null
- `reservation_date`: DateTime, Default Now
- `expiry_date`: DateTime, Default (Now + 3 days)
- `fulfilled`: Boolean, Default False
- `cancelled`: Boolean, Default False

## File Structure and Functionality

### 1. `app.py`

Main entry point for the application that:
- Configures the Streamlit page
- Initializes the database
- Manages authentication (login/logout/register)
- Controls navigation between user and admin interfaces
- Renders the appropriate page based on user role

### 2. `models.py`

Contains SQLAlchemy ORM models:
- `User`: Represents library users and administrators
- `Book`: Represents books in the library collection
- `Borrow`: Represents book borrowing transactions
- `Reservation`: Represents book reservations

### 3. `db.py`

Handles database operations:
- Database initialization
- Session management
- Authentication utilities
- Sample data generation

### 4. `user_pages.py`

Implements functionality for regular users:
- User profile management
- Book catalog browsing
- Book borrowing
- Book reservation
- Book return
- Borrowing history

### 5. `admin_pages.py`

Implements administrative functionality:
- Dashboard with library statistics
- Book management (CRUD operations)
- User management
- Loan management
- Reservation management

## Key Functions and Workflows

### Authentication Flow

1. User enters credentials on login page (`app.py`)
2. Credentials are hashed and checked against database (`db.py`)
3. Session state variables are updated based on authentication result
4. User is directed to appropriate interface based on their role

### Book Borrowing Workflow

1. User browses book catalog (`user_pages.py` > `show_book_catalog()`)
2. User clicks "Borrow" button on an available book
3. System checks user's eligibility to borrow
4. System creates a new Borrow record with appropriate dates
5. Book's available_copies count is decremented
6. User is redirected to "My Books" page

### Book Reservation Workflow

1. User attempts to borrow an unavailable book
2. System offers reservation option
3. System creates a new Reservation record with expiry date
4. When a copy becomes available, admin can fulfill reservation

### Admin Dashboard Analytics

The admin dashboard (`admin_pages.py` > `show_admin_dashboard()`) displays:
- Total books in the collection
- Registered users count
- Active loans count
- Active reservations count
- Books with no available copies
- Recent borrowing activity
- Genre distribution visualization
- Monthly borrowing trends

## Utility Functions

### Database Utilities

- `init_db()`: Initializes database and creates admin user if needed
- `get_session()`: Returns a SQLAlchemy session
- `hash_password()`: Hashes password using SHA-256
- `authenticate_user()`: Validates user credentials
- `add_sample_data()`: Populates database with sample data

### Book Management Utilities

- `check_book_availability()`: Checks if a book is available for borrowing
- `process_book_return()`: Handles book return workflow
- `extend_book_loan()`: Extends due date for borrowed books
- `check_and_fulfill_reservations()`: Processes reservations when books are returned

## Security Considerations

1. Passwords are hashed using SHA-256 before storage
2. Session state maintains authentication status
3. Admin functions are protected by role-based access control
4. Input validation is performed before database operations

## Limitations and Known Issues

1. No email notification system for overdue books
2. Limited search functionality (basic text search only)
3. No integration with external library systems
4. Limited reporting capabilities
5. No backup and restore functionality

## Performance Considerations

1. SQLite database is used for simplicity but might need to be replaced for production use
2. Large result sets could cause performance issues in the UI
3. No pagination implemented for large catalogs
4. Database indexes should be added for production use

## Deployment Notes

1. The system uses a file-based SQLite database appropriate for development
2. For production, consider switching to PostgreSQL or MySQL
3. Streamlit's default server is not intended for production use; consider deployment options:
   - Streamlit Sharing
   - Docker container with proper web server
   - Cloud platform (AWS, Azure, GCP)

---

This documentation is intended for developers working on the Library Management System. For user documentation, please refer to the README.md file.
