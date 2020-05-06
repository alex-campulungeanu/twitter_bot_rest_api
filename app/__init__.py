import os

##The enviroments needs to be loaded first !!!
from pathlib import Path
from dotenv import load_dotenv
env_name = os.getenv('FLASK_ENV')
if env_name == 'production':
    env_path = Path('.') / '.env.production'
elif env_name == 'development':
    env_path = Path('.') / '.env.development'
else:
    env_path = Path('.') / '.env.development'

load_dotenv(dotenv_path=env_path, verbose=True)


from flask import Flask

from app.config import app_config, setup_logger
from flask_migrate import Migrate
from flask_mail import Mail

migrate = Migrate()
mail = Mail()

# basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config.from_object(app_config[env_name])

app.logger.info(f"Run app with env:  {env_name}")

# Set up extensions
from app.models import db, ma
db.init_app(app)
ma.init_app(app)
migrate.init_app(app, db)
mail.init_app(app)

# Set up logging
setup_logger(app)

from app.views import register_blueprint_view
register_blueprint_view(app)

from app.commands import register_commands
register_commands(app)