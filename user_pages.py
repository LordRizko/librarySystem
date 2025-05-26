import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from db import get_session
from models import Book, Borrow, Reservation, User
from sqlalchemy import or_, and_

def show_user_profile(user_id):
    """Show user profile information"""
    session = get_session()
    user = session.query(User).filter(User.id == user_id).first()
    
    st.subheader("My Profile")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Username:** {user.username}")
        st.write(f"**Email:** {user.email}")
        st.write(f"**Full Name:** {user.full_name}")
    
    with col2:
        st.write(f"**Address:** {user.address if user.address else 'Not provided'}")
        st.write(f"**Phone:** {user.phone if user.phone else 'Not provided'}")
        st.write(f"**Registered:** {user.registration_date.strftime('%B %d, %Y')}")
    
    # Edit profile form
    st.subheader("Update Profile")
    with st.form("profile_form"):
        new_full_name = st.text_input("Full Name", value=user.full_name)
        new_email = st.text_input("Email", value=user.email)
        new_address = st.text_input("Address", value=user.address if user.address else "")
        new_phone = st.text_input("Phone", value=user.phone if user.phone else "")
        
        if st.form_submit_button("Update Profile"):
            user.full_name = new_full_name
            user.email = new_email
            user.address = new_address
            user.phone = new_phone
            session.commit()
            st.success("Profile updated successfully!")
            st.rerun()
    
    session.close()

def show_book_catalog():
    """Display book catalog for users to browse"""
    st.subheader("Book Catalog")
    
    session = get_session()
    
    # Search functionality
    search_col1, search_col2 = st.columns([3, 1])
    with search_col1:
        search_query = st.text_input("Search books by title, author, or ISBN")
    with search_col2:
        genre_filter = st.selectbox(
            "Filter by Genre",
            options=["All"] + sorted(list(set([b.genre for b in session.query(Book.genre).distinct()])))
        )
    
    # Apply filters
    if search_query:
        books = session.query(Book).filter(
            or_(
                Book.title.ilike(f"%{search_query}%"),
                Book.author.ilike(f"%{search_query}%"),
                Book.isbn.ilike(f"%{search_query}%")
            )
        )
    else:
        books = session.query(Book)
    
    if genre_filter and genre_filter != "All":
        books = books.filter(Book.genre == genre_filter)
        
    books = books.all()
    
    # Display books
    if not books:
        st.info("No books found matching your criteria.")
    else:
        for book in books:
            with st.expander(f"📚 {book.title} by {book.author}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Title:** {book.title}")
                    st.write(f"**Author:** {book.author}")
                    st.write(f"**Genre:** {book.genre}")
                    st.write(f"**ISBN:** {book.isbn}")
                    st.write(f"**Publisher:** {book.publisher}, {book.publication_year}")
                    st.write(f"**Description:** {book.description}")
                
                with col2:
                    st.write(f"**Available:** {book.available_copies} / {book.total_copies}")
                    
                    # Get current user and any existing borrows or reservations
                    user_id = st.session_state.user_id
                    existing_borrow = session.query(Borrow).filter(
                        Borrow.user_id == user_id,
                        Borrow.book_id == book.id,
                        Borrow.is_returned == False
                    ).first()
                    
                    existing_reservation = session.query(Reservation).filter(
                        Reservation.user_id == user_id,
                        Reservation.book_id == book.id,
                        Reservation.fulfilled == False,
                        Reservation.cancelled == False
                    ).first()
                    
                    if existing_borrow:
                        st.info(f"You have borrowed this book. Due: {existing_borrow.due_date.strftime('%b %d, %Y')}")
                    elif existing_reservation:
                        st.info("You have reserved this book")
                        if st.button(f"Cancel Reservation for '{book.title}'", key=f"cancel_{book.id}"):
                            existing_reservation.cancelled = True
                            session.commit()
                            st.success("Reservation canceled successfully!")
                            st.rerun()
                    elif book.available_copies > 0:
                        if st.button(f"Borrow '{book.title}'", key=f"borrow_{book.id}"):
                            # Create borrow record
                            new_borrow = Borrow(
                                user_id=user_id,
                                book_id=book.id,
                                borrow_date=datetime.now(),
                                due_date=datetime.now() + timedelta(days=14),
                                is_returned=False
                            )
                            # Update book availability
                            book.available_copies -= 1
                            
                            session.add(new_borrow)
                            session.commit()
                            st.success(f"You have successfully borrowed '{book.title}'")
                            st.rerun()
                    else:
                        st.warning("No copies available")
                        if st.button(f"Reserve '{book.title}'", key=f"reserve_{book.id}"):
                            # Create reservation record
                            new_reservation = Reservation(
                                user_id=user_id,
                                book_id=book.id,
                                reservation_date=datetime.now(),
                                expiry_date=datetime.now() + timedelta(days=3),
                                fulfilled=False
                            )
                            
                            session.add(new_reservation)
                            session.commit()
                            st.success(f"You have successfully reserved '{book.title}'")
                            st.rerun()
    
    session.close()

