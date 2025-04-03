from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False) # to create the body column for contents
    created_at = db.Column(db.DateTime, server_default=db.func.now()) # to add the created time column

    def __repr__(self):
        return f"<Message {self.username}: {self.body}>"
