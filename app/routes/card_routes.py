from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
from app.models.board import Board
import requests, os

card_bp = Blueprint("card_bp", __name__, url_prefix="/cards")
board_bp = Blueprint("board_bp", __name__, url_prefix="/boards")

# POST /boards/<board_id>/cards
# Create a card for a selected board
@board_bp.route("/<board_id>/cards", methods=["POST"])
def create_card_for_selected_board(board_id):
    # get request data
    request_body = request.get_json()
    # request_body is a dict
    
    # validate board
    board = validate_item(Board, board_id)
    
    # validate new card
    if len(request_body["message"]) > 40 or "message" not in request_body:
        return {"details": "Invalid Message"}, 400
    new_card = Card.from_dict(request_body)
    
    # add new card
    db.session.add(new_card)
    
    # attach new card to board
    new_card.board = board
    
    db.session.commit()

    # return message
    return {"new card successfully created"}, 201

# GET /boards/<board_id>/cards
# get all cards from 1 board
# @board_bp.route("/<board_id>/cards", methods=["GET"])
# def get_all_cards_from_board(board_id):
#     # validate board
#     board = validate_item(Board, board_id)

#     # initialize list of cards
#     cards_response = []
    
#     # loop thru each card from given board
#     for card in board.cards:
#         # return card dict
#         card_dict = card.to_dict()
#         # add board_id to each card dict
#         card_dict["board_id"] = board.board_id
#         # append each card dict to list
#         cards_response.append(card_dict)

#     # return updated list
#     return cards_response

# DELETE /cards/<card_id>
# Delete a card from 1 board
@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    # validate card
    card = validate_item(Card, card_id)
    
    # delete card and commit delete
    db.session.delete(card)
    db.session.commit()
    
    return {"details": f'Card {card.card_id} successfully deleted'}

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
    
    # commit updated goal
    db.session.commit()
    
    # return dict of goal dicts
    return {"card": card.to_dict()}

# Helper function
def validate_item (model, item_id):
    try:
        item_id_int = int(item_id)
    except:
        return abort(make_response({"message":f"Item {item_id} invalid"}, 400))
    
    item = model.query.get(item_id_int)
    
    if not item:
        return abort(make_response({"message":f"Item {item_id_int} not found"}, 404))
    
    return item 




# Card Routes
# 1. Create one Card 
# a. Post Request (request body) (/board_id/card_id)
# b. Return 201 OK + message saying card was successfully created 
# c. err message 404 

# 2. Read all Cards from one Board
# a. Get Request (/board_id/cards)
# b. 200 OK + a list of card objects (jsonified)
# c. err message 404 

# 3. Delete a Card from one Board
# a. Delete Request (/board_id/card_id)
# b. 202 Accepted Status + message saying it was successfully deleted
# c. err message 404 

# 4. Add num likes to a Card
# a. Patch Request (board_id/card_id) (request body {num_likes: 8})
# b. increment the num of likes based on user interaction
# c. err 200 OK