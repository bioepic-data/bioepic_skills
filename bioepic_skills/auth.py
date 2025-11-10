# -*- coding: utf-8 -*-
import requests
from datetime import datetime, timedelta
from bioepic_skills.api_base import APIBase
import logging

logger = logging.getLogger(__name__)


class BioEPICAuth(APIBase):
    """
    Authentication handler for BioEPIC API operations.

    You must provide either:
      - client_id and client_secret (for client credentials grant), OR
      - username and password (for password grant).

    Parameters
    ----------
    client_id : str
        The client ID for BioEPIC API authentication (required if using client credentials grant).
    client_secret : str
        The client secret for BioEPIC API authentication (required if using client credentials grant).
    username : str
        The username for BioEPIC API authentication (required if using password grant).
    password : str
        The password for BioEPIC API authentication (required if using password grant).

    Notes
    -----
    Security Warning: Your client_id and client_secret should be stored in a secure location.
        We recommend using environment variables.
        Do not hard code these values in your code.
    """

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        username: str | None = None,
        password: str | None = None,
        env: str = "prod",
    ):
        super().__init__(env=env)
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.token = None
        self.token_expiry = None

    def has_credentials(self) -> bool:
        """Check if the credentials are passed in properly."""
        has_client_creds = self.client_id is not None and self.client_secret is not None
        has_user_creds = self.username is not None and self.password is not None
        return has_client_creds or has_user_creds

    def get_token(self) -> str:
        """Get a valid access token, refreshing if necessary."""
        if self.token and self._is_token_valid():
            return self.token
        return self._refresh_token()

    def _is_token_valid(self) -> bool:
        """Check if current token is valid and not expired."""
        if not self.token or not self.token_expiry:
            return False
        # Add a 5-minute buffer before expiry
        return datetime.now() < (self.token_expiry - timedelta(minutes=5))

    def _refresh_token(self) -> str:
        """Refresh the access token."""
        url = f"{self.base_url}/token"
        
        if self.client_id and self.client_secret:
            # Client credentials grant
            data = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }
        elif self.username and self.password:
            # Password grant
            data = {
                "grant_type": "password",
                "username": self.username,
                "password": self.password,
            }
        else:
            raise ValueError("No valid credentials provided")

        try:
            response = requests.post(url, data=data)
            response.raise_for_status()
            token_data = response.json()
            self.token = token_data["access_token"]
            # Assuming token includes expires_in field in seconds
            expires_in = token_data.get("expires_in", 3600)
            self.token_expiry = datetime.now() + timedelta(seconds=expires_in)
            logging.debug("Token refreshed successfully")
            return self.token
        except requests.exceptions.RequestException as e:
            logger.error("Failed to refresh token", exc_info=True)
            raise RuntimeError("Failed to authenticate with BioEPIC API") from e
