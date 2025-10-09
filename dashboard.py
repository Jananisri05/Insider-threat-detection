import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import bcrypt
import datetime
import time
import random
import requests
from PIL import Image
from io import BytesIO

# Database connection
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# Create users table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
""")
conn.commit()

# Streamlit UI Setup
st.set_page_config(page_title="Cyber Forensic Dashboard", page_icon="", layout="wide")

# Apply Cyberpunk Design
cyber_css = """
    
    <style>
    body {
        background-color: #121212;
        color: white;
        font-family: 'Courier New', monospace;
    }
    .stApp {
        background-color: #0d0d0d;
        color: white;
    }
    .stSidebar, .stSidebarContent {
        background-color: #1a1a1a;
        border-right: 3px solid cyan;
        color: white !important;
    }
    .stSidebar .css-1d391kg, .stSidebarContent .css-1d391kg {
        color: white !important;
    }
    .stButton > button {
        background-color: cyan !important;
        color: black !important;
        border-radius: 10px;
        padding: 8px;
        font-size: 16px;
    }
    .stTextInput > div > div > input {
        background-color: #333;
        color: white;
        border: 2px solid cyan;
        border-radius: 5px;
    }
    .stDataFrame {
        background-color: black;
        color: white;
        border: 2px solid cyan;
        font-size: 14px;
    }
    </style>
"""


st.markdown(cyber_css, unsafe_allow_html=True)

# Sidebar Navigation
menu = st.sidebar.radio(" Navigation", ["Login", "Sign Up", "Admin Dashboard", "User Dashboard", "Settings"])

# Password Hashing Functions
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# Login Page
if menu == "Login":
    st.title(" Login to Your Account")
    username = st.text_input(" Username")
    password = st.text_input(" Password", type="password")
    
    if st.button(" Login"):
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        
        if user and check_password(password, user[2]):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["role"] = user[3]
            st.success(f" Logged in as {username} ({user[3]})")
        else:
            st.error(" Invalid username or password")

# Sign-up Page
elif menu == "Sign Up":
    st.title(" Create a New Account")
    new_user = st.text_input(" Username")
    new_password = st.text_input(" Password", type="password")
    role = st.selectbox(" Role", ["user", "admin"])
    
    if st.button(" Register"):
        hashed_password = hash_password(new_password)
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (new_user, hashed_password, role))
            conn.commit()
            st.success(" Account created successfully! Please login.")
        except:
            st.error("️ Username already exists.")

# Admin Dashboard
elif menu == "Admin Dashboard":
    if "logged_in" in st.session_state and st.session_state["role"] == "admin":
        st.title(" Cyber Admin Dashboard")
        st.subheader(" Suspicious Activities Detected")

        # Simulated user activity data
        user_activity_data = {
            "user_id": ["user1", "user2", "user3", "user4"],
            "typing_speed": [50, 80, 30, 100],
            "suspicious_score": ["Low", "Moderate", "High", "Critical"]
        }
        df = pd.DataFrame(user_activity_data)

        # Color-coding
        df["Color Code"] = df["suspicious_score"].map({
            "Low": "#2ECC71",  # Green
            "Moderate": "#F1C40F",  # Yellow
            "High": "#E67E22",  # Orange
            "Critical": "#E74C3C"  # Red
        })

        st.dataframe(df.style.applymap(lambda x: f'background-color: {df.loc[df.index[df["suspicious_score"] == x].tolist(), "Color Code"].values[0]};', subset=["suspicious_score"]))

        # Visualization
        fig = px.bar(df, x="user_id", y="typing_speed", color="suspicious_score", title="User Activity Suspiciousness")
        st.plotly_chart(fig)

    else:
        st.warning(" You must be an admin to access this page.")

# User Dashboard
elif menu == "User Dashboard":
    if "logged_in" in st.session_state and st.session_state["role"] == "user":
        st.title(" Cyber User Dashboard")
        st.write(f"Welcome, {st.session_state['username']}!")

        # User Typing Analysis
        st.subheader("️ Type in the Box Below")
        user_input = st.text_area("Start typing here...", height=150)

        if user_input:
            start_time = time.time()
            words_typed = len(user_input.split())
            typing_speed = words_typed / (time.time() - start_time) * 60  # Words per minute
            
            st.write(f"Your typing speed: {typing_speed:.2f} WPM")

            # Suspiciousness detection
            if typing_speed < 40:
                suspicion = "Low"
            elif typing_speed < 70:
                suspicion = "Moderate"
            elif typing_speed < 100:
                suspicion = "High"
            else:
                suspicion = "Critical"

            st.write(f"Suspicion Level: {suspicion}")

            # Meme Generation
            meme_dict = {
                "slow": "https://i.imgflip.com/1bij.jpg",  
                "fast": "https://i.imgflip.com/30b1gx.jpg",
                "moderate": "https://i.imgflip.com/26am.jpg"
            }

            meme_url = meme_dict["slow"] if typing_speed < 40 else meme_dict["fast"] if typing_speed > 80 else meme_dict["moderate"]
            response = requests.get(meme_url)
            img = Image.open(BytesIO(response.content))
            st.image(img, caption="Your typing speed meme")

    else:
        st.warning(" You must be logged in to access this page.")

# Settings Page
elif menu == "Settings":
    if "logged_in" in st.session_state:
        st.title("️ Cyber Settings")
        st.write(f"Welcome, {st.session_state['username']}!")

        # Change Password
        st.subheader(" Change Password")
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")

        if st.button("Update Password"):
            cursor.execute("SELECT password FROM users WHERE username=?", (st.session_state['username'],))
            stored_password = cursor.fetchone()[0]

            if check_password(current_password, stored_password):
                hashed_new_password = hash_password(new_password)
                cursor.execute("UPDATE users SET password=? WHERE username=?", (hashed_new_password, st.session_state['username']))
                conn.commit()
                st.success(" Password updated successfully!")
            else:
                st.error(" Incorrect current password.")

    else:
        st.warning(" You must be logged in to access this page.")
