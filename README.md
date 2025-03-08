## How it's Working Flask with JWT 

### Overview
This project demonstrates JWT (JSON Web Token) authentication in a Flask application with a JavaScript frontend.

### Key Components

#### Backend (Flask)
- Uses `flask-jwt-extended` for JWT implementation
- Implements 4 main routes:
  - `/` - Home route
  - `/login` - Authentication endpoint
  - `/dashboard` - Protected route requiring valid JWT
  - `/refresh` - Endpoint to refresh expired access tokens
- Configures JWT with:
  - 5 minute access token expiry
  - 24 hour refresh token expiry
  - Random secret keys for security

#### Frontend (JavaScript)
- Handles user authentication flow:
  - Login form submission
  - Token storage in localStorage
  - Protected API calls with JWT headers
  - Automatic token refresh on expiry
- Key functions:
  - `login()` - Handles authentication
  - `get_dashboard()` - Makes authenticated requests
  - `refresh_token()` - Handles token refresh flow

### Important Implementation Details

1. Two-Token System
   - Access Token (Short-lived - 5 mins)
   - Refresh Token (Long-lived - 24 hours)

2. Security Features
   - Random secret keys generated on startup
   - Token expiration handling
   - Secure token storage in localStorage

3. Error Handling
   - Invalid credentials handling
   - Token expiration detection
   - Automatic token refresh
   - Graceful error messaging

4. Best Practices
   - Bearer token authentication scheme
   - Proper HTTP methods (GET/POST)
   - Content-Type headers
   - Separation of concerns (frontend/backend)

### Flow
1. User submits login credentials
2. Server validates username and password and returns access + refresh tokens
3. Frontend stores tokens in localStorage
4. Protected requests include access token
5. On access_token expiry, refresh token used to get new access token
6. If refresh token expires, user must login again
