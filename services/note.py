from schema import NoteInput, NoteType, NoteServiceReturnType

from repository.note import NoteRepository

from models.note import Note


class NoteService:
    @staticmethod
    async def add_note(note_data: NoteInput):
        note = Note(name=note_data.name, description=note_data.description)
        await NoteRepository.create(note)

        return NoteType(id=note.id, name=note.name, description=note.description)

    @staticmethod
    async def get_all_notes():
        notes = await NoteRepository.get_all()

        return [
            NoteType(id=note.id, name=note.name, description=note.description)
            for note in notes
        ]

    @staticmethod
    async def get_note(note_id: int):
        note = await NoteRepository.get_by_id(note_id)
        return (
            NoteType(id=note.id, name=note.name, description=note.description)
            if note
            else None
        )

    @staticmethod
    async def update_note(note_id: int, note_data: NoteInput):
        note = Note(name=note_data.name, description=note_data.description)
        await NoteRepository.update(note_id, note)
        return NoteServiceReturnType(
            success=True, message=f"Succesfully updated: {note_id}"
        )

    @staticmethod
    async def delete_note(note_id: int):
        await NoteRepository.delete(note_id)
        return NoteServiceReturnType(
            success=True, message=f"Succesfully deleted: {note_id}"
        )
