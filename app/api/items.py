from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Item,User
import mongoengine.errors as errors

items_bp = Blueprint('items', __name__, url_prefix='/api/items')

@items_bp.route('/', methods=['POST'])
@jwt_required()
def create_item():
    user_id = get_jwt_identity()
    body = request.get_json()
    
    try: 
        new_item = Item(
            owner = user_id,
            title=body.get('title'),
            item_type=body.get('item_type'),
            content=body.get('content'),
            tags=body.get('tags',[])
        )
        new_item.save()
        return jsonify(new_item.to_dict()), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@items_bp.route('/', methods=['GET'])
@jwt_required()
def get_items():
    user_id = get_jwt_identity()
    
    try:
        items = Item.objects(owner=user_id)
        result = [item.to_dict() for item in items]
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@items_bp.route('/<item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(item_id):
    user_id = get_jwt_identity()
    
    try: 
        item_to_delete = Item.objects(id=item_id, owner=user_id).first()
        
        if item_to_delete:
            item_to_delete.delete()
            return jsonify({"msg": "Item deleted successfully"}), 200
        
        else:
            return jsonify({"error": "Item not found"}), 404
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@items_bp.route('/<item_id>', methods=['PUT'])
@jwt_required()
def update_item(item_id):
    user_id = get_jwt_identity()
    body = request.get_json()

    try:
        item_to_update = Item.objects(id=item_id, owner=user_id).first()

        if not item_to_update:
            return jsonify({"error": "Item not found"}), 404

        item_to_update.update(**body)

        updated_item = Item.objects(id=item_id).first()

        return jsonify(updated_item.to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500