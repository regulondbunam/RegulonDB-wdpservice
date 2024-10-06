from flask import Blueprint, request, jsonify
from .graphql_service import execute_graphql_query

def setup_routes(app):
    main = Blueprint('main', __name__)
    
    @main.route('/api/data', methods=['GET'])
    def get_data():
        # Define tu consulta GraphQL
        graphql_query = """
        query {
            someData {
                field1
                field2
            }
        }
        """
        try:
            # Ejecuta la consulta GraphQL
            data = execute_graphql_query(graphql_query)
            # Procesa el resultado según sea necesario y retorna al cliente REST
            return jsonify(data)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    app.register_blueprint(main)