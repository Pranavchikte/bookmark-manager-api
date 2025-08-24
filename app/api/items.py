from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Item, User
import mongoengine.errors as errors

items_bp = Blueprint('items', __name__, url_prefix='/api/items')

# Handles creating items
@items_bp.route('/', methods=['POST'])
@jwt_required()
def create_item():
    user_id = get_jwt_identity()
    body = request.get_json()
    
    # Validate required fields
    if not body:
        return jsonify({"error": "Request body is required"}), 400
    
    required_fields = ['title', 'item_type', 'content']
    for field in required_fields:
        if not body.get(field):
            return jsonify({"error": f"'{field}' is required"}), 400
    
    try: 
        new_item = Item(
            owner=user_id,
            title=body.get('title'),
            item_type=body.get('item_type'),
            content=body.get('content'),
            tags=body.get('tags', [])
        )
        new_item.save()
        return jsonify(new_item.to_dict()), 201
    except errors.ValidationError as e:
        return jsonify({"error": f"Validation error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Handles fetching items
@items_bp.route('/', methods=['GET'])
@jwt_required()
def get_items():
    user_id = get_jwt_identity()
    search_term = request.args.get('search', None)
    item_type = request.args.get('type', None)
    sort_by = request.args.get('sort', None)
    
    try:
        query = Item.objects(owner=user_id)
        
        if search_term:
            # Fixed typo: icontain -> icontains
            query = query.filter(title__icontains=search_term)
            
        if item_type and item_type != 'all':
            query = query.filter(item_type=item_type)
            
        if sort_by:
            if sort_by == 'title_asc':
                query = query.order_by('title')
            elif sort_by == 'title_desc':
                query = query.order_by('-title')
            elif sort_by == 'date_asc':
                query = query.order_by('created_at')
            else:
                query = query.order_by('-created_at')
        else:
            query = query.order_by('-created_at')
            
        result = [item.to_dict() for item in query]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Handles deleting a specific item
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
    except errors.DoesNotExist:
        return jsonify({"error": "Item not found"}), 404
    except errors.ValidationError:
        return jsonify({"error": "Invalid item ID"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Handles updating a specific item
@items_bp.route('/<item_id>', methods=['PUT'])
@jwt_required()
def update_item(item_id):
    user_id = get_jwt_identity()
    body = request.get_json()
    
    if not body:
        return jsonify({"error": "Request body is required"}), 400
    
    try:
        item_to_update = Item.objects(id=item_id, owner=user_id).first()
        if not item_to_update:
            return jsonify({"error": "Item not found"}), 404
            
        # Filter out None values and only update provided fields
        update_data = {k: v for k, v in body.items() if v is not None}
        if update_data:
            item_to_update.update(**update_data)
            updated_item = item_to_update.reload()
            return jsonify(updated_item.to_dict()), 200
        else:
            return jsonify({"error": "No valid fields to update"}), 400
            
    except errors.DoesNotExist:
        return jsonify({"error": "Item not found"}), 404
    except errors.ValidationError as e:
        return jsonify({"error": f"Validation error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500