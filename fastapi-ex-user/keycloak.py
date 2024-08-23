# app/keycloak.py
import logging
import jwt   # PyJWT for handling JWT tokens
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID
from fastapi import Security, HTTPException, status, Depends
from pydantic import Json
from sqlalchemy.orm import Session
from .models import User
from .database import get_db


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Keycloak configuration
KEYCLOAK_SERVER_URL = "http://localhost:8080"
KEYCLOAK_REALM = "fastapi-realm"
KEYCLOAK_CLIENT_ID = "fastapi-client"
KEYCLOAK_CLIENT_SECRET = "Gbpnp5W0by7xmyuFcnIcC6GCtkPVgeXL"  # Use None for public clients
ALGORITHM = "RS256"

# Initialize KeycloakOpenID
keycloak_openid = KeycloakOpenID(
    server_url=f"{KEYCLOAK_SERVER_URL}",
    client_id=KEYCLOAK_CLIENT_ID,
    realm_name=KEYCLOAK_REALM,
    client_secret_key=KEYCLOAK_CLIENT_SECRET,
    verify=False
)
config_well_known = keycloak_openid.well_known()

oauth2_scheme = OAuth2AuthorizationCodeBearer(authorizationUrl=f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/auth", tokenUrl=f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token")

async def get_idp_public_key() -> str:
    """
    Retrieve the Identity Provider's public key from Keycloak.
    """
    return (
        "-----BEGIN PUBLIC KEY-----\n"
        f"{keycloak_openid.public_key()}"
        "\n-----END PUBLIC KEY-----"
    )

async def get_auth(token: str = Security(oauth2_scheme)) -> Json:
    """
    Validate the provided token using Keycloak's public key.
    """
    logger.info(f"Decoded token: {await get_idp_public_key()}")
    try:
        # Decode the token using Keycloak's public key
        decoded_token = keycloak_openid.decode_token(
            token
        )
        logger.info(f"Decoded token: {decoded_token}")
        return decoded_token
    except Exception as e:
        logger.error(f"Error decoding token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),  # Return the exception message as the detail
            headers={"WWW-Authenticate": "Bearer"},
        )
# Get user infos from the payload
async def get_current_user(
    identity: Json = Depends(get_auth),
    db: Session = Depends(get_db)
) -> User:
    """
    Retrieve the current user from the database using the subject identifier in the token.
    """
    try:
        # Use the subject ('sub') from the token to find the user in the database
        user: User
        user = User.first_or_fail(identity['preferred_username'], db)
        logger.info(f"user: {user}")
        return user
    except Exception as e:
        logger.error(f"Error retrieving user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
