from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card

# create blueprint
board_bp = Blueprint("board", __name__, url_prefix="/boards")

# post, get, patch, delete routes
# Board Routes
# 1. Create one Board 
# a. Post Request (request body)
# b. Return 201 OK + message saying the board was successfully created
# c. err message 404
@board_bp.route("", methods=["POST"])
def add_board():
    response_body = request.get_json()

    try:    
        new_board = Board(title=response_body["title"], owner=response_body["owner"])
    except KeyError:
        return {"details": "Invalid data"}, 400
    
    db.session.add(new_board)
    db.session.commit()

    return {"message": "board successfully added"}, 201

# 2. Read one Board
# a. Get Request for 1 board (/board_id)
# b. Return 200 OK (json response w/ board information)
# c. err message 404 
@board_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id): 
    board = validate_item(Board, board_id)

    return board.to_dict(), 200

# POST /boards/<board_id>/cards
# Create a card for a selected board
@board_bp.route("/<board_id>/cards", methods=["POST"])
def create_card_for_selected_board(board_id):
    # get request data
    request_body = request.get_json()
    # request_body is a dict
    request_body["board_id"] = board_id
    # validate board
    board = validate_item(Board, board_id)
    
    # validate and create new card
    if "message" not in request_body or len(request_body["message"]) > 40:
        return {"details": "Invalid Message"}, 400
    new_card = Card.from_dict(request_body)
    
    # add new card
    db.session.add(new_card)
    
    # attach new card to selected board
    new_card.board = board
    
    # commit changes
    db.session.commit()

    # return new card dict
    return new_card.to_dict(), 201

# GET /boards/<board_id>/cards
# Get all cards from given board
@board_bp.route("/<board_id>/cards", methods=["GET"])
def get_all_cards_from_board(board_id):
    # validate board
    board = validate_item(Board, board_id)

    # initialize list to hold cards
    cards_response = []
    
    # loop thru each card from given board
    for card in board.cards:
        # get card dict
        card_dict = card.to_dict()
        # append each card dict to list
        cards_response.append(card_dict)

    # return updated list
    return jsonify(cards_response)

# helper function to validate objects
def validate_item(model, item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        return abort(make_response({"message": f"invalid id: {item_id}"}, 400))
    
    item = model.query.get(item_id)
    if not item: 
        return abort(make_response({"message": f"{model.__name__} {item_id} not found"}, 404))

    return item


# 3. Read all Board(s)
# a. Get Request for all boards (/)
# b. Return 200 OK (json response w/ list of board dictionaries)
# c. err message 404 
@board_bp.route("", methods=["GET"])
def get_all_boards():
    response = []
    all_boards = Board.query.all() 

    for board in all_boards: 
        response.append(board.to_dict())
    
    return jsonify(response), 200



