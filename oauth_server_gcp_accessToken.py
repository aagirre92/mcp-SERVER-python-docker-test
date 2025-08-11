"""
Run from the repository root:
    uv run examples/snippets/servers/oauth_server.py
"""
import os
from pydantic import AnyHttpUrl
import requests
from dotenv import load_dotenv
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings
from mcp.server.fastmcp import FastMCP
# from fastmcp import FastMCP  # Ensure you have the correct import for FastMCP
# Load environment variables from .env file
load_dotenv()

GOOGLE_ISSUER = "https://accounts.google.com"
GCP_OAUTH_CLIENT_ID = os.getenv("GCP_OAUTH_CLIENT_ID")  # Must match your OAuth client ID

class SimpleTokenVerifier(TokenVerifier):
    """Simple token verifier for demonstration.
    Docu url: https://gofastmcp.com/python-sdk/fastmcp-server-auth-providers-in_memory#verify-token
    """

    async def verify_token(self, token: str) -> AccessToken | None:
        print(f"Verifying token: {token}")
        gcp_access_token_verification_url = f"https://oauth2.googleapis.com/tokeninfo?access_token={token}"
        response = requests.get(gcp_access_token_verification_url)
        #response.raise_for_status()
        token_info = response.json()

        if token_info.get("error") == "invalid_token":
            print("🚨 Invalid token received from Google OAuth.")
            return None
        
        if token_info.get("aud") == os.getenv("GCP_OAUTH_CLIENT_ID"):
            access_token = AccessToken(
                token=token,
                client_id=token_info.get("aud"),
                scopes=token_info.get("scope", "").split(), # split function splits scopes by space (default)
                expires_at=token_info.get("exp"),
            )
            print(f"✅Token verified successfully: {access_token}")
            # Return the access token if verification is successful
        
            return access_token
        else:
            print("Invalid token or audience mismatch.")
            return None
        # Here you would implement the actual token verification logic
        pass  # This is where you would implement actual token validation


# Create FastMCP instance as a Resource Server (with from mcp.server.fastmcp import FastMCP)

mcp = FastMCP(
    "Weather Service",
    # Token verifier for authentication
    token_verifier=SimpleTokenVerifier(),
    # Auth settings for RFC 9728 Protected Resource Metadata
    auth=AuthSettings(
        issuer_url=AnyHttpUrl(GOOGLE_ISSUER),  # Authorization Server URL
        resource_server_url=AnyHttpUrl(f"http://localhost:{os.getenv('PORT', 8000)}"),  # This server's URL
        required_scopes=["openid"],
    ),
)


@mcp.tool()
async def get_weather(city: str = "London") -> dict[str, str]:
    """Get weather data for a city"""
    return {
        "city": city,
        "temperature": "22",
        "condition": "Partly cloudy",
        "humidity": "65%",
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")