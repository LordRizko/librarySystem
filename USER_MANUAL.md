# Library Management System - User Manual

This user manual provides detailed instructions on how to use the Library Management System for both regular users and administrators.

## Table of Contents

1. [Getting Started](#getting-started)
2. [User Guide](#user-guide)
3. [Administrator Guide](#administrator-guide)
4. [Troubleshooting](#troubleshooting)
5. [FAQ](#faq)

## Getting Started

### System Requirements

- Web browser (Chrome, Firefox, Safari, or Edge recommended)
- Internet connection
- Screen resolution of 1280x720 or higher (for best experience)

### Accessing the System

1. Launch the application using:
   ```
   streamlit run app.py
   ```
2. Navigate to the URL displayed in the terminal (typically http://localhost:8501)
3. You will be presented with the login/registration page

### Account Registration

1. On the login page, locate the "Register" section on the right side
2. Fill in the required information:
   - Username (must be unique)
   - Email address (must be unique)
   - Password
   - Confirm Password (must match)
   - Full Name
3. Click the "Register" button
4. If registration is successful, you will be automatically logged in

### Logging In

1. On the login page, enter your credentials:
   - Username
   - Password
2. Click the "Login" button
3. If authentication is successful, you will be redirected to the main interface

## User Guide

### Navigation

After logging in as a regular user, you'll see a sidebar menu with three options:
- **Book Catalog**: Browse and search for books
- **My Books**: View your borrowed books and reservation history
- **My Profile**: Update your personal information

### Browsing the Book Catalog

1. Click on "Book Catalog" in the sidebar
2. You will see a search section at the top:
   - Search by title, author, or ISBN
   - Filter by genre
   - Sort by title, author, or publication year
3. Click "Search" to apply filters
4. Browse through the displayed books

### Borrowing a Book

1. In the Book Catalog, find the book you want to borrow
2. Check that the book shows "Available" status
3. Click the "Borrow" button next to the book
4. Confirm the borrowing action when prompted
5. The book will now appear in your "My Books" section
6. Note the due date (typically 14 days from borrowing)

### Reserving a Book

1. In the Book Catalog, find the book you want to reserve
2. If the book shows "Unavailable" status, a "Reserve" button will appear
3. Click the "Reserve" button
4. Confirm the reservation action when prompted
5. The reservation will appear in your "My Books" section
6. You will be notified when the book becomes available

### Viewing Your Books

1. Click on "My Books" in the sidebar
2. The page is divided into sections:
   - Currently Borrowed Books
   - Reservations
   - Borrowing History

### Returning a Book

1. Go to "My Books" in the sidebar
2. Find the book you want to return in the "Currently Borrowed Books" section
3. Click the "Return" button next to the book
4. Confirm the return action when prompted
5. The book will move to your borrowing history

### Extending a Loan

1. Go to "My Books" in the sidebar
2. Find the book you want to extend in the "Currently Borrowed Books" section
3. Click the "Extend" button next to the book
4. If extension is allowed (maximum 2 times), the due date will be extended by 7 days
5. The updated due date will be displayed

### Updating Your Profile

1. Click on "My Profile" in the sidebar
2. View your current information
3. In the "Update Profile" section, modify any information you wish to update:
   - Full Name
   - Email
   - Address
   - Phone
4. Click "Update Profile" to save your changes

### Logging Out

1. Click the "Logout" button at the bottom of the sidebar
2. You will be redirected to the login page

## Administrator Guide

### Administrator Dashboard

After logging in as an administrator, you'll see a sidebar menu with five options:
- **Dashboard**: Overview of library statistics
- **Books**: Book management
- **Users**: User management
- **Loans**: Loan management
- **Reservations**: Reservation management

### Viewing Dashboard Statistics

1. Click on "Dashboard" in the sidebar
2. View key metrics:
   - Total Books
   - Registered Users
   - Active Loans
   - Active Reservations
3. Scroll down to see:
   - Books with No Copies Available
   - Recent Borrowing Activity
   - Book Genre Distribution
   - Monthly Borrowing Trends

### Managing Books

1. Click on "Books" in the sidebar
2. View the complete book catalog with all book details
3. To add a new book:
   - Scroll down to the "Add New Book" form
   - Fill in all required fields
   - Click "Add Book"
4. To edit a book:
   - Find the book in the catalog
   - Click "Edit" next to the book
   - Modify the information in the form that appears
   - Click "Update Book"
5. To delete a book:
   - Find the book in the catalog
   - Click "Delete" next to the book
   - Confirm the deletion when prompted

### Managing Users

1. Click on "Users" in the sidebar
2. View the list of all registered users
3. To view user details:
   - Click on a user's name to expand their information
4. To edit user information:
   - Find the user in the list
   - Click "Edit" next to the user
   - Modify the information in the form that appears
   - Click "Update User"
5. To delete a user:
   - Find the user in the list
   - Click "Delete" next to the user
   - Confirm the deletion when prompted

### Managing Loans

1. Click on "Loans" in the sidebar
2. View all active loans with due dates
3. To process a return:
   - Find the loan in the list
   - Click "Mark as Returned" next to the loan
   - Confirm the return action when prompted
4. To extend a loan:
   - Find the loan in the list
   - Click "Extend" next to the loan
   - The due date will be extended by 7 days

### Managing Reservations

1. Click on "Reservations" in the sidebar
2. View all active reservations
3. To fulfill a reservation:
   - Find the reservation in the list
   - Verify that the book is available
   - Click "Fulfill" next to the reservation
   - Confirm the action when prompted
4. To cancel a reservation:
   - Find the reservation in the list
   - Click "Cancel" next to the reservation
   - Confirm the cancellation when prompted

## Troubleshooting

### Login Issues

- **Issue**: Cannot log in with correct credentials
  - **Solution**: Verify username and password; try resetting your password through an administrator

- **Issue**: Forgot password
  - **Solution**: Contact the library administrator to reset your password

### Book Borrowing Issues

- **Issue**: Cannot borrow a book that shows as available
  - **Solution**: Refresh the page and try again; if the problem persists, contact the administrator

- **Issue**: Book due date is incorrect
  - **Solution**: Contact the library administrator to update the due date

### System Performance Issues

- **Issue**: Pages load slowly
  - **Solution**: Refresh the browser; ensure you have a stable internet connection

- **Issue**: Data doesn't update after making changes
  - **Solution**: Refresh the page or log out and log back in

## FAQ

**Q: How many books can I borrow at once?**
A: There is no hard limit, but libraries typically have policies on this. Check with your local library.

**Q: How long can I keep a borrowed book?**
A: The standard loan period is 14 days.

**Q: Can I extend my loan period?**
A: Yes, you can extend a loan up to 2 times, each extension adding 7 days to the due date.

**Q: How long will my reservation be held?**
A: Reservations are typically held for 3 days after the book becomes available.

**Q: Can I cancel my reservation?**
A: No, users cannot cancel their own reservations. Please contact the library administrator.

**Q: How do I return a book?**
A: Go to "My Books" and click "Return" next to the book you wish to return.

---

For technical support, please contact the system administrator.
