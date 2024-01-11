from typing import List, Optional
import strawberry

from schema import NoteType

from services.note import NoteService


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello graphql fast api!"

    @strawberry.field
    async def get_all(self) -> List[NoteType]:
        return await NoteService.get_all_notes()

    @strawberry.field
    async def get_by_id(self, note_id: int) -> Optional[NoteType]:
        return await NoteService.get_note(note_id)
