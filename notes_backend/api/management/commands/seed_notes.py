from django.core.management.base import BaseCommand
from api.models import Note


class Command(BaseCommand):
    help = "Seed the database with a few sample notes for development."

    # PUBLIC_INTERFACE
    def handle(self, *args, **options):
        """Create a handful of sample notes if none exist."""
        if Note.objects.exists():
            self.stdout.write(self.style.WARNING("Notes already exist. Skipping seeding."))
            return

        samples = [
            {"title": "Welcome to Notes", "content": "This is your first note. Feel free to edit or delete it.", "tags": "welcome,intro"},
            {"title": "Shopping List", "content": "- Milk\n- Bread\n- Eggs", "tags": "personal,shopping"},
            {"title": "Ideas", "content": "1. Build a notes app\n2. Add reminders", "tags": "ideas,work"},
        ]
        for data in samples:
            Note.objects.create(**data)

        self.stdout.write(self.style.SUCCESS("Seeded sample notes successfully."))
