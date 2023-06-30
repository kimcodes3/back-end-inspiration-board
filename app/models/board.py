from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String)
    owner=db.Column(db.String)
    cards = db.relationship("Card", back_populates="board", lazy=True)

    def to_dict(self): 
        return {
                "board_id": self.board_id,
                "title": self.title, 
                "owner": self.owner
                }

    # def sort_function(self):
        # return db.relationship("Card", back_populates="board", lazy=True, order_by="Card.id")
    
