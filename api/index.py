from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import urllib.error

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/telegram-webhook':
            try:
                # Read the request body
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                message = data.get('message', {})
                user_message = message.get('text', '')
                chat_id = message.get('chat', {}).get('id')
                
                # Prepare Vellum API request
                vellum_data = json.dumps({
                    'workflow_deployment_name': 'wan-shi-ai-assistant',
                    'inputs': {
                        'user_message': user_message,
                        'telegram_chat_id': chat_id,
                        'chat_history': []
                    }
                }).encode('utf-8')
                
                # Call Vellum API
                req = urllib.request.Request(
                    'https://predict.vellum.ai/v1/execute-workflow',
                    data=vellum_data,
                    headers={
                        'X-API-KEY': 'Nc3ny5Br.vf5AiDX3T3kjzXzgKsG6RDaFPiTcgl25',
                        'Content-Type': 'application/json'
                    },
                    method='POST'
                )
                
                with urllib.request.urlopen(req) as response:
                    response.read()
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'OK')
                
            except Exception as e:
                # Send error response
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(f'Error: {str(e)}'.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        # Health check endpoint
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Webhook server is running')