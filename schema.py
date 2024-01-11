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
