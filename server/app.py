from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages')
def messages():
    messages = Message.query.all() # gets all messages
    return jsonify([message.to_dict() for message in messages]), 200

# create messages
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()

    try:
        new_message = Message(
            body=data["body"], # gets the body content
            username=data["username"], # gets the username
        )
        db.session.add(new_message)
        db.session.commit()

        return jsonify(new_message.to_dict()), 201
    except KeyError as e:
        return jsonify({"error": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/messages/<int:id>')
def messages_by_id(id):
    return ''

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id) # finds the messages by id

    if not message:
        return jsonify({"error": "Message not found"}), 404
    
    data = request.get_json()
    try:
        if "body" in data:
            message.body = data["body"] # updates the body
        db.session.commit()

        return jsonify(message.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id) 

    if not message:
        return jsonify({"error": "Message not found"}), 404
    
    try:
        db.session.delete(message) # deletes a message
        db.session.commit()

        return jsonify({"message": "Message deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5555)
