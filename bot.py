from flask import Flask, request, jsonify
from utils.status_manager import initialize_status
from handlers import command_handlers, handle_help

app = Flask(__name__)

@app.route('/', methods=['POST'])
def slack_command():
    data = request.form
    user_id = data.get('user_id')
    user_name = data.get('user_name')
    command_text = data.get('text', '').strip()
    parts = command_text.split()
    
    action = parts[0].lower() if parts else "status"
    args = parts[1:]

    # Find the correct handler function using the action string.
    # If the command is unknown, default to the help handler.
    handler = command_handlers.get(action, handle_help)
    
    # Execute the handler to get the response blocks
    response_blocks = handler(args, user_id, user_name)

    return jsonify({
        "response_type": "in_channel",
        "blocks": response_blocks
    })

if __name__ == '__main__':
    # Ensure the status file exists before starting the server
    initialize_status()
    # To run in production, you would use a proper WSGI server like Gunicorn
    app.run(port=5000, debug=True)