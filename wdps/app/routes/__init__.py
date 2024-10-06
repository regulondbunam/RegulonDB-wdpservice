from .main_routes import main_bp
from .meme_routes import meme_bp

def init_app(app):
    # Registrar blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(meme_bp)