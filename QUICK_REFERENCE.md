# Library Management System - Quick Reference Guide

This quick reference guide provides a concise overview of the Library Management System's key features and workflows.

## System Overview

```
┌─────────────────────────────────────────────────────────┐
│                Library Management System                │
├─────────────────┬───────────────────┬──────────────────┤
│    User View    │   Admin View      │  Database        │
├─────────────────┼───────────────────┼──────────────────┤
│ - Book Catalog  │ - Dashboard       │ - Users          │
│ - My Books      │ - Book Management │ - Books          │
│ - My Profile    │ - User Management │ - Borrows        │
│                 │ - Loan Management │ - Reservations   │
│                 │ - Reservations    │                  │
└─────────────────┴───────────────────┴──────────────────┘
```

## Login Credentials

| Type  | Username | Password |
|-------|----------|----------|
| Admin | admin    | admin123 |
| User  | user     | user123  |

## User Workflow

### 1. Borrowing a Book

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Book Catalog│     │ Click Borrow │     │  Book Added  │
│    Page      ├────►│    Button    ├────►│ to My Books  │
└──────────────┘     └──────────────┘     └──────────────┘
```

### 2. Returning a Book

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   My Books   │     │ Click Return │     │Book Removed  │
│     Page     ├────►│    Button    ├────►│from My Books │
└──────────────┘     └──────────────┘     └──────────────┘
```

### 3. Reserving a Book

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Book Catalog│     │Click Reserve │     │ Reservation  │
│    Page      ├────►│    Button    ├────►│   Created    │
└──────────────┘     └──────────────┘     └──────────────┘
```

## Admin Workflow

### 1. Adding a Book

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    Books     │     │ Fill Add Book│     │ Book Added   │
│     Page     ├────►│     Form     ├────►│ to Catalog   │
└──────────────┘     └──────────────┘     └──────────────┘
```

### 2. Processing a Return

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    Loans     │     │ Click Mark as│     │Book Available│
│     Page     ├────►│   Returned   ├────►│   Again      │
└──────────────┘     └──────────────┘     └──────────────┘
```

### 3. Fulfilling a Reservation

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Reservations │     │ Click Fulfill│     │Book Borrowed │
│     Page     ├────►│    Button    ├────►│  by User     │
└──────────────┘     └──────────────┘     └──────────────┘
```

## Key Features Checklist

### User Features
- [ ] Browse book catalog
- [ ] Search for books
- [ ] Borrow available books
- [ ] Reserve unavailable books
- [ ] Return borrowed books
- [ ] View borrowing history
- [ ] Update personal profile

### Admin Features
- [ ] View library statistics
- [ ] Add/edit/delete books
- [ ] Manage user accounts
- [ ] Process book returns
- [ ] Fulfill reservations
- [ ] View system reports

## Common Tasks Quick Reference

### For Users

| Task | Navigation Path |
|------|----------------|
| Browse Books | Sidebar → Book Catalog |
| Borrow a Book | Book Catalog → Find Book → Click "Borrow" |
| Return a Book | My Books → Currently Borrowed → Click "Return" |
| Reserve a Book | Book Catalog → Find Book → Click "Reserve" |
| Update Profile | My Profile → Update Profile Form → Submit |

### For Administrators

| Task | Navigation Path |
|------|----------------|
| Add New Book | Books → Add New Book Form → Submit |
| Process Return | Loans → Find Loan → Click "Mark as Returned" |
| Fulfill Reservation | Reservations → Find Reservation → Click "Fulfill" |
| Add User | Users → Add New User Form → Submit |
| View Stats | Dashboard (homepage after login) |

## System Status Codes

| Status | Meaning |
|--------|---------|
| Available | Book can be borrowed |
| Unavailable | No copies available for borrowing |
| Borrowed | Book is currently borrowed by a user |
| Reserved | Book has been reserved |
| Overdue | Book was not returned by due date |
| Returned | Book was successfully returned |

## Command Reference (Development Only)

| Command | Description |
|---------|-------------|
| `streamlit run app.py` | Start the application |
| `python -c "from db import init_db; init_db()"` | Initialize database |
| `python -c "from db import add_sample_data; add_sample_data()"` | Add sample data |

---

For detailed instructions, please refer to the full [USER_MANUAL.md](./USER_MANUAL.md)