def show_my_books(user_id):
    """Show books borrowed and reserved by the user"""
    st.subheader("My Books")
    
    session = get_session()
    
    # Create tabs for borrowed and reserved books
    tab1, tab2 = st.tabs(["Borrowed Books", "Reserved Books"])
    
    with tab1:
        # Get borrowed books
        borrows = session.query(Borrow).join(Book).filter(
            Borrow.user_id == user_id,
            Borrow.is_returned == False
        ).all()
        
        if not borrows:
            st.info("You haven't borrowed any books yet.")
        else:
            for borrow in borrows:
                with st.expander(f"📚 {borrow.book.title}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Title:** {borrow.book.title}")
                        st.write(f"**Author:** {borrow.book.author}")
                        st.write(f"**Borrowed on:** {borrow.borrow_date.strftime('%B %d, %Y')}")
                        st.write(f"**Due date:** {borrow.due_date.strftime('%B %d, %Y')}")
                        
                        # Calculate days remaining or overdue
                        days_left = (borrow.due_date - datetime.now()).days
                        if days_left < 0:
                            st.error(f"**Overdue by {abs(days_left)} days**")
                        elif days_left < 3:
                            st.warning(f"**Due soon: {days_left} days left**")
                        else:
                            st.write(f"**Days remaining:** {days_left}")
                    
                    with col2:
                        # Return book button
                        if st.button(f"Return '{borrow.book.title}'", key=f"return_{borrow.id}"):
                            borrow.is_returned = True
                            borrow.return_date = datetime.now()
                            borrow.book.available_copies += 1
                            
                            # Check for reservations
                            pending_reservation = session.query(Reservation).filter(
                                Reservation.book_id == borrow.book_id,
                                Reservation.fulfilled == False,
                                Reservation.cancelled == False
                            ).order_by(Reservation.reservation_date).first()
                            
                            session.commit()
                            st.success(f"You have successfully returned '{borrow.book.title}'")
                            
                            if pending_reservation:
                                st.info(f"This book was reserved by another user and is now available for them.")
                            
                            st.rerun()
                        
                        # Extend borrow button (if not already extended twice)
                        if borrow.extended_times < 2 and days_left > 0:
                            if st.button(f"Extend loan period", key=f"extend_{borrow.id}"):
                                borrow.due_date = borrow.due_date + timedelta(days=7)
                                borrow.extended_times += 1
                                session.commit()
                                st.success(f"Loan period extended by 7 days. New due date: {borrow.due_date.strftime('%B %d, %Y')}")
                                st.rerun()
    
    with tab2:
        # Get reserved books
        reservations = session.query(Reservation).join(Book).filter(
            Reservation.user_id == user_id,
            Reservation.fulfilled == False,
            Reservation.cancelled == False
        ).all()
        
        if not reservations:
            st.info("You don't have any active reservations.")
        else:
            for reservation in reservations:
                with st.expander(f"📚 {reservation.book.title}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Title:** {reservation.book.title}")
                        st.write(f"**Author:** {reservation.book.author}")
                        st.write(f"**Reserved on:** {reservation.reservation_date.strftime('%B %d, %Y')}")
                        st.write(f"**Reservation expires:** {reservation.expiry_date.strftime('%B %d, %Y')}")
                        
                        # Check if book is available now
                        if reservation.book.available_copies > 0:
                            st.success("This book is now available for you to borrow!")
                    
                    with col2:
                        if reservation.book.available_copies > 0:
                            # Convert reservation to borrow
                            if st.button(f"Borrow now", key=f"borrow_reserved_{reservation.id}"):
                                # Create borrow record
                                new_borrow = Borrow(
                                    user_id=user_id,
                                    book_id=reservation.book_id,
                                    borrow_date=datetime.now(),
                                    due_date=datetime.now() + timedelta(days=14),
                                    is_returned=False
                                )
                                # Update book availability
                                reservation.book.available_copies -= 1
                                
                                # Fulfill reservation
                                reservation.fulfilled = True
                                
                                session.add(new_borrow)
                                session.commit()
                                st.success(f"You have successfully borrowed '{reservation.book.title}'")
                                st.rerun()
                        
                        # Cancel reservation
                        if st.button(f"Cancel reservation", key=f"cancel_reservation_{reservation.id}"):
                            reservation.cancelled = True
                            session.commit()
                            st.success(f"Reservation for '{reservation.book.title}' cancelled.")
                            st.rerun()
    
    # Show borrowing history
    st.subheader("Borrowing History")
    past_borrows = session.query(Borrow).join(Book).filter(
        Borrow.user_id == user_id,
        Borrow.is_returned == True
    ).order_by(Borrow.return_date.desc()).all()
    
    if not past_borrows:
        st.info("No borrowing history yet.")
    else:
        history_data = []
        for borrow in past_borrows:
            history_data.append({
                "Book Title": borrow.book.title,
                "Author": borrow.book.author,
                "Borrowed": borrow.borrow_date.strftime("%b %d, %Y"),
                "Returned": borrow.return_date.strftime("%b %d, %Y"),
                "Duration": f"{(borrow.return_date - borrow.borrow_date).days} days"
            })
        
        st.dataframe(pd.DataFrame(history_data), use_container_width=True)
    
    session.close()