from flask import Blueprint, jsonify

users_blueprint = Blueprint("users", __name__, url_prefix="/users", template_folder="templates")
from . import models, tasks

@app.route('/get_name', methods=['GET'])
@jwt_required()
def get_name():
    # Extract the user ID from the JWT
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    # Check if user exists
    if user:
        return jsonify({'message': 'User found', 'name': user.name})
    else:
        return jsonify({'message': 'User not found'}), 404
 