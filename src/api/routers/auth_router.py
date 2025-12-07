"""Authentication router for signup and login endpoints."""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.api.schemas.auth_schema import UserCreate, UserLogin, Token, UserOut
from src.api.dependencies.auth_dep import get_db, get_current_user
from src.models.tables import User
from src.api.utils.auth import hash_password, verify_password, create_access_token
from src.api.utils.api_logging import log_api_call

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=Token)
@log_api_call("user_signup")
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    Returns JWT token on successful signup.
    """
    # Check if username already exists
    existing = db.query(User).filter(User.username == payload.username).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )

    # Check if email already exists (if provided)
    if payload.email:
        existing_email = db.query(User).filter(User.email == payload.email).first()
        if existing_email:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

    # Create new user
    user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Generate JWT token
    token = create_access_token(subject=user.id)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
@log_api_call("user_login")
def login(payload: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and issue JWT token.
    """
    # Find user by username
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Generate JWT token
    token = create_access_token(subject=user.id)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
@log_api_call("get_current_user")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user info."""
    return UserOut(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        created_at=current_user.created_at.isoformat()
    )
