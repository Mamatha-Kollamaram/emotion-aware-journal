import streamlit as st
import firebase_admin
from firebase_admin import auth, credentials, initialize_app
import pyrebase
import json


# Custom CSS styling
def inject_custom_css():
    st.markdown("""
    <style>
        /* Main container styling */
        .stApp {
            background-color: #f5f7fa;
            background-image: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        /* Title styling */
        .css-10trblm {
            color: #2c3e50;
            text-align: center;
            font-family: 'Arial', sans-serif;
            font-weight: 700;
            margin-bottom: 30px;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #2c3e50 !important;
            color: white !important;
            padding: 20px !important;
        }
        
        .st-b7, .st-cm, .st-cn, .st-co {
            color: white !important;
        }
        
        /* Sidebar selectbox styling */
        .st-b7 .st-cm {
            color: #2c3e50 !important;
        }
        
        /* Input field styling */
        .stTextInput input, .stTextInput input:focus {
            border-radius: 8px !important;
            border: 1px solid #dfe6e9 !important;
            padding: 10px !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
        }
        
        /* Button styling */
        .stButton>button {
            border-radius: 8px !important;
            border: none !important;
            background-color: #3498db !important;
            color: white !important;
            padding: 10px 24px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
        }
        
        .stButton>button:hover {
            background-color: #2980b9 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
        }
        
        /* Success message styling */
        .stAlert .st-bb {
            background-color: #2ecc71 !important;
            color: white !important;
            border-radius: 8px !important;
        }
        
        /* Error message styling */
        .stAlert .st-cm {
            background-color: #e74c3c !important;
            color: white !important;
            border-radius: 8px !important;
        }
        
        /* Card-like containers */
        .stContainer {
            background-color: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        /* Custom divider */
        .divider {
            height: 1px;
            background: linear-gradient(to right, transparent, #bdc3c7, transparent);
            margin: 20px 0;
        }
        
        /* Sidebar header styling */
        .sidebar-header {
            color: white !important;
            font-size: 1.5rem;
            margin-bottom: 20px;
            font-weight: 600;
        }
        
        /* Selectbox in sidebar */
        .stSelectbox div[data-baseweb="select"] {
            background-color: white !important;
            border-radius: 8px !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Inject CSS
inject_custom_css()

# ✅ 1. Load pyrebase frontend config from firebase_config.json
#with open("firebase_config.json") as f:
#   firebase_config = json.load(f)

firebase_config = json.loads(st.secrets["FIREBASE_CONFIG"])

# ✅ 2. Load Firebase Admin SDK credentials from firebase_service_key.json
# if not firebase_admin._apps:
#     cred = credentials.Certificate("firebase_service_key.json")

#     firebase_admin.initialize_app(cred)
firebase_service_key = json.loads(st.secrets["FIREBASE_SERVICE_KEY"])
# Initialize Firebase
cred = credentials.Certificate(firebase_service_key)
initialize_app(cred)

# ✅ 3. Initialize Pyrebase (for frontend auth)
firebase = pyrebase.initialize_app(firebase_config)
auth_client = firebase.auth()

# Check if user is already logged in
if "user_id" in st.session_state and st.session_state.user_id:
    st.success(f"✅ Logged in as {st.session_state.user_email}")
    st.switch_page("journal_app")  # Redirect to journal page

# Main container with shadow
with st.container():
    st.title("✨ AI Mood Tracker")
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Sidebar Navigation with custom styling
    with st.sidebar:
        st.markdown('<p class="sidebar-header">Authentication</p>', unsafe_allow_html=True)
        auth_choice = st.selectbox(
            "Select Action", 
            ["Sign Up", "Login"],
            key="auth_choice",
            label_visibility="visible"  # Ensure label is always visible
        )

    # Main content area
    if auth_choice == "Sign Up":
        with st.container():
            st.subheader("Create a New Account")
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            
            email = st.text_input("📧 Email Address", placeholder="your@email.com")
            password = st.text_input("🔑 Password", type="password", placeholder="Create a strong password")
            
            if st.button("Create Account", key="signup_btn"):
                try:
                    user = auth.create_user(email=email, password=password)
                    st.success("✅ Account created successfully! Please log in.")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    elif auth_choice == "Login":
        with st.container():
            st.subheader("Welcome Back!")
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            
            email = st.text_input("📧 Email Address", placeholder="your@email.com")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
            
            if st.button("Login", key="login_btn"):
                try:
                    # Authenticate using Pyrebase
                    user = auth_client.sign_in_with_email_and_password(email, password)

                    # Store user ID & email in session state
                    st.session_state.user_id = user["localId"]
                    st.session_state.user_email = email  

                    st.success(f"✅ Login successful! Redirecting...")
                    st.switch_page("pages/journal.py")
                    
                except Exception as e:
                    error_msg = str(e)
                    if "INVALID_PASSWORD" in error_msg or "EMAIL_NOT_FOUND" in error_msg:
                        st.error("❌ Invalid email or password")
                    else:
                        st.error(f"❌ Login failed: {error_msg}")