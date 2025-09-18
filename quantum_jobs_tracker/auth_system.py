"""
Simple JWT-based authentication system for Quantum Jobs Tracker
Handles user registration, login, and token management
"""

import jwt
import hashlib
import sqlite3
import time
from datetime import datetime, timedelta
from flask import request, jsonify, session
import secrets

class AuthSystem:
    def __init__(self, secret_key=None):
        self.secret_key = secret_key or secrets.token_hex(32)
        self.db_path = "quantum_data.db"
        self.init_user_table()
    
    def init_user_table(self):
        """Initialize users table in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                api_key TEXT NOT NULL,
                crn TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password, password_hash):
        """Verify password against hash"""
        return self.hash_password(password) == password_hash
    
    def generate_token(self, user_id, email):
        """Generate JWT token for user"""
        payload = {
            'user_id': user_id,
            'email': email,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token):
        """Verify JWT token and return user data"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def register_user(self, email, password, api_key, crn):
        """Register a new user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Check if user already exists
            cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
            if cursor.fetchone():
                return False, "User already exists"
            
            # Hash password
            password_hash = self.hash_password(password)
            
            # Insert new user
            cursor.execute('''
                INSERT INTO users (email, password_hash, api_key, crn)
                VALUES (?, ?, ?, ?)
            ''', (email, password_hash, api_key, crn))
            
            user_id = cursor.lastrowid
            conn.commit()
            
            return True, f"User registered successfully with ID: {user_id}"
            
        except Exception as e:
            return False, f"Registration failed: {str(e)}"
        finally:
            conn.close()
    
    def login_user(self, email, password):
        """Login user and return token"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get user data
            cursor.execute('''
                SELECT id, email, password_hash, api_key, crn 
                FROM users WHERE email = ?
            ''', (email,))
            
            user = cursor.fetchone()
            if not user:
                return False, "User not found", None, None, None
            
            user_id, user_email, password_hash, api_key, crn = user
            
            # Verify password
            if not self.verify_password(password, password_hash):
                return False, "Invalid password", None, None, None
            
            # Update last login
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
            ''', (user_id,))
            conn.commit()
            
            # Generate token
            token = self.generate_token(user_id, user_email)
            
            return True, "Login successful", token, api_key, crn
            
        except Exception as e:
            return False, f"Login failed: {str(e)}", None, None, None
        finally:
            conn.close()
    
    def get_user_credentials(self, user_id):
        """Get user's API key and CRN"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT api_key, crn FROM users WHERE id = ?', (user_id,))
            result = cursor.fetchone()
            if result:
                return result[0], result[1]
            return None, None
        finally:
            conn.close()

# Global auth system instance
auth_system = AuthSystem()
