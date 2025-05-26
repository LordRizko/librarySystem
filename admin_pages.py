import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from db import get_session, hash_password
from models import Book, User, Borrow, Reservation
from sqlalchemy import func, or_, and_, desc

def show_admin_dashboard():
    """Display an overview dashboard for administrators"""
    session = get_session()
    
    st.subheader("Library Dashboard")
    
    # Key metrics in cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_books = session.query(func.sum(Book.total_copies)).scalar() or 0
        st.metric("Total Books", f"{total_books}")
    
    with col2:
        total_users = session.query(func.count(User.id)).filter(User.is_admin == False).scalar() or 0
        st.metric("Registered Users", f"{total_users}")
    
    with col3:
        active_borrows = session.query(func.count(Borrow.id)).filter(Borrow.is_returned == False).scalar() or 0
        st.metric("Active Loans", f"{active_borrows}")
    
    with col4:
        active_reservations = session.query(func.count(Reservation.id)).filter(
            Reservation.fulfilled == False,
            Reservation.cancelled == False
        ).scalar() or 0
        st.metric("Active Reservations", f"{active_reservations}")
    
    # Books with no copies available
    st.subheader("Books with No Copies Available")
    unavailable_books = session.query(Book).filter(Book.available_copies == 0).all()
    if unavailable_books:
        unavailable_data = [{
            "Title": book.title,
            "Author": book.author, 
            "Total Copies": book.total_copies,
            "ISBN": book.isbn
        } for book in unavailable_books]
        st.dataframe(pd.DataFrame(unavailable_data), use_container_width=True)
    else:
        st.info("All books have at least one available copy.")
    
    # Recent activity
    st.subheader("Recent Activity")
    recent_borrows = session.query(Borrow).join(Book).join(User).order_by(desc(Borrow.borrow_date)).limit(5).all()
    
    if recent_borrows:
        recent_data = []
        for borrow in recent_borrows:
            activity_type = "Return" if borrow.is_returned else "Borrow"
            activity_date = borrow.return_date if borrow.is_returned else borrow.borrow_date
            recent_data.append({
                "Date": activity_date.strftime("%Y-%m-%d %H:%M"),
                "Activity": activity_type,
                "Book": borrow.book.title,
                "User": borrow.user.username,
                "Status": "Returned" if borrow.is_returned else f"Due: {borrow.due_date.strftime('%Y-%m-%d')}"
            })
        st.dataframe(pd.DataFrame(recent_data), use_container_width=True)
    else:
        st.info("No recent borrowing activity.")
    
    # Visualizations
    st.subheader("Analytics")
    
    tab1, tab2 = st.tabs(["Borrowing Trends", "Popular Books"])
    
    with tab1:
        # Get borrowing data for the last 30 days
        thirty_days_ago = datetime.now() - timedelta(days=30)
        borrow_counts = session.query(
            func.date(Borrow.borrow_date).label('date'),
            func.count(Borrow.id).label('count')
        ).filter(Borrow.borrow_date >= thirty_days_ago).group_by(func.date(Borrow.borrow_date)).all()
        
        return_counts = session.query(
            func.date(Borrow.return_date).label('date'),
            func.count(Borrow.id).label('count')
        ).filter(
            Borrow.is_returned == True,
            Borrow.return_date >= thirty_days_ago
        ).group_by(func.date(Borrow.return_date)).all()
        
        if borrow_counts:
            borrow_df = pd.DataFrame([(row.date, row.count, 'Borrowed') for row in borrow_counts], 
                                    columns=['date', 'count', 'action'])
            return_df = pd.DataFrame([(row.date, row.count, 'Returned') for row in return_counts],
                                    columns=['date', 'count', 'action'])
            
            activity_df = pd.concat([borrow_df, return_df], ignore_index=True)
            
            fig = px.line(activity_df, x='date', y='count', color='action',
                        title='Book Borrowing and Return Activity (Last 30 Days)',
                        labels={'count': 'Number of Books', 'date': 'Date'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Not enough data to generate borrowing trends.")
    
    with tab2:
        # Most popular books by borrow count
        popular_books = session.query(
            Book.title, Book.author,
            func.count(Borrow.id).label('borrow_count')
        ).join(Borrow).group_by(Book.id).order_by(desc('borrow_count')).limit(10).all()
        
        if popular_books:
            popular_df = pd.DataFrame([(row.title, row.author, row.borrow_count) for row in popular_books],
                                    columns=['Title', 'Author', 'Borrow Count'])
            
            fig = px.bar(popular_df, x='Title', y='Borrow Count',
                        title='Most Popular Books',
                        hover_data=['Author'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Not enough data to determine popular books.")
    
    session.close()

def manage_books():
    """Interface for administrators to manage books"""
    st.subheader("Book Management")
    
    # Create tabs for different operations
    tab1, tab2 = st.tabs(["Add/Edit Books", "Book Inventory"])
    
    session = get_session()
    
    with tab1:
        # Form to add a new book
        st.subheader("Add a New Book")
        with st.form("add_book_form"):
            new_title = st.text_input("Title")
            new_author = st.text_input("Author")
            new_isbn = st.text_input("ISBN")
            new_publisher = st.text_input("Publisher")
            new_publication_year = st.number_input("Publication Year", min_value=1000, max_value=datetime.now().year, value=datetime.now().year)
            new_genre = st.text_input("Genre")
            new_description = st.text_area("Description")
            new_copies = st.number_input("Number of Copies", min_value=1, value=1)
            
            submitted = st.form_submit_button("Add Book")
            
            if submitted:
                # Check if ISBN already exists
                existing_book = session.query(Book).filter(Book.isbn == new_isbn).first()
                
                if existing_book:
                    st.error(f"A book with ISBN {new_isbn} already exists.")
                else:
                    new_book = Book(
                        title=new_title,
                        author=new_author,
                        isbn=new_isbn,
                        publisher=new_publisher,
                        publication_year=new_publication_year,
                        genre=new_genre,
                        description=new_description,
                        total_copies=new_copies,
                        available_copies=new_copies
                    )
                    session.add(new_book)
                    session.commit()
                    st.success(f"Book '{new_title}' has been added successfully.")
                    st.rerun()
        
        # Form to edit an existing book
        st.subheader("Edit an Existing Book")
        
        # Get all books for selection
        books = session.query(Book).order_by(Book.title).all()
        book_options = ["Select a book..."] + [f"{book.title} ({book.isbn})" for book in books]
        
        selected_book_idx = st.selectbox("Select a book to edit", options=range(len(book_options)), 
                                         format_func=lambda x: book_options[x])
        
        if selected_book_idx > 0:  # If a book is selected (not the "Select a book..." option)
            selected_book = books[selected_book_idx - 1]  # -1 because of the "Select a book..." option
            
            with st.form("edit_book_form"):
                edit_title = st.text_input("Title", value=selected_book.title)
                edit_author = st.text_input("Author", value=selected_book.author)
                edit_isbn = st.text_input("ISBN", value=selected_book.isbn)
                edit_publisher = st.text_input("Publisher", value=selected_book.publisher)
                edit_publication_year = st.number_input("Publication Year", min_value=1000, max_value=datetime.now().year, value=selected_book.publication_year)
                edit_genre = st.text_input("Genre", value=selected_book.genre)
                edit_description = st.text_area("Description", value=selected_book.description)
                
                col1, col2 = st.columns(2)
                with col1:
                    edit_total_copies = st.number_input("Total Copies", min_value=1, value=selected_book.total_copies)
                with col2:
                    edit_available_copies = st.number_input("Available Copies", min_value=0, max_value=edit_total_copies, value=min(selected_book.available_copies, edit_total_copies))
                
                update_submitted = st.form_submit_button("Update Book")
                
                if update_submitted:
                    # Check if ISBN is changed and already exists
                    if edit_isbn != selected_book.isbn:
                        existing_book = session.query(Book).filter(Book.isbn == edit_isbn).first()
                        if existing_book:
                            st.error(f"A book with ISBN {edit_isbn} already exists.")
                            session.close()
                            return
                    
                    selected_book.title = edit_title
                    selected_book.author = edit_author
                    selected_book.isbn = edit_isbn
                    selected_book.publisher = edit_publisher
                    selected_book.publication_year = edit_publication_year
                    selected_book.genre = edit_genre
                    selected_book.description = edit_description
                    selected_book.total_copies = edit_total_copies
                    selected_book.available_copies = edit_available_copies
                    
                    session.commit()
                    st.success(f"Book '{edit_title}' has been updated successfully.")
                    st.rerun()
    
    with tab2:
        # Book inventory table with search
        st.subheader("Book Inventory")
        
        # Search functionality
        search_query = st.text_input("Search books by title, author, or ISBN", key="inventory_search")
        
        if search_query:
            books = session.query(Book).filter(
                or_(
                    Book.title.ilike(f"%{search_query}%"),
                    Book.author.ilike(f"%{search_query}%"),
                    Book.isbn.ilike(f"%{search_query}%")
                )
            ).all()
        else:
            books = session.query(Book).order_by(Book.title).all()
        
        if books:
            # Convert to DataFrame for display
            books_data = [{
                "Title": book.title,
                "Author": book.author,
                "ISBN": book.isbn,
                "Genre": book.genre,
                "Year": book.publication_year,
                "Available": book.available_copies,
                "Total": book.total_copies
            } for book in books]
            
            books_df = pd.DataFrame(books_data)
            st.dataframe(books_df, use_container_width=True)
            
            # Book removal
            st.subheader("Remove a Book")
            book_to_remove = st.selectbox(
                "Select a book to remove",
                options=["Select a book..."] + [f"{book.title} ({book.isbn})" for book in books],
                key="remove_book_select"
            )
            
            if book_to_remove != "Select a book...":
                isbn_to_remove = book_to_remove.split("(")[-1].split(")")[0]
                book_to_delete = session.query(Book).filter(Book.isbn == isbn_to_remove).first()
                
                if st.button(f"Remove '{book_to_delete.title}'"):
                    # Check if any copies are currently borrowed
                    active_borrows = session.query(Borrow).filter(
                        Borrow.book_id == book_to_delete.id,
                        Borrow.is_returned == False
                    ).count()
                    
                    if active_borrows > 0:
                        st.error(f"Cannot remove book. {active_borrows} copies are currently borrowed.")
                    else:
                        session.delete(book_to_delete)
                        session.commit()
                        st.success(f"Book '{book_to_delete.title}' has been removed.")
                        st.rerun()
        else:
            st.info("No books found matching your search criteria.")
    
    session.close()

def manage_users():
    """Interface for administrators to manage users"""
    st.subheader("User Management")
    
    session = get_session()
    
    # Create tabs for different operations
    tab1, tab2, tab3 = st.tabs(["View Users", "Add User", "User Activity"])
    
    with tab1:
        # Search users
        search_query = st.text_input("Search users by username, email, or name")
        
        if search_query:
            users = session.query(User).filter(
                or_(
                    User.username.ilike(f"%{search_query}%"),
                    User.email.ilike(f"%{search_query}%"),
                    User.full_name.ilike(f"%{search_query}%")
                )
            ).order_by(User.username).all()
        else:
            users = session.query(User).order_by(User.username).all()
        
        if users:
            for user in users:
                with st.expander(f"👤 {user.username} - {user.full_name}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Username:** {user.username}")
                        st.write(f"**Full Name:** {user.full_name}")
                        st.write(f"**Email:** {user.email}")
                        st.write(f"**Role:** {'Administrator' if user.is_admin else 'User'}")
                    
                    with col2:
                        st.write(f"**Address:** {user.address if user.address else 'Not provided'}")
                        st.write(f"**Phone:** {user.phone if user.phone else 'Not provided'}")
                        st.write(f"**Registered:** {user.registration_date.strftime('%B %d, %Y')}")
                        
                        # Count active borrows for this user
                        active_borrows = session.query(func.count(Borrow.id)).filter(
                            Borrow.user_id == user.id,
                            Borrow.is_returned == False
                        ).scalar()
                        
                        st.write(f"**Active Borrows:** {active_borrows}")
                    
                    # Edit user form
                    with st.form(key=f"edit_user_{user.id}"):
                        st.subheader(f"Edit User: {user.username}")
                        
                        edit_full_name = st.text_input("Full Name", value=user.full_name)
                        edit_email = st.text_input("Email", value=user.email)
                        edit_address = st.text_input("Address", value=user.address if user.address else "")
                        edit_phone = st.text_input("Phone", value=user.phone if user.phone else "")
                        edit_is_admin = st.checkbox("Administrator", value=user.is_admin)
                        edit_password = st.text_input("New Password (leave blank to keep current)", type="password")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            update_submitted = st.form_submit_button("Update User")
                        with col2:
                            delete_submitted = st.form_submit_button("Delete User")
                        
                        if update_submitted:
                            user.full_name = edit_full_name
                            user.email = edit_email
                            user.address = edit_address
                            user.phone = edit_phone
                            user.is_admin = edit_is_admin
                            
                            if edit_password:
                                user.password = hash_password(edit_password)
                            
                            session.commit()
                            st.success(f"User '{user.username}' has been updated successfully.")
                            st.rerun()
                        
                        if delete_submitted:
                            # Check if user has active borrows
                            if active_borrows > 0:
                                st.error(f"Cannot delete user. {active_borrows} books are currently borrowed.")
                            else:
                                try:
                                    session.delete(user)
                                    session.commit()
                                    st.success(f"User '{user.username}' has been deleted.")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error deleting user: {str(e)}")
                                    session.rollback()
        else:
            st.info("No users found matching your search criteria.")
    
    with tab2:
        # Form to add a new user
        st.subheader("Add a New User")
        with st.form("add_user_form"):
            new_username = st.text_input("Username")
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            new_full_name = st.text_input("Full Name")
            new_address = st.text_input("Address (optional)")
            new_phone = st.text_input("Phone (optional)")
            new_is_admin = st.checkbox("Administrator")
            
            submitted = st.form_submit_button("Add User")
            
            if submitted:
                # Check if username or email already exists
                existing_user = session.query(User).filter(
                    or_(
                        User.username == new_username,
                        User.email == new_email
                    )
                ).first()
                
                if existing_user:
                    st.error(f"A user with that username or email already exists.")
                else:
                    new_user = User(
                        username=new_username,
                        email=new_email,
                        password=hash_password(new_password),
                        full_name=new_full_name,
                        address=new_address,
                        phone=new_phone,
                        is_admin=new_is_admin,
                        registration_date=datetime.now()
                    )
                    session.add(new_user)
                    session.commit()
                    st.success(f"User '{new_username}' has been added successfully.")
                    st.rerun()
    
    with tab3:
        # User activity and statistics
        st.subheader("User Activity")
        
        # Select user
        users = session.query(User).order_by(User.username).all()
        user_options = ["All Users"] + [f"{user.username} - {user.full_name}" for user in users]
        
        selected_user_idx = st.selectbox("Select a user", options=range(len(user_options)), 
                                        format_func=lambda x: user_options[x])
        
        # Get activity data
        borrows_query = session.query(Borrow).join(Book).join(User)
        
        if selected_user_idx > 0:  # If specific user selected
            selected_user = users[selected_user_idx - 1]  # -1 because of "All Users" option
            borrows_query = borrows_query.filter(Borrow.user_id == selected_user.id)
        
        borrows = borrows_query.order_by(desc(Borrow.borrow_date)).all()
        
        if borrows:
            # Convert to DataFrame for display
            borrows_data = [{
                "Book": borrow.book.title,
                "User": borrow.user.username,
                "Borrow Date": borrow.borrow_date.strftime("%Y-%m-%d"),
                "Due Date": borrow.due_date.strftime("%Y-%m-%d"),
                "Returned": "Yes" if borrow.is_returned else "No",
                "Return Date": borrow.return_date.strftime("%Y-%m-%d") if borrow.return_date else "",
                "Status": "On time" if borrow.is_returned and borrow.return_date <= borrow.due_date else 
                         "Late" if borrow.is_returned and borrow.return_date > borrow.due_date else
                         "Overdue" if datetime.now() > borrow.due_date else "Current"
            } for borrow in borrows]
            
            borrows_df = pd.DataFrame(borrows_data)
            st.dataframe(borrows_df, use_container_width=True)
            
            # Statistics
            st.subheader("Borrowing Statistics")
            
            total_borrows = len(borrows)
            returned = sum(1 for b in borrows if b.is_returned)
            current = total_borrows - returned
            overdue = sum(1 for b in borrows if not b.is_returned and datetime.now() > b.due_date)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Borrows", total_borrows)
            with col2:
                st.metric("Returned", returned)
            with col3:
                st.metric("Current", current)
            with col4:
                st.metric("Overdue", overdue)
        else:
            st.info("No borrowing activity recorded.")
    
    session.close()

def manage_reservations():
    """Interface for administrators to manage book reservations"""
    st.subheader("Reservation Management")
    
    session = get_session()
    
    # Get all active reservations
    active_reservations = session.query(Reservation).join(Book).join(User).filter(
        Reservation.fulfilled == False,
        Reservation.cancelled == False
    ).order_by(Reservation.reservation_date).all()
    
    # Display active reservations
    st.subheader("Active Reservations")
    
    if not active_reservations:
        st.info("There are no active reservations.")
    else:
        for reservation in active_reservations:
            with st.expander(f"📚 {reservation.book.title} - Reserved by {reservation.user.username}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Book:** {reservation.book.title}")
                    st.write(f"**Author:** {reservation.book.author}")
                    st.write(f"**User:** {reservation.user.full_name} ({reservation.user.username})")
                    st.write(f"**Reserved on:** {reservation.reservation_date.strftime('%B %d, %Y')}")
                    st.write(f"**Expires on:** {reservation.expiry_date.strftime('%B %d, %Y')}")
                    
                    # Check if book is available
                    if reservation.book.available_copies > 0:
                        st.success("This book is now available for this reservation!")
                    else:
                        st.warning("No copies of this book are currently available.")
                
                with col2:
                    if reservation.book.available_copies > 0:
                        # Mark as fulfilled (converted to borrow)
                        if st.button(f"Mark as Fulfilled", key=f"fulfill_{reservation.id}"):
                            # Create borrow record
                            new_borrow = Borrow(
                                user_id=reservation.user_id,
                                book_id=reservation.book_id,
                                borrow_date=datetime.now(),
                                due_date=datetime.now() + timedelta(days=14),
                                is_returned=False
                            )
                            # Update book availability
                            reservation.book.available_copies -= 1
                            
                            # Mark reservation as fulfilled
                            reservation.fulfilled = True
                            
                            session.add(new_borrow)
                            session.commit()
                            st.success(f"Reservation fulfilled and converted to borrow for '{reservation.book.title}'")
                            st.rerun()
                    
                    # Cancel reservation
                    if st.button(f"Cancel Reservation", key=f"admin_cancel_{reservation.id}"):
                        reservation.cancelled = True
                        session.commit()
                        st.success(f"Reservation cancelled for '{reservation.book.title}'")
                        st.rerun()
    
    # Display reservation history (fulfilled or cancelled)
    st.subheader("Reservation History")
    
    history_reservations = session.query(Reservation).join(Book).join(User).filter(
        or_(
            Reservation.fulfilled == True,
            Reservation.cancelled == True
        )
    ).order_by(desc(Reservation.reservation_date)).limit(50).all()
    
    if not history_reservations:
        st.info("No reservation history available.")
    else:
        history_data = [{
            "Book": res.book.title,
            "User": res.user.username,
            "Reserved On": res.reservation_date.strftime("%Y-%m-%d"),
            "Status": "Fulfilled" if res.fulfilled else "Cancelled",
            "Expiry": res.expiry_date.strftime("%Y-%m-%d")
        } for res in history_reservations]
        
        st.dataframe(pd.DataFrame(history_data), use_container_width=True)
    
    session.close()

def manage_borrows():
    """Interface for administrators to manage book borrows and returns"""
    st.subheader("Loan Management")
    
    session = get_session()
    
    # Create tabs for active loans and loan history
    tab1, tab2 = st.tabs(["Active Loans", "Loan History"])
    
    with tab1:
        # Get all active borrows
        active_borrows = session.query(Borrow).join(Book).join(User).filter(
            Borrow.is_returned == False
        ).order_by(Borrow.due_date).all()
        
        # Display active borrows
        st.subheader("Active Loans")
        
        if not active_borrows:
            st.info("There are no active loans.")
        else:
            # Filter options
            filter_col1, filter_col2 = st.columns(2)
            with filter_col1:
                show_overdue = st.checkbox("Show only overdue", value=False)
            with filter_col2:
                search_query = st.text_input("Search by book title or user")
            
            # Apply filters
            filtered_borrows = active_borrows
            if show_overdue:
                filtered_borrows = [b for b in filtered_borrows if datetime.now() > b.due_date]
            if search_query:
                filtered_borrows = [b for b in filtered_borrows if 
                                    search_query.lower() in b.book.title.lower() or 
                                    search_query.lower() in b.user.username.lower() or
                                    search_query.lower() in b.user.full_name.lower()]
            
            if not filtered_borrows:
                st.info("No loans match the current filters.")
            else:
                for borrow in filtered_borrows:
                    # Calculate days left or overdue
                    days_left = (borrow.due_date - datetime.now()).days
                    status_color = "red" if days_left < 0 else "orange" if days_left < 3 else "green"
                    status_text = f"Overdue by {abs(days_left)} days" if days_left < 0 else f"{days_left} days remaining"
                    
                    with st.expander(f"📚 {borrow.book.title} - Borrowed by {borrow.user.username} ({status_text})"):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.write(f"**Book:** {borrow.book.title}")
                            st.write(f"**Author:** {borrow.book.author}")
                            st.write(f"**User:** {borrow.user.full_name} ({borrow.user.username})")
                            st.write(f"**Borrowed on:** {borrow.borrow_date.strftime('%B %d, %Y')}")
                            st.write(f"**Due date:** {borrow.due_date.strftime('%B %d, %Y')}")
                            
                            if days_left < 0:
                                st.error(f"**Overdue by {abs(days_left)} days**")
                            elif days_left < 3:
                                st.warning(f"**Due soon: {days_left} days left**")
                            else:
                                st.success(f"**Days remaining: {days_left}**")
                        
                        with col2:
                            # Return book button
                            if st.button(f"Mark as Returned", key=f"admin_return_{borrow.id}"):
                                borrow.is_returned = True
                                borrow.return_date = datetime.now()
                                borrow.book.available_copies += 1
                                session.commit()
                                st.success(f"'{borrow.book.title}' marked as returned.")
                                st.rerun()
                            
                            # Extend due date
                            if st.button(f"Extend Due Date", key=f"admin_extend_{borrow.id}"):
                                borrow.due_date = borrow.due_date + timedelta(days=7)
                                borrow.extended_times += 1
                                session.commit()
                                st.success(f"Due date extended by 7 days. New due date: {borrow.due_date.strftime('%B %d, %Y')}")
                                st.rerun()
    
    with tab2:
        # Get loan history (returned books)
        loan_history = session.query(Borrow).join(Book).join(User).filter(
            Borrow.is_returned == True
        ).order_by(desc(Borrow.return_date)).all()
        
        # Display loan history
        st.subheader("Loan History")
        
        if not loan_history:
            st.info("No loan history available.")
        else:
            # Search filter
            search_history = st.text_input("Search loan history by book title or user", key="history_search")
            
            # Apply filter
            if search_history:
                filtered_history = [b for b in loan_history if 
                                   search_history.lower() in b.book.title.lower() or 
                                   search_history.lower() in b.user.username.lower() or
                                   search_history.lower() in b.user.full_name.lower()]
            else:
                filtered_history = loan_history
            
            # Convert to DataFrame for display
            history_data = [{
                "Book": borrow.book.title,
                "Author": borrow.book.author,
                "User": borrow.user.username,
                "Borrowed": borrow.borrow_date.strftime("%Y-%m-%d"),
                "Returned": borrow.return_date.strftime("%Y-%m-%d"),
                "Duration": f"{(borrow.return_date - borrow.borrow_date).days} days",
                "On Time": "Yes" if borrow.return_date <= borrow.due_date else "No"
            } for borrow in filtered_history]
            
            st.dataframe(pd.DataFrame(history_data), use_container_width=True)
    
    session.close()