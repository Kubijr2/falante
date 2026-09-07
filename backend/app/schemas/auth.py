from pydantic import BaseModel, ConfigDict


class GoogleAuthRequest(BaseModel):
    id_token: str


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    name: str
    picture_url: str | None
    dashboard_widgets: list[str]


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead
