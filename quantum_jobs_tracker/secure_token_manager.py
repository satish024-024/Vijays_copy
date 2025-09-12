"""
Secure Token Manager for IBM Quantum Authentication
Handles multiple authentication methods with secure storage
"""

import os
import json
import secrets
import hashlib
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import keyring
from flask import session, current_app
import redis
import time

class SecureTokenManager:
    """Manages secure storage and retrieval of IBM Quantum tokens"""

    def __init__(self, use_keyring=True, use_redis=False, redis_url=None):
        self.use_keyring = use_keyring and self._keyring_available()
        self.use_redis = use_redis
        self.redis_client = None

        if use_redis:
            try:
                self.redis_client = redis.from_url(redis_url or os.getenv('REDIS_URL', 'redis://localhost:6379'))
            except Exception as e:
                print(f"Redis connection failed: {e}")
                self.use_redis = False

        # Generate or load encryption key
        self.encryption_key = self._get_encryption_key()

    def _keyring_available(self):
        """Check if keyring is available"""
        try:
            import keyring
            return True
        except ImportError:
            return False

    def _get_encryption_key(self):
        """Get or generate encryption key"""
        key_file = os.path.join(os.path.dirname(__file__), '.encryption_key')

        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            # Generate new key
            salt = secrets.token_bytes(16)
            password = secrets.token_hex(32).encode()

            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password))

            # Store key securely
            with open(key_file, 'wb') as f:
                f.write(key)

            # Store password hint (not the actual password)
            with open(key_file + '.hint', 'w') as f:
                f.write(hashlib.sha256(password).hexdigest()[:16])

            return key

    def _encrypt_data(self, data):
        """Encrypt data using Fernet"""
        f = Fernet(self.encryption_key)
        json_data = json.dumps(data)
        return f.encrypt(json_data.encode()).decode()

    def _decrypt_data(self, encrypted_data):
        """Decrypt data using Fernet"""
        f = Fernet(self.encryption_key)
        decrypted = f.decrypt(encrypted_data.encode())
        return json.loads(decrypted.decode())

    def store_token(self, user_id, token_data, method='api_token'):
        """
        Store token data securely

        Args:
            user_id: Unique user identifier
            token_data: Token data dictionary
            method: Authentication method ('api_token', 'oauth', 'iam')
        """
        storage_data = {
            'token_data': token_data,
            'method': method,
            'timestamp': int(time.time()),
            'user_id': user_id
        }

        encrypted_data = self._encrypt_data(storage_data)

        # Store in multiple locations based on configuration
        if self.use_redis:
            self._store_redis(user_id, encrypted_data)
        elif self.use_keyring:
            self._store_keyring(user_id, encrypted_data)
        else:
            self._store_file(user_id, encrypted_data)

    def retrieve_token(self, user_id):
        """
        Retrieve token data securely

        Args:
            user_id: Unique user identifier

        Returns:
            Token data dictionary or None if not found
        """
        encrypted_data = None

        # Try to retrieve from storage
        if self.use_redis:
            encrypted_data = self._retrieve_redis(user_id)
        elif self.use_keyring:
            encrypted_data = self._retrieve_keyring(user_id)
        else:
            encrypted_data = self._retrieve_file(user_id)

        if not encrypted_data:
            return None

        try:
            storage_data = self._decrypt_data(encrypted_data)
            return storage_data
        except Exception as e:
            print(f"Failed to decrypt token data: {e}")
            return None

    def delete_token(self, user_id):
        """Delete stored token data"""
        if self.use_redis:
            self._delete_redis(user_id)
        elif self.use_keyring:
            self._delete_keyring(user_id)
        else:
            self._delete_file(user_id)

    def _store_redis(self, user_id, data):
        """Store in Redis"""
        key = f"quantum_token:{user_id}"
        self.redis_client.set(key, data, ex=3600*24*30)  # 30 days

    def _retrieve_redis(self, user_id):
        """Retrieve from Redis"""
        key = f"quantum_token:{user_id}"
        return self.redis_client.get(key)

    def _delete_redis(self, user_id):
        """Delete from Redis"""
        key = f"quantum_token:{user_id}"
        self.redis_client.delete(key)

    def _store_keyring(self, user_id, data):
        """Store in system keyring"""
        keyring.set_password("quantum_dashboard", user_id, data)

    def _retrieve_keyring(self, user_id):
        """Retrieve from system keyring"""
        return keyring.get_password("quantum_dashboard", user_id)

    def _delete_keyring(self, user_id):
        """Delete from system keyring"""
        try:
            keyring.delete_password("quantum_dashboard", user_id)
        except keyring.errors.PasswordDeleteError:
            pass  # Already deleted

    def _store_file(self, user_id, data):
        """Store in encrypted file"""
        filename = f".quantum_token_{hashlib.sha256(user_id.encode()).hexdigest()[:16]}"
        filepath = os.path.join(os.path.dirname(__file__), filename)

        with open(filepath, 'w') as f:
            f.write(data)

        # Set restrictive permissions
        os.chmod(filepath, 0o600)

    def _retrieve_file(self, user_id):
        """Retrieve from encrypted file"""
        filename = f".quantum_token_{hashlib.sha256(user_id.encode()).hexdigest()[:16]}"
        filepath = os.path.join(os.path.dirname(__file__), filename)

        if not os.path.exists(filepath):
            return None

        with open(filepath, 'r') as f:
            return f.read()

    def _delete_file(self, user_id):
        """Delete encrypted file"""
        filename = f".quantum_token_{hashlib.sha256(user_id.encode()).hexdigest()[:16]}"
        filepath = os.path.join(os.path.dirname(__file__), filename)

        if os.path.exists(filepath):
            os.remove(filepath)

