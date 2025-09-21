"""
IBM Quantum Authentication Integration
Complete integration of multiple authentication methods into Flask application
"""

import os
from flask import Flask, request, session, redirect, url_for, render_template, jsonify
from oauth_auth import IBMQuantumOAuth, setup_oauth_routes
from ibm_cloud_auth import IBMCloudIAM, setup_ibm_cloud_routes
from secure_token_manager import init_token_manager, get_user_token, store_user_token, validate_user_token
import secrets

class QuantumAuthManager:
    """Unified authentication manager for multiple IBM Quantum auth methods"""

    def __init__(self, app=None):
        self.app = app
        self.oauth_handler = None
        self.ibm_cloud_handler = None

        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize authentication handlers for Flask app"""

        # Initialize secure token manager
        token_manager, token_validator = init_token_manager(app)

        # Initialize OAuth handler
        self.oauth_handler = IBMQuantumOAuth(
            client_id=os.getenv('IBM_QUANTUM_CLIENT_ID'),
            client_secret=os.getenv('IBM_QUANTUM_CLIENT_SECRET'),
            redirect_uri=os.getenv('IBM_QUANTUM_REDIRECT_URI', f'http://localhost:{app.config.get("PORT", 10000)}/oauth/callback')
        )

        # Initialize IBM Cloud IAM handler
        self.ibm_cloud_handler = IBMCloudIAM(
            api_key=os.getenv('IBM_CLOUD_API_KEY'),
            account_id=os.getenv('IBM_CLOUD_ACCOUNT_ID')
        )

        # Setup all authentication routes
        self._setup_routes(app)

        # Store handlers in app for access by other modules
        app.quantum_auth = self
        app.oauth_handler = self.oauth_handler
        app.ibm_cloud_handler = self.ibm_cloud_handler

    def _setup_routes(self, app):
        """Setup all authentication routes"""

        @app.route('/auth')
        def auth_selection():
            """Main authentication method selection page"""
            return render_template('multi_auth.html')

        @app.route('/token-input')
        def token_input():
            """API token input page"""
            return render_template('token_input.html')

        @app.route('/auth/status')
        def auth_status():
            """Check authentication status"""
            user_id = session.get('user_id', 'anonymous')

            # Check if user has valid token
            is_valid, message = validate_user_token(user_id)

            auth_method = session.get('auth_method', 'none')
            quantum_token = get_user_token(user_id)

            return jsonify({
                'authenticated': is_valid,
                'auth_method': auth_method,
                'message': message,
                'has_token': quantum_token is not None,
                'user_id': user_id
            })

        # Setup OAuth routes
        setup_oauth_routes(app, self.oauth_handler)

        # Setup IBM Cloud routes
        setup_ibm_cloud_routes(app, self.ibm_cloud_handler)

        # Enhanced token handling
        @app.route('/api/set-token', methods=['POST'])
        def api_set_token():
            """Enhanced API endpoint for setting tokens"""
            try:
                data = request.get_json()
                if not data or 'token' not in data:
                    return jsonify({'error': 'Token is required'}), 400

                token = data['token'].strip()
                if not token:
                    return jsonify({'error': 'Token cannot be empty'}), 400

                # Generate user ID if not exists
                if 'user_id' not in session:
                    session['user_id'] = secrets.token_hex(16)

                user_id = session['user_id']

                # Store token securely
                token_data = {
                    'token': token,
                    'method': 'api_token',
                    'expires_at': None  # API tokens don't expire
                }

                success = store_user_token(user_id, token_data, 'api_token')
                if success:
                    session['auth_method'] = 'api_token'
                    session['quantum_token'] = token
                    return jsonify({
                        'success': True,
                        'message': 'Token stored successfully',
                        'auth_method': 'api_token'
                    })
                else:
                    return jsonify({'error': 'Failed to store token'}), 500

            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @app.route('/auth/logout')
        def auth_logout():
            """Unified logout endpoint"""
            user_id = session.get('user_id')

            # Clear token from secure storage
            if user_id:
                from secure_token_manager import SecureTokenManager
                manager = SecureTokenManager()
                manager.delete_token(user_id)

            # Clear session
            session.clear()

            return redirect('/auth')

    def get_current_token(self):
        """Get the current user's IBM Quantum token"""
        user_id = session.get('user_id')
        if not user_id:
            return None

        return get_user_token(user_id)

    def require_auth(self, f):
        """Decorator to require authentication"""
        def decorated_function(*args, **kwargs):
            user_id = session.get('user_id')
            if not user_id:
                return redirect('/auth')

            # Validate token
            is_valid, message = validate_user_token(user_id)
            if not is_valid:
                return redirect('/auth')

            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function

