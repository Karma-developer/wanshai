from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/telegram-webhook', methods=['POST'])
def webhook():
    data = request.json
    message = data.get('message', {})
    
    # Chiama Vellum API
    requests.post(
        'https://predict.vellum.ai/v1/execute-workflow',
        headers={'X-API-KEY': 'Nc3ny5Br.vf5AiDX3T3kjzXzgKsG6RDaFPiTcgl25'},
        json={
            'workflow_deployment_name': 'wan-shi-ai-assistant',
            'inputs': {
                'user_message': message.get('text', ''),
                'telegram_chat_id': message['chat']['id'],
                'chat_history': []
            }
        }
    )
    return 'OK'