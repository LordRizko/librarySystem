import streamlit as st
import os
from db import init_db, add_sample_data, authenticate_user, get_session, hash_password
from models import User
from admin_pages import show_admin_dashboard, manage_books, manage_users, manage_reservations, manage_borrows
from user_pages import show_user_profile, show_book_catalog, show_my_books

# Configure Streamlit page
st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_db()
add_sample_data()

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None

def logout():
    """Log out the current user by resetting session state"""
    st.session_state.logged_in = False
    st.session_state.is_admin = False
    st.session_state.user_id = None
    st.session_state.username = None

def login_page():
    """Display login form"""
    st.title("📚 Library Management System")
    
    # Create columns for layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Login")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            
            if submitted:
                user = authenticate_user(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.is_admin = user.is_admin
                    st.session_state.user_id = user.id
                    st.session_state.username = user.username
                    st.success(f"Welcome back, {user.full_name}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password. Please try again.")
    
    with col2:
        st.subheader("Register")
        with st.form("register_form"):
            new_username = st.text_input("Username", key="reg_username")
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password", key="reg_password")
            confirm_password = st.text_input("Confirm Password", type="password")
            new_full_name = st.text_input("Full Name")
            
            register_submitted = st.form_submit_button("Register")
            
            if register_submitted:
                if new_password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    # Check if username or email already exists
                    session = get_session()
                    existing_user = session.query(User).filter(
                        (User.username == new_username) | (User.email == new_email)
                    ).first()
                    
                    if existing_user:
                        st.error("Username or email already exists.")
                    else:
                        # Create new user
                        hashed_password = hash_password(new_password)
                        new_user = User(
                            username=new_username,
                            email=new_email,
                            password=hashed_password,
                            full_name=new_full_name,
                            is_admin=False
                        )
                        session.add(new_user)
                        session.commit()
                        
                        # Auto login
                        st.session_state.logged_in = True
                        st.session_state.is_admin = False
                        st.session_state.user_id = new_user.id
                        st.session_state.username = new_user.username
                        
                        session.close()
                        st.success("Registration successful! You are now logged in.")
                        st.rerun()
    
    # Sample credentials notice
    st.info("""
    ### Sample Credentials
    
    **Admin:** username: `admin`, password: `admin123`
    
    **Regular User:** username: `user`, password: `user123`
    """)

def main_app():
    """Main application after login"""
    # Sidebar navigation
    st.sidebar.title("📚 Library System")
    st.sidebar.write(f"Welcome, {st.session_state.username}!")
    
    if st.session_state.is_admin:
        # Admin navigation
        nav_selection = st.sidebar.radio(
            "Navigation",
            ["Dashboard", "Books", "Users", "Loans", "Reservations"]
        )
        
        if nav_selection == "Dashboard":
            st.title("Admin Dashboard")
            show_admin_dashboard()
        
        elif nav_selection == "Books":
            st.title("Book Management")
            manage_books()
        
        elif nav_selection == "Users":
            st.title("User Management")
            manage_users()
        
        elif nav_selection == "Loans":
            st.title("Loan Management")
            manage_borrows()
        
        elif nav_selection == "Reservations":
            st.title("Reservation Management")
            manage_reservations()
    
    else:
        # Regular user navigation
        nav_selection = st.sidebar.radio(
            "Navigation",
            ["Book Catalog", "My Books", "My Profile"]
        )
        
        if nav_selection == "Book Catalog":
            st.title("Book Catalog")
            show_book_catalog()
        
        elif nav_selection == "My Books":
            st.title("My Books")
            show_my_books(st.session_state.user_id)
        
        elif nav_selection == "My Profile":
            st.title("My Profile")
            show_user_profile(st.session_state.user_id)
    
    # Logout button at the bottom of the sidebar
    st.sidebar.write("---")
    if st.sidebar.button("Logout"):
        logout()
        st.rerun()

# Main entry point
if st.session_state.logged_in:
    main_app()
else:
    login_page()

