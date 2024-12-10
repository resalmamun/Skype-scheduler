from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime, timedelta
import threading
from skpy import Skype
import os

app = Flask(__name__)

# Function to send the message to Skype
def send_message(message, receivers):
    skype = Skype("hasanalmamun55@gmail.com", "pprlqvwdmvguomhn")  # Replace with your Skype credentials
    for receiver in receivers:
        contact = skype.contacts[receiver.strip()]  # Strip to remove extra spaces around receiver ID
        contact.chat.sendMsg(message)
    print(f"Message sent to {', '.join(receivers)}: {message}")

# Function to schedule a task at a specific time
def schedule_task(message, task_time, receivers, weekly=False):
    delay = (task_time - datetime.now()).total_seconds()
    if delay > 0:
        if weekly:
            # Schedule the task every week on the same day and time
            def repeat_weekly():
                send_message(message, receivers)
                schedule_task(message, task_time + timedelta(weeks=1), receivers, weekly=True)
            threading.Timer(delay, repeat_weekly).start()
        else:
            threading.Timer(delay, send_message, [message, receivers]).start()  # Schedule the message

# Route for the main page (index.html)
@app.route('/')
def index():
    # Serve index.html from the same directory as app.py
    return send_from_directory(os.path.dirname(__file__), 'index.html')

# Route to serve other static files (e.g., CSS and JS)
@app.route('/<filename>')
def serve_file(filename):
    # Serve other files (CSS, JS) from the same directory as app.py
    return send_from_directory(os.path.dirname(__file__), filename)

# Route to schedule a message
@app.route('/schedule_message', methods=['POST'])
def schedule_message():
    data = request.get_json()
    message = data['message']
    datetime_str = data['datetime']
    receivers = data['receivers']
    weekly = data.get('weekly', False)
    task_time = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
    schedule_task(message, task_time, receivers, weekly)
    return jsonify({"status": "success", "message": f"Message scheduled for {task_time}"}), 200

if __name__ == '__main__':
    app.run(debug=True)
