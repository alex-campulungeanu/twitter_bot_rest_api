from app.views.MainView import main as main_blueprint
from app.views.UserView import user_api as user_blueprint
from app.views.PostView import post_api as post_blueprint
from app.views.twitter.TwitterView import twitter_api as twitter_blueprint
from app.views.ErrorsView import errors as errors_blueprint

def register_blueprint_view(app):
    app.register_blueprint(main_blueprint, url_prefix='/api')
    app.register_blueprint(errors_blueprint)
    app.register_blueprint(user_blueprint, url_prefix='/api')
    app.register_blueprint(post_blueprint, url_prefix='/api')
    app.register_blueprint(twitter_blueprint, url_prefix='/api/twitter')