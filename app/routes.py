# from flask import Blueprint, request, jsonify, make_response
# from app import db

# example_bp = Blueprint('example_bp', __name__)

# post, get, patch, delete routes
# Board Routes
# 1. Create one Board 
# a. Post Request (request body)
# b. Return 201 OK + message saying the board was successfully created
# c. err message 404

# 2. Read one Board
# a. Get Request for 1 board (/board_id)
# b. Return 200 OK (json response w/ board information)
# c. err message 404 

# 3. Read all Board(s)
# a. Get Request for all boards (/)
# b. Return 200 OK (json response w/ list of board dictionaries)
# c. err message 404 


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

