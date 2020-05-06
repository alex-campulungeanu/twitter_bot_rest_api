##craete app with function
# import os

# from app import create_app

# env_name = os.getenv('FLASK_ENV', 'default')
# app = create_app(env_name)

from app import app

if __name__ == '__main__':
    app.run()