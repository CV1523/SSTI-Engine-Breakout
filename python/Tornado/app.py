import asyncio
import tornado.web
import tornado.template

class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            with open('index.html', 'r') as f:
                self.write(f.read())
        except FileNotFoundError:
            self.set_status(404)
            self.write("index.html missing from active directory.")

class RenderApiHandler(tornado.web.RequestHandler):
    def get(self):
        user_input = self.get_argument('payload', '')
        
        # Intentional Vulnerability: Direct string injection into the template block before compilation
        vulnerable_template_string = f"""
        <div>
            Source Reflection: {user_input}
        </div>
        """
        
        try:
            # Tornado compiles and renders the string template inline
            t = tornado.template.Template(vulnerable_template_string)
            rendered_result = t.generate(deploy_env="tornado-async-core")
            
            self.set_header("Content-Type", "application/json")
            self.write({"status": "success", "result": rendered_result.decode('utf-8')})
        except Exception as e:
            self.set_status(500)
            self.set_header("Content-Type", "application/json")
            self.write({"status": "error", "error_message": str(e)})

def make_app():
    return tornado.web.Application([
        (r"/", HomeHandler),
        (r"/api/render", RenderApiHandler),
    ], debug=True, autoreload=True)

async def main():
    app = make_app()
    app.listen(5001, address="0.0.0.0")
    print("Tornado SSTI Lab server started on port 5001...")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())