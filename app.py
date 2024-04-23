# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_socketio import SocketIO, emit
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key' # Replace 'your_secret_key' with a secure key
socketio = SocketIO(app)

# Function to load users from JSON file
def load_users():
    try:
        with open('users.json', 'r') as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {"user": []}
        with open('users.json', 'w') as f:
            json.dump(users, f)
    return users

# Function to save users to JSON file
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)

# Function to load chat messages from JSON file
def load_chat_messages():
    try:
        with open('chat_messages.json', 'r') as f:
            messages = json.load(f)
    except FileNotFoundError:
        messages = []
        with open('chat_messages.json', 'w') as f:
            json.dump(messages, f)
    return messages

# Function to save chat messages to JSON file
def save_chat_messages(messages):
    with open('chat_messages.json', 'w') as f:
        json.dump(messages, f)

def load_private_chat_messages():
    try:
        with open('index.json', 'r') as f:
            messages = json.load(f)
    except FileNotFoundError:
        messages = {}
        with open('index.json', 'w') as f:
            json.dump(messages, f)
    return messages

def save_private_chat_messages(messages):
    with open('index.json', 'w') as f:
        json.dump(messages, f)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        for user in users['user']:
            if user['username'] == username and user['password'] == password:
                session['username'] = username # Store the username in the session
                return redirect(url_for('profile', username=username))
        return "Invalid login", 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        for user in users['user']:
            if user['username'] == username:
                return "Username already exists", 400
        new_user = {"username": username, "password": password}
        users['user'].append(new_user)
        save_users(users)
        return redirect(url_for('profile', username=username))
    return render_template('register.html')

@app.route('/profile/<username>')
def profile(username):
    if 'username' in session and session['username'] == username:
        return render_template('profile.html', user={"username": username})
    else:
        return "User not found or not logged in", 404

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/chat')
def chat():
    messages = load_chat_messages()
    return render_template('chat.html', messages=messages)

@socketio.on('message')
def handle_message(data):
    print("Received message:", data)
    messages = load_chat_messages()
    print("Current messages:", messages)
    messages.append(data)
    print("Updated messages:", messages)
    save_chat_messages(messages)
    print("Messages saved.")
    emit('message', data, broadcast=True)

@app.route('/chat/<username>', methods=['GET', 'POST'])
def chat_with_user(username):
    if 'username' in session:
        return render_template('chat_with_user.html', receiver_username=username)
    else:
        return "User not found or not logged in", 404
@socketio.on('private_message')
def handle_private_message(data):
    print("Received private message:", data)
    sender_username = session.get('username')
    receiver_username = data.get('receiver')
    message_content = data.get('message')

    if sender_username and receiver_username and message_content:
        messages = load_private_chat_messages()
        print("Current messages:", messages)
        conversation_key = f"{sender_username}-{receiver_username}"
        if conversation_key not in messages:
            messages[conversation_key] = []
        messages[conversation_key].append({
            'sender': sender_username,
            'message': message_content,
            'timestamp': datetime.now().isoformat()
        })
        print("Updated messages:", messages)
        save_private_chat_messages(messages)
        print("Messages saved.")
        emit('private_message', {'sender': sender_username, 'message': message_content}, room=conversation_key)
    else:
        print("Message not saved due to missing data.")



@app.route('/messages')
def view_messages():
    if 'username' in session:
        username = session['username']
        all_messages = load_private_chat_messages()
        user_messages = []
        for conversation_key, messages in all_messages.items():
            if username in conversation_key:
                user_messages.extend(messages)
        return render_template('messages.html', messages=user_messages)
    else:
        return "User not found or not logged in", 404
    
if __name__ == '__main__':
    socketio.run(app, debug=True)
