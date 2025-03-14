from pydantic import BaseModel

class AuthRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    token: str

class AuthErrorResponse(BaseModel):
    error: str
