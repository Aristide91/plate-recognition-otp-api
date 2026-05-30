from fastapi import APIRouter, Depends
from app.core.security import get_current_user

router = APIRouter()

@router.get("/me", summary="Get current user information", response_model=dict)
async def read_current_user(current_user: dict = Depends(get_current_user)):
    """
    Retrieve details of the authenticated user.
    This endpoint requires a valid Keycloak JWT token.
    """
    return current_user
