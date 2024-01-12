import strawberry
from strawberry.tools import merge_types
from strawberry.permission import PermissionExtension

from services.note import NoteService
from services.authentication import AuthenticationService

from middleware.JWTBearer import IsAuthenticated

from schema import (
    NoteInput,
    NoteServiceReturnType,
    NoteType,
    RegisterInput,
    LoginInput,
    LoginType,
    ServiceReturnType,
)


@strawberry.type
class NotesMutation:
    @strawberry.mutation(
        extensions=[
            PermissionExtension(permissions=[IsAuthenticated()], fail_silently=False),
        ]
    )
    async def create(self, note_input: NoteInput) -> NoteType:
        return await NoteService.add_note(note_input)

    @strawberry.mutation(
        extensions=[
            PermissionExtension(permissions=[IsAuthenticated()], fail_silently=False)
        ]
    )
    async def update_note(
        self, note_id: int, note_input: NoteInput
    ) -> NoteServiceReturnType:
        return await NoteService.update_note(note_id, note_input)

    @strawberry.mutation(
        extensions=[
            PermissionExtension(permissions=[IsAuthenticated()], fail_silently=False)
        ]
    )
    async def delete_note(self, note_id: int) -> NoteServiceReturnType:
        return await NoteService.delete_note(note_id)


@strawberry.type
class UserMutation:
    @strawberry.mutation
    async def login(self, credentials: LoginInput) -> LoginType:
        return await AuthenticationService.login(credentials)

    @strawberry.mutation
    async def register(self, user_data: RegisterInput) -> ServiceReturnType:
        return await AuthenticationService.register(user_data)


Mutation = merge_types("Mutation", (NotesMutation, UserMutation))
