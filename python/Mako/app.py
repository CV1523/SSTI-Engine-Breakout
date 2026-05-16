from flask import Flask, request, jsonify
from mako.template import Template

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
    
    # Intentional Vulnerability: Directly interpolating user input into the template source string
    vulnerable_template_string = f"""
    <div>
        Source Reflection: {user_input}
    </div>
    """
    
    try:
        # Initializing the Mako template object
        mako_template = Template(vulnerable_template_string)
        
        # Rendering with a couple of mock environment context parameters
        rendered_result = mako_template.render(
            api_tier="internal-prod-01",
            debug_status=False
        )
        return jsonify({"status": "success", "result": rendered_result}), 200
    except Exception as e:
        return jsonify({"status": "error", "error_message": str(e)}), 500

if __name__ == '__main__':
    # Running Mako Lab on Port 5005
    app.run(debug=True, host='0.0.0.0', port=5001)