def create_app_with_auth():
    """Create Flask app with full authentication integration"""
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(32)

    # Initialize authentication
    auth_manager = QuantumAuthManager(app)

    @app.route('/')
    def index():
        """Main dashboard - requires authentication"""
        return auth_manager.require_auth(lambda: render_template('index.html'))()

    @app.route('/dashboard')
    def dashboard():
        """Dashboard page - requires authentication"""
        return auth_manager.require_auth(lambda: render_template('hackathon_dashboard.html'))()

    @app.route('/api/quantum-data')
    def quantum_data():
        """API endpoint that requires authentication"""
        token = auth_manager.get_current_token()
        if not token:
            return jsonify({'error': 'Authentication required'}), 401

        # Your quantum data logic here
        return jsonify({
            'success': True,
            'data': 'Quantum data here',
            'token_preview': token[:20] + '...' if token else None
        })

    return app

# Integration helper functions
def integrate_auth_into_existing_app(app, quantum_manager=None):
    """
    Integrate authentication into an existing Flask app

    Args:
        app: Existing Flask application
        quantum_manager: Optional quantum manager instance
    """
    # Initialize authentication
    auth_manager = QuantumAuthManager(app)

    # Add authentication middleware
    @app.before_request
    def check_auth():
        # Skip auth check for static files, auth routes, and API status
        if (request.path.startswith('/static/') or
            request.path.startswith('/auth') or
            request.path == '/api/auth/status' or
            request.path in ['/oauth/login', '/oauth/callback', '/ibm-cloud/login', '/ibm-cloud/auth']):
            return

        # Require auth for dashboard routes
        if request.path in ['/', '/dashboard', '/api/quantum-data']:
            user_id = session.get('user_id')
            if not user_id:
                return redirect('/auth')

            is_valid, _ = validate_user_token(user_id)
            if not is_valid:
                return redirect('/auth')

    # Add quantum token to quantum manager if provided
    if quantum_manager:
        @app.before_request
        def update_quantum_manager():
            if hasattr(session, 'quantum_token'):
                token = auth_manager.get_current_token()
                if token:
                    quantum_manager.connect_with_token(token)

    return auth_manager

# Environment setup helper
def setup_environment_variables():
    """Setup environment variables for different authentication methods"""
    env_vars = {}

    # OAuth configuration
    env_vars['IBM_QUANTUM_CLIENT_ID'] = os.getenv('IBM_QUANTUM_CLIENT_ID', 'your_oauth_client_id')
    env_vars['IBM_QUANTUM_CLIENT_SECRET'] = os.getenv('IBM_QUANTUM_CLIENT_SECRET', 'your_oauth_client_secret')
    env_vars['IBM_QUANTUM_REDIRECT_URI'] = os.getenv('IBM_QUANTUM_REDIRECT_URI', 'http://localhost:10000/oauth/callback')

    # IBM Cloud configuration
    env_vars['IBM_CLOUD_API_KEY'] = os.getenv('IBM_CLOUD_API_KEY', 'your_ibm_cloud_api_key')
    env_vars['IBM_CLOUD_ACCOUNT_ID'] = os.getenv('IBM_CLOUD_ACCOUNT_ID', 'your_account_id')

    # Token storage configuration
    env_vars['USE_REDIS'] = os.getenv('USE_REDIS', 'false')
    env_vars['REDIS_URL'] = os.getenv('REDIS_URL', 'redis://localhost:6379')

    return env_vars

if __name__ == '__main__':
    # Create app with authentication
    app = create_app_with_auth()

    # Setup environment
    env_vars = setup_environment_variables()
    print("Environment variables configured:")
    for key, value in env_vars.items():
        if 'SECRET' in key or 'KEY' in key:
            print(f"  {key}: {'*' * len(value) if value != 'your_' + key.split('_')[-1].lower() else value}")
        else:
            print(f"  {key}: {value}")

    print("\nStarting Flask app with authentication...")
    print("Visit http://localhost:10000/auth to choose authentication method")

    app.run(debug=True, port=10000)
