import strawberry


@strawberry.type
class NoteType:
    id: int
    name: str
    description: str


@strawberry.type
class NoteServiceReturnType:
    success: bool
    message: str


@strawberry.input
class NoteInput:
    name: str
    description: str


@strawberry.type
class UserType:
    id: int
    name: str
    email: str


@strawberry.input
class RegisterInput:
    name: str
    email: str
    password: str


@strawberry.input
class LoginInput:
    email: str
    password: str


@strawberry.type
class LoginType:
    email: str
    token: str


@strawberry.type
class ServiceReturnType:
    success: bool
    message: str
