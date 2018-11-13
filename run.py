# run a test server
from api import create_app, db
from config import DevelopmentConfig
from api.models import Todo

app = create_app(DevelopmentConfig)

app.run(host='127.0.0.1', port=8080, debug=True)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Todo': Todo}