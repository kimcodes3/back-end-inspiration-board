from app import db

# create Card class
class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey("board.board_id"), nullable=True)
    board = db.relationship("Board", back_populates="cards")
    
    # create method to format responses for existing card
    def to_dict(self):
        return {
            "card_id": self.card_id,
            "message": self.message,
            "likes_count": self.likes_count
        }
    
    # create class method to format responses for new card  
    @classmethod
    def from_dict(cls, card_request_data):
        return cls (
            message = card_request_data["message"],
            likes_count = card_request_data["likes_count"],
            board_id = card_request_data["board_id"]
        )

