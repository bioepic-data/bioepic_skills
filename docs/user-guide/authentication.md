# Authentication

BioEPIC Skills provides a robust authentication system for accessing protected API endpoints.

## Overview

The `BioEPICAuth` class handles authentication with the API, supporting both client credentials and username/password authentication methods.

## Authentication Methods

### Client Credentials

Recommended for server-to-server authentication:

```python
from bioepic_skills.auth import BioEPICAuth

auth = BioEPICAuth(
    client_id="your_client_id",
    client_secret="your_client_secret",
    env="prod"
)
```

### Username and Password

For user-based authentication:

```python
auth = BioEPICAuth(
    username="your_username",
    password="your_password",
    env="prod"
)
```

## Using Environment Variables

**Best Practice:** Store credentials in environment variables:

### Setup .env File

Create a `.env` file:

```bash
# .env
ENV=prod
CLIENT_ID=your_client_id_here
CLIENT_SECRET=your_client_secret_here
```

### Load and Use

```python
import os
from dotenv import load_dotenv
from bioepic_skills.auth import BioEPICAuth

# Load environment variables
load_dotenv()

# Initialize with environment variables
auth = BioEPICAuth(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    env=os.getenv("ENV", "prod")
)
```

## Token Management

The authentication system automatically manages tokens:

### Getting a Token

```python
# Get or refresh token automatically
token = auth.get_token()
print(f"Token: {token[:20]}...")  # Show first 20 chars
```

### Check Credentials

```python
if auth.has_credentials():
    print("Credentials are configured")
    token = auth.get_token()
else:
    print("No credentials found")
```

### Token Expiry

Tokens are automatically refreshed when needed:

- Tokens are cached until they expire
- A 5-minute buffer before expiry triggers automatic refresh
- You don't need to manually manage token lifecycle

## Using the @requires_auth Decorator

Protect methods that require authentication:

```python
from bioepic_skills.decorators import requires_auth
from bioepic_skills.auth import BioEPICAuth

class MyAPIClient:
    def __init__(self, auth: BioEPICAuth):
        self.auth = auth
    
    @requires_auth
    def protected_method(self):
        """This method requires authentication"""
        token = self.auth.get_token()
        # Use token in API call...
        pass
```

## Error Handling

### Authentication Errors

```python
from bioepic_skills.decorators import AuthenticationError

try:
    auth = BioEPICAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET")
    )
    
    if not auth.has_credentials():
        raise AuthenticationError("No credentials provided")
    
    token = auth.get_token()
    
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except RuntimeError as e:
    print(f"Token refresh failed: {e}")
```

## Complete Example

```python
import os
import logging
from dotenv import load_dotenv
from bioepic_skills.auth import BioEPICAuth
from bioepic_skills.api_search import APISearch

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def main():
    # Initialize authentication
    auth = BioEPICAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        env=os.getenv("ENV", "prod")
    )
    
    # Verify credentials
    if not auth.has_credentials():
        logger.error("No credentials found. Check your .env file.")
        return
    
    logger.info("Authentication initialized")
    
    # Get token
    try:
        token = auth.get_token()
        logger.info("Token acquired successfully")
    except RuntimeError as e:
        logger.error(f"Failed to get token: {e}")
        return
    
    # Use with API client
    api_client = APISearch(collection_name="samples")
    # Make authenticated requests...
    
if __name__ == "__main__":
    main()
```

## Security Best Practices

### 1. Never Hardcode Credentials

❌ **Don't do this:**

```python
auth = BioEPICAuth(
    client_id="abc123",  # Hardcoded!
    client_secret="secret456"  # Hardcoded!
)
```

✅ **Do this:**

```python
auth = BioEPICAuth(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET")
)
```

### 2. Keep .env Files Secure

- Add `.env` to `.gitignore`
- Never commit `.env` files to version control
- Use `.env.example` as a template

### 3. Use Different Credentials for Different Environments

```python
# Development
auth_dev = BioEPICAuth(
    client_id=os.getenv("DEV_CLIENT_ID"),
    client_secret=os.getenv("DEV_CLIENT_SECRET"),
    env="dev"
)

# Production
auth_prod = BioEPICAuth(
    client_id=os.getenv("PROD_CLIENT_ID"),
    client_secret=os.getenv("PROD_CLIENT_SECRET"),
    env="prod"
)
```

### 4. Rotate Credentials Regularly

Establish a process for regular credential rotation, especially for production environments.

## Troubleshooting

### "No credentials found" Error

Check that:
1. `.env` file exists in your project root
2. Environment variables are properly set
3. You're calling `load_dotenv()` before accessing credentials

### Token Refresh Failures

If token refresh fails:
1. Verify your credentials are still valid
2. Check network connectivity to the auth endpoint
3. Ensure the auth endpoint URL is correct in `api_base.py`

### Invalid Credentials

If you receive authentication errors:
1. Verify credentials in your account dashboard
2. Ensure you're using the correct environment (prod vs dev)
3. Check that credentials haven't expired

## API Reference

For detailed API documentation, see:

- [BioEPICAuth API](../api/auth.md)
- [Decorators API](../api/auth.md#decorators)
