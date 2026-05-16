import os
from flask import Flask, request, jsonify
from django.conf import settings
from django.template import Template, Context

# Minimal Django configuration to run the template engine standalone
if not settings.configured:
    settings.configure(
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
        }]
    )

import django
django.setup()

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
    
    # Intentional Vulnerability: Dynamically injecting user input directly into the template compilation string
    vulnerable_template_string = f"""
    <div>
        Source Reflection: {user_input}
    </div>
    """
    
    try:
        # Compiling the template string using Django's Engine
        django_template = Template(vulnerable_template_string)
        
        # We pass a simple user context dictionary to simulate template variable availability
        context = Context({
            'current_user': 'sec_admin',
            'is_authenticated': True
        })
        
        rendered_result = django_template.render(context)
        return jsonify({"status": "success", "result": rendered_result}), 200
        
    except Exception as e:
        return jsonify({"status": "error", "error_message": str(e)}), 500

if __name__ == '__main__':
    # Running Django Lab on Port 5003
    app.run(debug=True, host='0.0.0.0', port=5001)