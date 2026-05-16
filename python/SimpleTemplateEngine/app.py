from bottle import route, run, request, response, SimpleTemplate

@route('/')
def home():
    try:
        with open('index.html', 'r') as f:
            content = f.read()
            response.content_type = 'text/html'
            return content
    except FileNotFoundError:
        response.status = 404
        return "index.html missing from active directory."

@route('/api/render')
def render_api():
    user_input = request.query.get('payload', '')
    
    # Intentional Vulnerability: Direct concatenation into the dynamic compilation string
    vulnerable_template_string = f"""
    <div>
        Source Reflection: {user_input}
    </div>
    """
    
    try:
        # Initializing the template compiler and rendering
        compiled_tpl = SimpleTemplate(vulnerable_template_string)
        rendered_result = compiled_tpl.render(deploy_env="staging-node-core")
        
        response.content_type = 'application/json'
        return {"status": "success", "result": rendered_result}
    except Exception as e:
        response.status = 500
        response.content_type = 'application/json'
        return {"status": "error", "error_message": str(e)}

if __name__ == '__main__':
    # Running Bottle on Port 5007
    run(host='0.0.0.0', port=5001, debug=True, reloader=True)