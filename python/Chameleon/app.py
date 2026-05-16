from flask import Flask, request, jsonify
from flask_cors import CORS
from chameleon import PageTemplate
import os

app = Flask(__name__)
CORS(app)

# NEW: Add this route to serve your index.html file automatically at the root URL
@app.route('/', methods=['GET'])
def home():
    try:
        with open('index.html', 'r') as f:
            return f.read(), 200, {'Content-Type': 'text/html'}
    except FileNotFoundError:
        return "Frontend index.html file missing from directory.", 404

# Your existing API endpoint remains exactly the same
@app.route('/api/render', methods=['GET'])
def render_api():
    user_input = request.args.get('payload', '')
    vulnerable_template = f"<div>{user_input}</div>"
    try:
        template = PageTemplate(vulnerable_template)
        # Simulating a vulnerable development practice:
        # Explicitly passing the system environment variables as 'env'
        rendered_result = template(env=os.environ)
        
        return jsonify({"status": "success", "result": rendered_result}), 200
    except Exception as e:
        return jsonify({"status": "error", "error_message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001)