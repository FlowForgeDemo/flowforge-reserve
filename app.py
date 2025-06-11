from flask import Flask, request, jsonify, send_from_directory
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os
import pickle

app = Flask(__name__)

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