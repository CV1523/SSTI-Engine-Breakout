from flask import Flask, request, jsonify
import pystache

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    try:
        with open('index.html', 'r') as f:
            content = f.read()
            return content, 200, {'Content-Type': 'text/html'}
    except FileNotFoundError:
        return "index.html missing from active directory.", 404

@app.route('/api/render', methods=['GET'])
def render_api():
    user_input = request.args.get('payload', '')
    
    # Intentional Vulnerability: Directly injecting user input into the raw template source string
    vulnerable_template_string = f"""
    <div>
        Source Reflection: {user_input}
    </div>
    """
    
    try:
        # A mocked data context containing hierarchical information to demonstrate disclosure patterns
        data_context = {
            "current_user": {
                "username": "sec_operator_05",
                "role": "Researcher",
                "api_access_token": "TOK-PYSTACHE-9933-X7",
                "is_admin": False
            },
            "environment": {
                "tier": "Staging-Lab",
                "debug_flag": True,
                "internal_dns": "internal-db.local"
            },
            "system_messages": ["Session Initialized", "Lab Bound on Port 5006"]
        }
        
        # Pystache renders the dynamically compiled string with the context dictionary
        rendered_result = pystache.render(vulnerable_template_string, data_context)
        return jsonify({"status": "success", "result": rendered_result}), 200
        
    except Exception as e:
        return jsonify({"status": "error", "error_message": str(e)}), 500

if __name__ == '__main__':
    # Running Pystache Lab on Port 5006
    app.run(debug=True, host='0.0.0.0', port=5001)