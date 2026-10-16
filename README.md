# Watch Party

## What is this?

This is a simple website where friends can join a room and watch sample videos together.

## Features

- Create a room or join using a room code
- The host controls the video
- Chat with other people
- Send emoji reactions
- Add videos to the playlist

## Tools used

- Python
- Flask
- HTML
- CSS
- JavaScript
- Socket.IO

## Project files

- `app.py` - runs the server and handles rooms
- `templates/index.html` - the webpage
- `static/script.js` - makes the buttons work
- `static/style.css` - changes how the page looks
- `requirements.txt` - packages needed to run the project

## How to run it in VS Code

These steps use **Command Prompt**, not PowerShell.

1. Download and unzip the project.
2. Open the folder in VS Code.
3. Click **Terminal → New Terminal**. Choose **Command Prompt** if needed.
4. Check Python:

   ```bat
   python --version
   ```

5. Create a virtual environment:

   ```bat
   python -m venv .venv
   ```

6. Activate it:

   ```bat
   .venv\\Scripts\\activate.bat
   ```

7. Install the packages:

   ```bat
   python -m pip install -r requirements.txt
   ```

8. Run the project:

   ```bat
   python app.py
   ```

9. Open this address in your browser:

   **http://127.0.0.1:5000**

Keep the terminal open while the website is running. Press `Ctrl+C` to stop it.

## How to test

1. Create a room and copy the room code.
2. Open another browser window.
3. Enter a name and join using the room code.
4. Try chat, reactions, playlist buttons, and video controls.

Some websites do not allow their videos to play inside other websites, so use the sample videos provided.

## Upload to GitHub

1. Create a new repository on [GitHub](https://github.com/).
2. Open this folder in VS Code.
3. Click **Source Control** on the left.
4. Click **Initialize Repository**.
5. Stage and commit the files.
6. Click **Publish to GitHub**.

## Note

This is a beginner project for learning. Room data is stored in memory, so it disappears when the server stops. The project has not been tested with 10 or more users yet.
