from flask import Flask, render_template, jsonify, request, session
from engine.game_manager import BlackjackGame
from agent.brain import BlackjackAgent
from agent.parser import ActionParser
from config import Config

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# Initialize our core components
game = BlackjackGame()
agent = BlackjackAgent(api_key=Config.OPENAI_API_KEY, model=Config.MODEL_NAME)
parser = ActionParser(game)

@app.route('/')
def index():
    """Renders the main game page."""
    return render_template('index.html')

@app.route('/api/start', methods=['POST'])
def start_game():
    """Initializes a new deck and deals the first two cards."""
    game.start_new_game()
   # Store the result of to_dict() in the session
    session['game_state'] = game.to_dict()
    return jsonify(game.get_state())

@app.route('/api/status', methods=['GET'])
def get_status():
    """Returns the current board state as JSON."""
    return jsonify(game.get_state())

@app.route('/api/action', methods=['POST'])
def player_action():

    # 1. Pull the data from the session
    state_data = session.get('game_state')
    if not state_data:
        return jsonify({"error": "No game in progress"}), 400

    """
    Receives a manual action from a user button.
    Expected JSON: {"action": "HIT"} or {"action": "STAND"}
    """
    data = request.json
    # 2. Rebuild the game object (or update the dict directly)
    # For a simple app, it's often easier to just work with the dict
    action = request.json.get('action').upper()

    if game.status != "IN_PROGRESS":
        return jsonify({"error": "Game is not in progress"}), 400

    if action == "HIT":
        game.player_hit()
    elif action == "STAND":
        game.player_stand()
    else:
        return jsonify({"error": "Invalid action"}), 400

    session['game_state'] = game.to_dict()
    session.modified = True
    return jsonify(game.get_state())
@app.route('/api/agent_step', methods=['POST'])
def agent_step():
    """
    Triggers the LLM to look at the board and make a move.
    """
    if game.status == "IN_PROGRESS":
        # 1. Brain thinks
        decision = agent.get_decision(game.get_state())
        # 2. Parser executes move on the Engine
        parser.execute_agent_move(decision)
        
    return jsonify(game.get_state())

if __name__ == '__main__':
    # Run on http://127.0.0.1:5000
    app.run(debug=True)