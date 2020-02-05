from app import create_app, db
from app.models import Channel, Video, Task

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Channel': Channel, 'Video': Video, 'Task': Task}