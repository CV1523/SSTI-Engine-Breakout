from flask import Flask, request, jsonify, render_template_string

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
    
    # Intentional Vulnerability: Rendering user input dynamically as a template string
    vulnerable_template_string = f"""
    <div>
        Source Reflection: {user_input}
    </div>
    """
    
    try:
        # Flask's built-in Jinja2 runtime engine compilation
        rendered_result = render_template_string(vulnerable_template_string, 
            secret_config="JINJA_LAB_SECRET_VAL_5544",
            user_status="guest_user"
        )
        return jsonify({"status": "success", "result": rendered_result}), 200
    except Exception as e:
        return jsonify({"status": "error", "error_message": str(e)}), 500

if __name__ == '__main__':
    # Running Jinja2 Lab on Port 5004
    app.run(debug=True, host='0.0.0.0', port=5001)