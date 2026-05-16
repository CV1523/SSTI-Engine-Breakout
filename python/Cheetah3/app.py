from flask import Flask, request, jsonify
from Cheetah.Template import Template

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
    
    # Reflecting input explicitly into template compilation block
    vulnerable_template_string = f"""
    <div>
        Source Reflection: {user_input}
    </div>
    """
    
    try:
        # Pre-seeding local variables to explore info disclosure properties
        compiled_template = Template(vulnerable_template_string, searchList=[{
            'secret_api_key': 'CHEETAH_LAB_MASTER_TOKEN_998822',
            'server_env': 'development-backend'
        }])
        
        rendered_result = str(compiled_template)
        return jsonify({"status": "success", "result": rendered_result}), 200
        
    except Exception as e:
        return jsonify({"status": "error", "error_message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)