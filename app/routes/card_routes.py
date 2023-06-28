from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card

# create blueprint
card_bp = Blueprint("card_bp", __name__, url_prefix="/cards")

# DELETE /cards/<card_id>
# Delete a card from given board
@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    # validate card
    card = validate_item(Card, card_id)
    
    # delete card and commit delete
    db.session.delete(card)
    db.session.commit()
    
    # return delete message
    return {"details": f'Card id {card.card_id} successfully deleted'}

# PUT /cards/<card_id>/like
# Update likes in card
@card_bp.route("/<card_id>/like", methods=["PUT"])
def update_like(card_id):
    # validate card
    card = validate_item(Card, card_id)
    
    # get request data
    request_data = request.get_json()
    
    # update card w/ new likes
    card.likes_count = request_data["likes_count"]
    
    # commit updated card
    db.session.commit()
    
    # return updated card
    return card.to_dict()

# Helper function to validate objects
def validate_item (model, item_id):
    # turn id into int and return 400 if invalid id
    try:
        item_id_int = int(item_id)
    except ValueError:
        return abort(make_response({"message":f"Item {item_id} invalid"}, 400))
    
    # if valid id, get item 
    item = model.query.get(item_id_int)
    
    # return 404 if item doesn't exist
    if not item:
        return abort(make_response({"message":f"Item {item_id_int} not found"}, 404))
    
    # return valid, existing item
    return item 
