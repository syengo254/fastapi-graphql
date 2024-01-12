from typing import List, Optional
import strawberry

from schema import NoteType

from services.note import NoteService

from middleware.JWTBearer import IsAuthenticated


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello graphql fast api!"

    @strawberry.field(
        extensions=[
            strawberry.permission.PermissionExtension(
                permissions=[IsAuthenticated()], fail_silently=False
            )
        ]
    )
    async def get_all(self) -> List[NoteType]:
        return await NoteService.get_all_notes()

    @strawberry.field(
        extensions=[
            strawberry.permission.PermissionExtension(
                permissions=[IsAuthenticated()], fail_silently=False
            )
        ]
    )
    async def get_by_id(self, note_id: int) -> Optional[NoteType]:
        return await NoteService.get_note(note_id)
