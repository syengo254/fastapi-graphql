import strawberry

from services.note import NoteService
from schema import NoteInput, NoteServiceReturnType, NoteType


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create(self, note_input: NoteInput) -> NoteType:
        return await NoteService.add_note(note_input)

    @strawberry.mutation
    async def update_note(
        self, note_id: int, note_input: NoteInput
    ) -> NoteServiceReturnType:
        return await NoteService.update_note(note_id, note_input)

    @strawberry.mutation
    async def delete_note(self, note_id: int) -> NoteServiceReturnType:
        return await NoteService.delete_note(note_id)
