from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board

# create blueprint
board_bp = Blueprint("board", __name__, url_prefix="/board")

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

