from flask import Flask
from .routes import init_app 
from flask_graphql import GraphQLView
from .schema import schema

def create_app():
    app = Flask(__name__)

    # Inicializa las rutas
    init_app(app)

    # Descomentar esta línea si necesitas habilitar la interfaz GraphiQL
    """app.add_url_rule(
        '/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
    )"""

    return app