class TokenValidator:
    """Validates and refreshes IBM Quantum tokens"""

    def __init__(self, token_manager):
        self.token_manager = token_manager

    def validate_token(self, user_id):
        """Validate if stored token is still valid"""
        token_data = self.token_manager.retrieve_token(user_id)
        if not token_data:
            return False, "No token found"

        method = token_data.get('method', 'api_token')
        token_info = token_data.get('token_data', {})

        if method == 'oauth':
            return self._validate_oauth_token(token_info)
        elif method == 'iam':
            return self._validate_iam_token(token_info)
        else:
            return self._validate_api_token(token_info)

    def _validate_oauth_token(self, token_info):
        """Validate OAuth token"""
        # Check if token is expired
        expires_at = token_info.get('expires_at', 0)
        if time.time() > expires_at:
            # Try to refresh token
            return self._refresh_oauth_token(token_info)

        return True, "Token valid"

    def _validate_iam_token(self, token_info):
        """Validate IBM Cloud IAM token"""
        # Implement IAM token validation
        expires_at = token_info.get('expires_at', 0)
        if time.time() > expires_at:
            return self._refresh_iam_token(token_info)

        return True, "IAM token valid"

    def _validate_api_token(self, token_info):
        """Validate API token by testing IBM Quantum connection"""
        try:
            # Import here to avoid circular imports
            from .real_quantum_app import QuantumBackendManager

            token = token_info.get('token')
            if not token:
                return False, "No API token found"

            # Test connection
            manager = QuantumBackendManager(token)
            if manager.is_connected():
                return True, "API token valid"
            else:
                return False, "API token invalid"

        except Exception as e:
            return False, f"Token validation failed: {str(e)}"

    def _refresh_oauth_token(self, token_info):
        """Refresh OAuth token"""
        try:
            from .oauth_auth import IBMQuantumOAuth

            oauth = IBMQuantumOAuth()
            refresh_token = token_info.get('refresh_token')

            if not refresh_token:
                return False, "No refresh token available"

            new_token_data = oauth.refresh_token(refresh_token)

            # Update stored token
            user_id = token_info.get('user_id')
            if user_id:
                self.token_manager.store_token(user_id, new_token_data, 'oauth')

            return True, "Token refreshed"

        except Exception as e:
            return False, f"Token refresh failed: {str(e)}"

    def _refresh_iam_token(self, token_info):
        """Refresh IBM Cloud IAM token"""
        # Implement IAM token refresh
        return False, "IAM token refresh not implemented"

# Flask integration
def init_token_manager(app):
    """Initialize token manager for Flask app"""
    if not hasattr(app, 'token_manager'):
        # Configure based on environment
        use_redis = os.getenv('USE_REDIS', 'false').lower() == 'true'
        redis_url = os.getenv('REDIS_URL')

        app.token_manager = SecureTokenManager(
            use_keyring=not use_redis,  # Use keyring if not using Redis
            use_redis=use_redis,
            redis_url=redis_url
        )

    if not hasattr(app, 'token_validator'):
        app.token_validator = TokenValidator(app.token_manager)

    return app.token_manager, app.token_validator

# Convenience functions for Flask routes
def get_user_token(user_id=None):
    """Get user's token from secure storage"""
    if not current_app or not hasattr(current_app, 'token_manager'):
        return None

    if user_id is None:
        user_id = session.get('user_id')

    if not user_id:
        return None

    token_data = current_app.token_manager.retrieve_token(user_id)
    if token_data:
        return token_data.get('token_data', {}).get('token')

    return None

def store_user_token(user_id, token_data, method='api_token'):
    """Store user's token securely"""
    if not current_app or not hasattr(current_app, 'token_manager'):
        return False

    current_app.token_manager.store_token(user_id, token_data, method)
    return True

def validate_user_token(user_id=None):
    """Validate user's stored token"""
    if not current_app or not hasattr(current_app, 'token_validator'):
        return False, "Token manager not initialized"

    if user_id is None:
        user_id = session.get('user_id')

    if not user_id:
        return False, "No user ID"

    return current_app.token_validator.validate_token(user_id)

if __name__ == '__main__':
    # Test the token manager
    manager = SecureTokenManager(use_keyring=False, use_redis=False)

    # Test data
    test_user = "test_user_123"
    test_token_data = {
        'token': 'test_ibm_quantum_token',
        'expires_at': int(time.time()) + 3600,
        'user_info': {'name': 'Test User'}
    }

    # Store token
    manager.store_token(test_user, test_token_data, 'api_token')
    print("Token stored successfully")

    # Retrieve token
    retrieved = manager.retrieve_token(test_user)
    if retrieved:
        print(f"Token retrieved: {retrieved['token_data']['token'][:20]}...")
    else:
        print("Token retrieval failed")

    # Delete token
    manager.delete_token(test_user)
    print("Token deleted successfully")
