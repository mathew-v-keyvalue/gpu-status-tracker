"""Main Flask application for GPU status tracker Slack bot."""
import logging
from flask import Flask, request, jsonify
from utils.status_manager import initialize_status
from handlers import command_handlers, handle_help

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/', methods=['POST'])
def slack_command():
    """
    Handle Slack slash command requests.
    
    Expected form data:
    - user_id: Slack user ID
    - user_name: Slack user name
    - text: Command text (e.g., "claim 0 training 2h")
    
    Returns:
        JSON response with Slack Block Kit blocks
    """
    try:
        data = request.form
        user_id = data.get('user_id', 'unknown')
        user_name = data.get('user_name', 'Unknown User')
        command_text = data.get('text', '').strip()
        
        logger.info(f"Received command from {user_name} ({user_id}): {command_text}")
        
        parts = command_text.split() if command_text else []
        action = parts[0].lower() if parts else "status"
        args = parts[1:]

        # Find the correct handler function using the action string.
        # If the command is unknown, default to the help handler.
        handler = command_handlers.get(action, handle_help)
        
        # Execute the handler to get the response blocks
        response_blocks = handler(args, user_id, user_name)
        
        logger.debug(f"Returning {len(response_blocks)} blocks for action: {action}")

        return jsonify({
            "response_type": "in_channel",
            "blocks": response_blocks
        })
        
    except Exception as e:
        logger.error(f"Error processing command: {e}", exc_info=True)
        return jsonify({
            "response_type": "ephemeral",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"❌ *Error*\nAn unexpected error occurred: {str(e)}"
                    }
                }
            ]
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    # Ensure the status file exists before starting the server
    try:
        initialize_status()
        logger.info("GPU status tracker bot starting...")
    except Exception as e:
        logger.error(f"Failed to initialize status: {e}")
        raise
    
    # To run in production, you would use a proper WSGI server like Gunicorn
    # Example: gunicorn -w 4 -b 0.0.0.0:5000 bot:app
    app.run(port=5000, debug=True)