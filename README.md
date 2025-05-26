# Library Management System

A comprehensive library management system built with Python, Streamlit, and SQLAlchemy. This application provides an intuitive interface for both library patrons and administrators to manage books, borrowings, reservations, and user accounts.

Developed as part of CSC426-Software Engineering coursework | City University

![Library Management System](https://img.shields.io/badge/Library-Management_System-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-CC2927?style=flat&logo=sqlalchemy&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)

## 📚 Features

### For Users
- **Account Management**: Register, login, and update personal information
- **Book Catalog**: Browse and search the library collection by title, author, or genre
- **Borrowing System**: Borrow available books with automatic due date assignment
- **Reservation System**: Reserve books that are currently unavailable
- **Personal Dashboard**: View borrowed books, reservation status, and history

### For Administrators
- **Administrative Dashboard**: View key metrics and library statistics
- **Book Management**: Add, edit, and remove books from the library catalog
- **User Management**: View and manage user accounts
- **Loan Management**: Track borrowed books, process returns, and handle overdue items
- **Reservation Management**: Process and manage book reservations

## 🛠️ Installation

1. **Clone the repository**

```bash
git clone https://github.com/LordRizko/librarySystem.git
cd librarySystem
```

2. **Create a virtual environment (optional but recommended)**

```bash
python -m venv venv
```

3. **Activate the virtual environment**

On Windows:
```bash
venv\Scripts\activate
```

On macOS/Linux:
```bash
source venv/bin/activate
```

4. **Install required packages**

```bash
pip install -r requirements.txt
```

5. **Run the application**

```bash
streamlit run app.py
```

## 🖥️ Usage

### Login Credentials

The system comes with sample users for testing:

- **Administrator Account**:
  - Username: `admin`
  - Password: `admin123`

- **Sample User Account**:
  - Username: `user`
  - Password: `user123`

### User Guide

1. **Login or Register**:
   - Use existing credentials or create a new account

2. **Browse Books**:
   - View the complete catalog
   - Search for specific books
   - View book details

3. **Borrow Books**:
   - Click "Borrow" on any available book
   - Books will automatically be assigned a two-week due date

4. **Reserve Books**:
   - If a book is unavailable, you can reserve it
   - You'll be notified when the book becomes available

5. **Return Books**:
   - Go to "My Books" section
   - Click "Return" next to the book you want to return

6. **Manage Profile**:
   - Update your personal information
   - View your borrowing history and current books

### Admin Guide

1. **Dashboard**:
   - View library statistics and metrics
   - Monitor unavailable books
   - Track recent activity

2. **Book Management**:
   - Add new books to the catalog
   - Edit book information
   - Remove books from circulation

3. **User Management**:
   - View registered users
   - Edit user information
   - Manage user permissions

4. **Loan Management**:
   - Process book returns
   - Track overdue books
   - Extend loan periods

5. **Reservation Management**:
   - View active reservations
   - Fulfill reservations when books become available
   - Cancel reservations if needed

## 📂 Project Structure

```
librarySystem/
├── app.py                # Main application entry point
├── models.py             # Database models (SQLAlchemy)
├── db.py                 # Database connection and utilities
├── user_pages.py         # UI components for regular users
├── admin_pages.py        # UI components for administrators
├── requirements.txt      # Dependencies
├── README.md             # Documentation
├── data/                 # Database and data files
│   └── library.db        # SQLite database file
└── assets/               # Static files (if any)
```

## 🗄️ Database Schema

The system uses the following main entities:

1. **User**:
   - Basic user information
   - Authentication details
   - Admin status

2. **Book**:
   - Bibliographic details
   - Availability status
   - Collection metadata

3. **Borrow**:
   - Borrowing records
   - Due dates
   - Return status

4. **Reservation**:
   - Book reservation details
   - Reservation status
   - Expiration dates

## 🧩 Technologies Used

- **Streamlit**: Web application framework
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Database engine
- **Pandas**: Data manipulation
- **Plotly**: Data visualization
- **Python**: Programming language

## 👥 Sample Data

The system comes pre-populated with:
- 20 sample books across various genres
- 8 sample user accounts
- 25 historical borrowing records
- 12 active borrowing records
- 8 active reservations
- 15 historical reservations

## 🚀 Future Enhancements

- Email notification system for due dates and reservations
- Fine management for overdue books
- Barcode/QR code integration for physical books
- Enhanced reporting and analytics
- Mobile-responsive design improvements

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

