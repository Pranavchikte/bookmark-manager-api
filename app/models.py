import mongoengine as db
import datetime

class User(db.Document):
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True, min_length=8)
    created_at = db.DateTimeField(default=datetime.datetime.now(datetime.UTC))
    
class Item(db.Document):
    owner = db.ReferenceField(User, required=True)
    title = db.StringField(required=True, max_length=200)
    item_type = db.StringField(choices=('bookmark', 'snippet', 'note'), required=True)
    content = db.StringField(required=True)
    tags = db.ListField(db.StringField(max_length=50))
    created_at = db.DateTimeField(default=datetime.datetime.now(datetime.UTC))
        
    def to_dict(self):
        return{
            "id": str(self.id),
            "title": self.title,
            "item_type": self.item_type,
            "content": self.content,
            "tags": self.tags,
            "created_at": self.created_at.isoformat()
        }