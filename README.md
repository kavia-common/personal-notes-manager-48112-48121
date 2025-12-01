# personal-notes-manager-48112-48121

Backend: Django + Django REST Framework

Quickstart
- Install dependencies (handled by environment).
- Run migrations:
  - cd notes_backend
  - python manage.py makemigrations
  - python manage.py migrate
- Seed sample data (optional):
  - python manage.py seed_notes
- Run server:
  - python manage.py runserver 0.0.0.0:3001

API Docs
- Swagger UI: /docs
- ReDoc: /redoc
- OpenAPI JSON: /swagger.json

Health
- GET /api/health/

Notes CRUD
- List notes (with pagination and filters):
  curl -s "http://localhost:3001/api/notes/?page=1&search=note&is_archived=false"
- Create note:
  curl -s -X POST "http://localhost:3001/api/notes/" -H "Content-Type: application/json" -d '{"title":"New","content":"Body"}'
- Retrieve note:
  curl -s "http://localhost:3001/api/notes/1/"
- Update note:
  curl -s -X PATCH "http://localhost:3001/api/notes/1/" -H "Content-Type: application/json" -d '{"title":"Updated"}'
- Delete note:
  curl -s -X DELETE "http://localhost:3001/api/notes/1/"
- Archive note:
  curl -s -X POST "http://localhost:3001/api/notes/1/archive/"
- Unarchive note:
  curl -s -X POST "http://localhost:3001/api/notes/1/unarchive/"

Query Params
- search: substring on title
- is_archived: true/false
- Pagination: page (default DRF page size 10)

Notes
- CORS enabled for development (allow all origins)
- Uses SQLite by default; no external services needed
