from flask import Flask, request, jsonify, send_from_directory
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os
import pickle
from flask import abort
import json
import requests

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")  # Renderに環境変数として登録しておく

@app.route('/callback', methods=['POST'])
def callback():
    body = request.get_data(as_text=True)
    events = json.loads(body).get("events", [])

    for event in events:
        if event['type'] == 'message' and event['message']['type'] == 'text':
            reply_token = event['replyToken']
            message_text = event['message']['text']
            reply_message = f"「{message_text}」ですね。ご予約ありがとうございます！"

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
            }
            payload = {
                "replyToken": reply_token,
                "messages": [{
                    "type": "text",
                    "text": reply_message
                }]
            }

            requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, data=json.dumps(payload))

    return 'OK', 200

# スプレッドシート設定
SPREADSHEET_ID = '19YEhSe-A28MJ7nE6D2xY192BQKywNFAO1Imx3Z5-LkE'
RANGE_NAME = 'A:F'  # A列〜F列

# OAuth設定
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
TOKEN_PATH = 'token.pickle'
CREDENTIALS_PATH = 'credentials/client_secret_486682803199-n0so5fhs109e42ju53hv971akplkjikh.apps.googleusercontent.com.json'

@app.route('/')
def index():
    return '予約API 起動中'

@app.route('/form')
def serve_form():
    return send_from_directory('static', 'reserve.html')

@app.route('/privacy')
def serve_privacy():
    return send_from_directory('static', 'privacy.html')

@app.route('/reserve', methods=['POST'])
def reserve():
    data = request.json
    name = data.get('name')
    line_id = data.get('lineId')
    date = data.get('date')
    time = data.get('time')
    menu = data.get('menu')
    note = data.get('note')

    # 認証処理（Render環境ではtoken.pickleが存在している前提）
    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    else:
        return jsonify({'status': 'error', 'message': 'token.pickle not found'}), 500

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    values = [[date, time, menu, note, name, line_id]]
    body = {'values': values}

    result = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()

    return jsonify({
        'status': 'success',
        'updatedCells': result.get('updates', {}).get('updatedCells', 0)
    })

if __name__ == '__main__':
    # Render本番環境対応：外部公開用に0.0.0.0にbind、PORT環境変数で起動
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)