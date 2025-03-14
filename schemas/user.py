from pydantic import BaseModel

class User(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str

class Support(BaseModel):
    url: str
    text: str

class UserResponse(BaseModel):
    data: User
    support: Support

class UserListResponse(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: list[User]
    support: Support