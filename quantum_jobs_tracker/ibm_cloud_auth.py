"""
IBM Cloud Authentication Policy for DataPower API Gateway
Implements the ibm-cloud-authentication policy v1.0.0 for watsonx.ai
"""

import os
import json
import time
import requests
from flask import Flask, request, session, jsonify, redirect, url_for, render_template
from urllib.parse import urlencode
import secrets

class IBMCloudAuthPolicy:
    """IBM Cloud Authentication Policy v1.0.0 for DataPower API Gateway"""

    def __init__(self, watsonx_api_key=None, version="1.0.0", title="ibm-cloud-authentication", description=""):
        # Policy configuration
        self.version = version
        self.title = title
        self.description = description

        # watsonx.ai API key for authentication
        self.watsonx_api_key = watsonx_api_key or os.getenv('WATSONX_API_KEY')

        # IBM Cloud endpoints for authentication
        self.token_url = "https://iam.cloud.ibm.com/identity/token"
        self.watsonx_url = "https://us-south.ml.cloud.ibm.com"

        # Token cache (simulates DataPower caching)
        self.token_cache = {}
        self.cache_expiry = {}  # Track token expiry times
        self.token_lifetime = 3600  # 60 minutes as per policy spec

        # Policy state
        self.policy_enabled = True
        self.last_refresh = None

    def authenticate_and_get_token(self, watsonx_api_key=None):
        """
        Authenticate with IBM Cloud and obtain Bearer token for watsonx.ai

        Args:
            watsonx_api_key: watsonx.ai API key (if not set in constructor)

        Returns:
            dict: Token information with Bearer token
        """
        if watsonx_api_key:
            self.watsonx_api_key = watsonx_api_key

        if not self.watsonx_api_key:
            raise ValueError("watsonx.ai API key is required for authentication")

        # Check if we have a valid cached token
        cache_key = self._get_cache_key(self.watsonx_api_key)
        if self._is_token_valid(cache_key):
            print(f"✅ Using cached token for watsonx.ai API key")
            return self.token_cache[cache_key]

        # Get new token from IBM Cloud
        print(f"🔄 Obtaining new Bearer token for watsonx.ai")
        token_data = self._get_ibm_cloud_token()

        # Cache the token
        self._cache_token(cache_key, token_data)

        return token_data

    def _get_ibm_cloud_token(self):
        """
        Get Bearer token from IBM Cloud IAM using watsonx.ai API key

        Returns:
            dict: Token data with Bearer token
        """
        if not self.watsonx_api_key:
            raise ValueError("watsonx.ai API key is required")

        # Prepare IAM authentication request for watsonx.ai
        data = {
            'grant_type': 'urn:ibm:params:oauth:grant-type:apikey',
            'apikey': self.watsonx_api_key
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }

        try:
            response = requests.post(self.token_url, data=data, headers=headers, timeout=30)

            if response.status_code == 200:
                token_response = response.json()

                # Format as Bearer token for watsonx.ai
                return {
                    'access_token': token_response.get('access_token'),
                    'token_type': 'Bearer',
                    'expires_in': token_response.get('expires_in', self.token_lifetime),
                    'scope': token_response.get('scope', 'watsonx.ai'),
                    'issued_at': time.time(),
                    'policy_version': self.version,
                    'watsonx_ready': True
                }
            else:
                error_msg = f"IBM Cloud authentication failed: {response.status_code}"

                if response.status_code == 401:
                    error_msg += "\n\n❌ INVALID API KEY"
                    error_msg += "\n• Check if your watsonx.ai API key is correct"
                    error_msg += "\n• Make sure it's a watsonx.ai API key (not IBM Quantum)"
                    error_msg += "\n• Verify the key hasn't expired"
                elif response.status_code == 403:
                    error_msg += "\n\n🚫 INSUFFICIENT PERMISSIONS"
                    error_msg += "\n• Your API key might not have watsonx.ai access"
                    error_msg += "\n• Check if you have the right service permissions"
                elif response.status_code == 404:
                    error_msg += "\n\n🔍 SERVICE NOT FOUND"
                    error_msg += "\n• watsonx.ai service might not be available in your region"
                    error_msg += "\n• Check your watsonx.ai URL configuration"
                elif response.status_code >= 500:
                    error_msg += "\n\n🔧 IBM CLOUD SERVER ERROR"
                    error_msg += "\n• IBM Cloud might be experiencing issues"
                    error_msg += "\n• Try again in a few minutes"

                error_msg += f"\n\n📄 Response: {response.text}"
                raise ValueError(error_msg)

        except requests.RequestException as e:
            error_msg = f"Network connection failed: {str(e)}"
            if "CERTIFICATE" in str(e).upper():
                error_msg += "\n\n🔧 SSL Certificate Issue: Try updating certificates or use HTTP instead"
            elif "TIMEOUT" in str(e).upper():
                error_msg += "\n\n⏱️ Connection Timeout: IBM Cloud might be temporarily unavailable"
            elif "CONNECTION" in str(e).upper():
                error_msg += "\n\n🌐 Network Issue: Check your internet connection"
            raise ValueError(error_msg)

    def _get_cache_key(self, api_key):
        """Generate cache key for API key"""
        import hashlib
        return hashlib.sha256(api_key.encode()).hexdigest()[:16]

    def _is_token_valid(self, cache_key):
        """Check if cached token is still valid"""
        if cache_key not in self.token_cache:
            return False

        if cache_key not in self.cache_expiry:
            return False

        # Check if token is expired (with 5-minute buffer)
        return time.time() < (self.cache_expiry[cache_key] - 300)

    def _cache_token(self, cache_key, token_data):
        """Cache the Bearer token"""
        self.token_cache[cache_key] = token_data

        # Set expiry time (token lifetime from policy spec)
        expires_in = token_data.get('expires_in', self.token_lifetime)
        self.cache_expiry[cache_key] = time.time() + expires_in

        self.last_refresh = time.time()
        print(f"💾 Cached Bearer token for watsonx.ai (expires in {expires_in} seconds)")

    def refresh_token_if_needed(self, watsonx_api_key):
        """Refresh token if expired or about to expire"""
        cache_key = self._get_cache_key(watsonx_api_key)

        if not self._is_token_valid(cache_key):
            print(f"🔄 Token expired or about to expire, refreshing...")
            token_data = self._get_ibm_cloud_token()
            self._cache_token(cache_key, token_data)
            return token_data

        return self.token_cache[cache_key]

    def get_policy_info(self):
        """Get policy information"""
        return {
            'version': self.version,
            'title': self.title,
            'description': self.description,
            'gateway_support': 'DataPower® API Gateway',
            'token_lifetime': self.token_lifetime,
            'cached_tokens': len(self.token_cache),
            'last_refresh': self.last_refresh
        }

    def clear_cache(self):
        """Clear all cached tokens (useful for testing or policy updates)"""
        self.token_cache.clear()
        self.cache_expiry.clear()
        self.last_refresh = None
        print("🗑️ Cleared all cached tokens")

    def get_authorization_url(self, state=None):
        """Generate professional authorization URL"""
        if not state:
            state = self.generate_state()

        # Store state for later verification
        self.sessions[state] = {
            'timestamp': time.time(),
            'status': 'pending'
        }

        # For professional IBM Cloud auth, we'll redirect to our own login page
        # that looks like IBM Cloud's login page
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': 'openid cloud_platform watsonx',
            'state': state
        }

        return f"/ibm-cloud/professional-login?{urlencode(params)}", state

    def show_professional_login_page(self, state, client_id, redirect_uri):
        """Show a professional login page that looks like IBM Cloud"""
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>IBM Cloud - Sign In</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}

                body {{
                    font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }}

                .login-container {{
                    background: white;
                    border-radius: 12px;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
                    padding: 40px;
                    width: 100%;
                    max-width: 400px;
                    position: relative;
                    overflow: hidden;
                }}

                .login-container::before {{
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 4px;
                    background: linear-gradient(90deg, #1e40af, #3b82f6, #06b6d4, #10b981);
                    background-size: 300% 300%;
                    animation: gradientShift 3s ease infinite;
                }}

                @keyframes gradientShift {{
                    0%, 100% {{ background-position: 0% 50%; }}
                    50% {{ background-position: 100% 50%; }}
                }}

                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}

                .ibm-cloud-logo {{
                    width: 60px;
                    height: 60px;
                    background: linear-gradient(135deg, #1e40af, #3b82f6);
                    border-radius: 12px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0 auto 20px;
                    color: white;
                    font-size: 30px;
                    font-weight: bold;
                }}

                .header h1 {{
                    color: #0f172a;
                    font-size: 24px;
                    font-weight: 600;
                    margin-bottom: 8px;
                }}

                .header p {{
                    color: #64748b;
                    font-size: 14px;
                }}

                .form-group {{
                    margin-bottom: 20px;
                }}

                .form-group label {{
                    display: block;
                    color: #374151;
                    font-size: 14px;
                    font-weight: 500;
                    margin-bottom: 6px;
                }}

                .form-group input {{
                    width: 100%;
                    padding: 12px 16px;
                    border: 2px solid #e2e8f0;
                    border-radius: 8px;
                    font-size: 16px;
                    transition: all 0.3s ease;
                }}

                .form-group input:focus {{
                    outline: none;
                    border-color: #3b82f6;
                    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
                }}

                .login-btn {{
                    width: 100%;
                    padding: 14px;
                    background: linear-gradient(135deg, #1e40af, #3b82f6);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    margin-bottom: 20px;
                }}

                .login-btn:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px rgba(30, 64, 175, 0.3);
                }}

                .login-btn:disabled {{
                    opacity: 0.6;
                    cursor: not-allowed;
                    transform: none;
                }}

                .divider {{
                    text-align: center;
                    margin: 20px 0;
                    position: relative;
                    color: #64748b;
                    font-size: 14px;
                }}

                .divider::before {{
                    content: '';
                    position: absolute;
                    top: 50%;
                    left: 0;
                    right: 0;
                    height: 1px;
                    background: #e2e8f0;
                }}

                .divider span {{
                    background: white;
                    padding: 0 16px;
                    position: relative;
                    z-index: 1;
                }}

                .guest-btn {{
                    width: 100%;
                    padding: 12px;
                    background: #f8fafc;
                    color: #475569;
                    border: 2px solid #e2e8f0;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: 500;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }}

                .guest-btn:hover {{
                    background: #e2e8f0;
                    border-color: #cbd5e1;
                }}

                .back-link {{
                    text-align: center;
                    margin-top: 20px;
                }}

                .back-link a {{
                    color: #3b82f6;
                    text-decoration: none;
                    font-size: 14px;
                }}

                .back-link a:hover {{
                    text-decoration: underline;
                }}

                .loading {{
                    display: none;
                    text-align: center;
                    color: #64748b;
                    font-size: 14px;
                }}

                .loading.show {{
                    display: block;
                }}

                .professional-notice {{
                    background: #eff6ff;
                    border: 1px solid #dbeafe;
                    border-radius: 6px;
                    padding: 12px;
                    margin-bottom: 20px;
                    font-size: 13px;
                    color: #1e40af;
                }}

                .professional-notice strong {{
                    color: #1e293b;
                }}
            </style>
        </head>
        <body>
            <div class="login-container">
                <div class="header">
                    <div class="ibm-cloud-logo">☁️</div>
                    <h1>IBM Cloud</h1>
                    <p>Sign in to your account</p>
                </div>

                <div class="professional-notice">
                    <strong>🔒 Enterprise Authentication</strong><br>
                    Your credentials are securely managed by IBM Cloud's authentication system.
                </div>

                <form id="loginForm" method="post" action="/ibm-cloud/professional-authenticate">
                    <input type="hidden" name="state" value="{state}">
                    <input type="hidden" name="client_id" value="{client_id}">
                    <input type="hidden" name="redirect_uri" value="{redirect_uri}">

                    <div class="form-group">
                        <label for="email">IBM Cloud Email or IBMid</label>
                        <input type="email" id="email" name="email" required
                               placeholder="your.email@ibm.com">
                    </div>

                    <div class="form-group">
                        <label for="password">Password</label>
                        <input type="password" id="password" name="password" required
                               placeholder="Enter your IBM Cloud password">
                    </div>

                    <button type="submit" class="login-btn" id="loginBtn">
                        <span id="loginText">Sign In to IBM Cloud</span>
                    </button>

                    <div id="loading" class="loading">
                        Authenticating with IBM Cloud...
                    </div>
                </form>

                <div class="divider">
                    <span>or</span>
                </div>

                <button class="guest-btn" onclick="guestLogin()">
                    Continue with Guest Access
                </button>

                <div class="back-link">
                    <a href="/auth">← Back to authentication options</a>
                </div>
            </div>

            <script>
                const loginForm = document.getElementById('loginForm');
                const loginBtn = document.getElementById('loginBtn');
                const loginText = document.getElementById('loginText');
                const loading = document.getElementById('loading');

                loginForm.addEventListener('submit', function(e) {{
                    loginBtn.disabled = true;
                    loginText.style.display = 'none';
                    loading.classList.add('show');
                }});

                function guestLogin() {{
                    // Redirect to guest authentication
                    window.location.href = '/ibm-cloud/guest-authenticate?state={state}&client_id={client_id}&redirect_uri={redirect_uri}';
                }}
            </script>
        </body>
        </html>
        """

    def authenticate_user(self, email, password, state):
        """Simulate professional IBM Cloud authentication"""
        # In production, this would validate against IBM Cloud's authentication system
        # For demo purposes, we'll accept any email/password combination

        if not email or not password:
            raise ValueError("Email and password are required")

        # Generate mock tokens
        access_token = secrets.token_hex(32)
        refresh_token = secrets.token_hex(32)

        # Store authentication state
        auth_code = self.generate_auth_code()
        self.pending_auth[auth_code] = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'email': email,
            'timestamp': time.time(),
            'state': state,
            'cloud_account': f"IBM Cloud Account ({email.split('@')[0]})"
        }

        return auth_code

    def guest_authenticate(self, state):
        """Handle guest authentication for IBM Cloud"""
        # Generate mock tokens for guest access
        access_token = secrets.token_hex(32)
        refresh_token = secrets.token_hex(32)

        # Store authentication state
        auth_code = self.generate_auth_code()
        self.pending_auth[auth_code] = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'email': 'guest@ibmcloud.com',
            'timestamp': time.time(),
            'state': state,
            'guest': True,
            'cloud_account': 'IBM Cloud Guest Access'
        }

        return auth_code

    def exchange_code_for_token(self, code, state, redirect_uri):
        """Exchange authorization code for tokens"""
        if code not in self.pending_auth:
            raise ValueError("Invalid authorization code")

        auth_data = self.pending_auth[code]

        # Verify state
        if auth_data['state'] != state:
            raise ValueError("State mismatch")

        # Clean up pending auth
        del self.pending_auth[code]

        # Return token data
        return {
            'access_token': auth_data['access_token'],
            'refresh_token': auth_data['refresh_token'],
            'token_type': 'Bearer',
            'expires_in': 3600,
            'scope': 'openid cloud_platform watsonx quantum_computing',
            'account_info': {
                'email': auth_data['email'],
                'account_name': auth_data['cloud_account'],
                'guest': auth_data.get('guest', False)
            }
        }

    def get_user_info(self, access_token):
        """Get user information"""
        # Mock user info - in production this would come from IBM Cloud
        return {
            'sub': 'ibm_cloud_user123',
            'email': 'user@ibmcloud.com',
            'name': 'IBM Cloud User',
            'preferred_username': 'ibm_cloud_user',
            'accounts': ['IBM Cloud Account']
        }

    def get_quantum_token(self, access_token):
        """Get IBM Quantum API token from IBM Cloud token"""
        # In production, this would exchange the IBM Cloud token for an IBM Quantum API token
        # For demo, we'll return a mock token
        return secrets.token_hex(32)

class IBMCloudServiceIDAuth:
    """Authentication using IBM Cloud Service IDs"""

    def __init__(self, service_id=None, api_key=None):
        self.service_id = service_id or os.getenv('IBM_CLOUD_SERVICE_ID')
        self.api_key = api_key or os.getenv('IBM_CLOUD_SERVICE_API_KEY')
        self.iam = IBMCloudIAM()

    def authenticate(self):
        """
        Authenticate using Service ID credentials

        Returns:
            dict: Token information
        """
        if not self.api_key:
            raise ValueError("Service ID API key is required")

        # Service IDs use the same IAM authentication flow
        return self.iam.authenticate(api_key=self.api_key)

    def get_quantum_token(self):
        """
        Get IBM Quantum token for Service ID

        Returns:
            str: IBM Quantum API token
        """
        token_data = self.authenticate()
        return self.iam.get_quantum_token(token_data['access_token'])

# Flask routes for IBM Cloud Authentication Policy
def setup_ibm_cloud_auth_policy(app, policy_handler):
    @app.route('/ibm-cloud/policy/authenticate', methods=['POST'])
    def ibm_cloud_policy_authenticate():
        """IBM Cloud Authentication Policy endpoint"""
        try:
            # Get watsonx.ai API key from request
            data = request.get_json() or request.form
            watsonx_api_key = data.get('apikey') or data.get('watsonx_api_key')

            if not watsonx_api_key:
                return jsonify({
                    'error': 'API key is required',
                    'policy_version': policy_handler.version,
                    'gateway': 'DataPower® API Gateway'
                }), 400

            # Authenticate and get Bearer token
            token_data = policy_handler.authenticate_and_get_token(watsonx_api_key)

            # Return Bearer token for watsonx.ai requests
            return jsonify({
                'access_token': token_data['access_token'],
                'token_type': token_data['token_type'],
                'expires_in': token_data['expires_in'],
                'scope': token_data['scope'],
                'policy_version': token_data['policy_version'],
                'watsonx_ready': token_data['watsonx_ready'],
                'issued_at': token_data['issued_at']
            })

        except ValueError as e:
            return jsonify({
                'error': str(e),
                'policy_version': policy_handler.version
            }), 401
        except Exception as e:
            return jsonify({
                'error': f'Authentication policy failed: {str(e)}',
                'policy_version': policy_handler.version
            }), 500

    @app.route('/ibm-cloud/policy/info')
    def ibm_cloud_policy_info():
        """Get IBM Cloud Authentication Policy information"""
        return jsonify(policy_handler.get_policy_info())

    @app.route('/ibm-cloud/policy/cache/clear', methods=['POST'])
    def ibm_cloud_policy_clear_cache():
        """Clear token cache (admin function)"""
        try:
            policy_handler.clear_cache()
            return jsonify({
                'success': True,
                'message': 'Token cache cleared',
                'policy_version': policy_handler.version
            })
        except Exception as e:
            return jsonify({
                'error': f'Failed to clear cache: {str(e)}',
                'policy_version': policy_handler.version
            }), 500

    @app.route('/ibm-cloud/policy/health')
    def ibm_cloud_policy_health():
        """Health check for IBM Cloud Authentication Policy"""
        return jsonify({
            'status': 'healthy' if policy_handler.policy_enabled else 'disabled',
            'policy_version': policy_handler.version,
            'gateway_support': 'DataPower® API Gateway',
            'watsonx_integration': True,
            'token_cache_size': len(policy_handler.token_cache),
            'last_refresh': policy_handler.last_refresh
        })

    @app.route('/ibm-cloud/policy/refresh', methods=['POST'])
    def ibm_cloud_policy_refresh():
        """Manually refresh token for API key"""
        try:
            data = request.get_json() or request.form
            watsonx_api_key = data.get('apikey') or data.get('watsonx_api_key')

            if not watsonx_api_key:
                return jsonify({
                    'error': 'API key is required for token refresh',
                    'policy_version': policy_handler.version
                }), 400

            # Refresh token
            token_data = policy_handler.refresh_token_if_needed(watsonx_api_key)

            return jsonify({
                'success': True,
                'access_token': token_data['access_token'],
                'token_type': token_data['token_type'],
                'expires_in': token_data['expires_in'],
                'refreshed_at': time.time(),
                'policy_version': policy_handler.version
            })

        except Exception as e:
            return jsonify({
                'error': f'Token refresh failed: {str(e)}',
                'policy_version': policy_handler.version
            }), 500

    @app.route('/watsonx/authenticate', methods=['POST'])
    def watsonx_authenticate():
        """watsonx.ai authentication endpoint using IBM Cloud policy"""
        try:
            # Get watsonx.ai API key
            data = request.get_json() or request.form
            watsonx_api_key = data.get('apikey') or data.get('watsonx_api_key')

            if not watsonx_api_key:
                return jsonify({
                    'error': 'watsonx.ai API key is required',
                    'service': 'watsonx.ai',
                    'policy': 'ibm-cloud-authentication'
                }), 400

            # Get Bearer token using IBM Cloud Authentication Policy
            try:
                token_data = policy_handler.authenticate_and_get_token(watsonx_api_key)
            except Exception as e:
                error_message = str(e)
                if "BXNIM0415E" in error_message or "Provided API key could not be found" in error_message:
                    return jsonify({
                        'success': False,
                        'error': 'Invalid watsonx.ai API key',
                        'details': 'The provided API key could not be found in IBM Cloud. Please check your watsonx.ai API key.',
                        'error_code': 'BXNIM0415E',
                        'suggestions': [
                            'Verify your watsonx.ai API key is correct',
                            'Make sure you are using a watsonx.ai API key (not IBM Quantum)',
                            'Check if the key has expired or been revoked',
                            'Ensure you have access to watsonx.ai services'
                        ]
                    }), 400
                elif "CredWrite" in error_message or "stub received bad data" in error_message:
                    return jsonify({
                        'success': False,
                        'error': 'Windows credential storage error',
                        'details': 'Unable to save credentials to Windows Credential Manager. This is a Windows system issue.',
                        'error_code': 'CREDWRITE_ERROR',
                        'suggestions': [
                            'Try running the application as Administrator',
                            'Check Windows Credential Manager permissions',
                            'Use the "Skip Authentication" option below to continue with sample data',
                            'Restart the application and try again'
                        ]
                    }), 400
                else:
                    return jsonify({
                        'success': False,
                        'error': 'watsonx.ai authentication failed',
                        'details': error_message,
                        'suggestions': [
                            'Check your watsonx.ai API key',
                            'Verify your IBM Cloud account has watsonx.ai access',
                            'Try refreshing the page and entering the key again',
                            'Use the "Skip Authentication" option to continue with sample data'
                        ]
                    }), 400

            # Store authentication in Flask session (server-side)
            import secrets
            user_id = secrets.token_hex(16)
            session['user_id'] = user_id
            session['auth_method'] = 'watsonx_policy'
            session['quantum_token'] = token_data['access_token']
            session['watsonx_token'] = token_data['access_token']
            session['watsonx_expires'] = time.time() + token_data['expires_in']
            session['watsonx_url'] = policy_handler.watsonx_url
            session['policy_version'] = token_data['policy_version']

            # Store securely using the token manager
            from secure_token_manager import store_user_token
            token_store_data = {
                'token': token_data['access_token'],
                'watsonx_token': token_data['access_token'],
                'expires_at': time.time() + token_data['expires_in'],
                'watsonx_url': policy_handler.watsonx_url,
                'policy_version': token_data['policy_version'],
                'service': 'watsonx.ai'
            }
            store_user_token(user_id, token_store_data, 'watsonx_policy')

            print(f"✅ watsonx.ai authentication successful for user {user_id}")

            # Return watsonx.ai ready authentication
            return jsonify({
                'success': True,
                'bearer_token': token_data['access_token'],
                'token_type': token_data['token_type'],
                'expires_in': token_data['expires_in'],
                'watsonx_url': policy_handler.watsonx_url,
                'service': 'watsonx.ai',
                'policy': 'ibm-cloud-authentication',
                'policy_version': token_data['policy_version'],
                'ready_for_watsonx': token_data['watsonx_ready'],
                'redirect': '/dashboard'
            })

        except ValueError as e:
            return jsonify({
                'error': str(e),
                'service': 'watsonx.ai',
                'policy': 'ibm-cloud-authentication'
            }), 401
        except Exception as e:
            return jsonify({
                'error': f'watsonx.ai authentication failed: {str(e)}',
                'service': 'watsonx.ai',
                'policy': 'ibm-cloud-authentication'
            }), 500

def test_watsonx_api_key(api_key):
    """
    Test watsonx.ai API key validity before using in application

    Args:
        api_key (str): watsonx.ai API key to test

    Returns:
        dict: Test result with success/failure and details
    """
    if not api_key or len(api_key.strip()) == 0:
        return {
            'success': False,
            'error': 'API key is empty',
            'guidance': 'Please provide a valid watsonx.ai API key'
        }

    # Test API key format (should start with certain patterns)
    if not (api_key.startswith('WATSONX_') or api_key.startswith('watsonx_') or len(api_key) >= 40):
        return {
            'success': False,
            'error': 'Invalid API key format',
            'guidance': 'watsonx.ai API keys should be at least 40 characters long'
        }

    # Try to authenticate
    policy = IBMCloudAuthPolicy(watsonx_api_key=api_key)

    try:
        token_data = policy.authenticate_and_get_token(api_key)
        return {
            'success': True,
            'message': '✅ watsonx.ai API key is valid!',
            'token_type': token_data.get('token_type'),
            'expires_in': token_data.get('expires_in'),
            'watsonx_url': token_data.get('watsonx_url')
        }
    except ValueError as e:
        return {
            'success': False,
            'error': str(e),
            'guidance': 'Check your API key and watsonx.ai service access'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}',
            'guidance': 'Please try again or contact support'
        }


if __name__ == '__main__':
    # Example usage
    iam = IBMCloudIAM(
        api_key='your_ibm_cloud_api_key',
        account_id='your_account_id'
    )

    app = Flask(__name__)
    app.secret_key = secrets.token_hex(32)

    setup_ibm_cloud_routes(app, iam)
    app.run(debug=True, port=5000)
