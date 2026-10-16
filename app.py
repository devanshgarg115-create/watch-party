# Watch Party - simple Python project
# This file runs the website and handles live updates between users.

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room
import random
import string
import time

app = Flask(__name__)
app.config["SECRET_KEY"] = "watch-party-key"
socketio = SocketIO(app, cors_allowed_origins="*")

# Room information is kept here while the server is running.
rooms = {}

# Small list of sample videos for testing.
videos = [
    {
        "title": "Flower Video",
        "category": "Nature",
        "url": "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"
    },
    {
        "title": "Big Buck Bunny",
        "category": "Animation",
        "url": "https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
    },
    {
        "title": "Elephant Dream",
        "category": "Sci-Fi",
        "url": "https://storage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4"
    }
]


@app.route("/")
def home():
    # Open the main webpage.
    return render_template("index.html")


def make_room_code():
    # Create a random 6-character room code.
    letters = string.ascii_uppercase + string.digits
    return "".join(random.choice(letters) for _ in range(6))


def send_room_update(code):
    # Send the latest room information to everyone in that room.
    room = rooms[code]
    socketio.emit("room_update", room, to=code)


@socketio.on("create_room")
def create_room(data):
    name = data.get("name", "Guest").strip() or "Guest"
    code = make_room_code()

    # Make sure the code is not already being used.
    while code in rooms:
        code = make_room_code()

    rooms[code] = {
        "code": code,
        "host": request.sid,
        "users": [{"id": request.sid, "name": name}],
        "video_url": videos[0]["url"],
        "playing": False,
        "current_time": 0,
        "chat": [],
        "playlist": [],
        "reactions": []
    }

    join_room(code)
    emit("room_joined", {"code": code, "room": rooms[code]})


@socketio.on("join_room")
def join_existing_room(data):
    code = data.get("code", "").strip().upper()
    name = data.get("name", "Guest").strip() or "Guest"

    if code not in rooms:
        emit("show_error", "Room not found. Check the code.")
        return

    room = rooms[code]
    room["users"].append({"id": request.sid, "name": name})
    join_room(code)

    emit("room_joined", {"code": code, "room": room})
    send_room_update(code)


@socketio.on("play_video")
def play_video(data):
    code = data.get("code")
    if code not in rooms:
        return

    room = rooms[code]

    # Only the host can control the video.
    if room["host"] != request.sid:
        emit("show_error", "Only the host can control the video.")
        return

    room["playing"] = data.get("playing", False)
    room["current_time"] = data.get("current_time", 0)
    socketio.emit("video_update", {
        "video_url": room["video_url"],
        "playing": room["playing"],
        "current_time": room["current_time"],
        "sent_at": time.time()
    }, to=code)
    send_room_update(code)


@socketio.on("choose_video")
def choose_video(data):
    code = data.get("code")
    if code not in rooms:
        return

    room = rooms[code]
    if room["host"] != request.sid:
        emit("show_error", "Only the host can choose the video.")
        return

    room["video_url"] = data.get("url", videos[0]["url"])
    room["playing"] = False
    room["current_time"] = 0

    socketio.emit("video_update", {
        "video_url": room["video_url"],
        "playing": False,
        "current_time": 0,
        "sent_at": time.time()
    }, to=code)
    send_room_update(code)


@socketio.on("send_chat")
def send_chat(data):
    code = data.get("code")
    if code not in rooms:
        return

    message_text = data.get("message", "").strip()
    if not message_text:
        return

    room = rooms[code]
    user_name = "Guest"
    for user in room["users"]:
        if user["id"] == request.sid:
            user_name = user["name"]

    message = {"name": user_name, "text": message_text[:300]}
    room["chat"].append(message)
    room["chat"] = room["chat"][-50:]
    socketio.emit("new_chat", message, to=code)


@socketio.on("send_reaction")
def send_reaction(data):
    code = data.get("code")
    if code not in rooms:
        return

    reaction = data.get("emoji", "❤️")
    room = rooms[code]
    room["reactions"].append(reaction)
    room["reactions"] = room["reactions"][-10:]
    socketio.emit("new_reaction", reaction, to=code)


@socketio.on("add_playlist")
def add_playlist(data):
    code = data.get("code")
    if code not in rooms:
        return

    room = rooms[code]
    room["playlist"].append({
        "title": data.get("title", "Video"),
        "url": data.get("url", "")
    })
    send_room_update(code)


@socketio.on("disconnect")
def disconnect_user():
    # Remove the person who disconnected from any room they were in.
    for code in list(rooms.keys()):
        room = rooms[code]
        room["users"] = [
            user for user in room["users"] if user["id"] != request.sid
        ]

        # If the host leaves, make the first remaining person the host.
        if room["host"] == request.sid and room["users"]:
            room["host"] = room["users"][0]["id"]

        # Delete the room if everyone has left.
        if not room["users"]:
            del rooms[code]
        else:
            send_room_update(code)


if __name__ == "__main__":
    # Start the website on your computer.
    socketio.run(app, host="127.0.0.1", port=5000, debug=True)
