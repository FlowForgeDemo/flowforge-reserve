from flask import Flask, request, jsonify, send_from_directory
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import pickle

app = Flask(__name__)

# スプレッドシート設定
SPREADSHEET_ID = '19YEhSe-A28MJ7nE6D2xY192BQKywNFAO1Imx3Z5-LkE'
RANGE_NAME = 'A:F'  # A列〜F列（ヘッダーがある場合、2行目から自動で追記）

# OAuth用スコープ
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
TOKEN_PATH = 'token.pickle'
CREDENTIALS_PATH = 'credentials/client_secret_486682803199-n0so5fhs109e42ju53hv971akplkjikh.apps.googleusercontent.com.json'  # ダウンロードしたJSONファイルのパス

# トップページ
@app.route('/')
def index():
    return '予約API 起動中'

# HTML予約フォーム表示（LIFFで読み込む）
@app.route('/form')
def serve_form():
    return send_from_directory('static', 'reserve.html')

# 予約データ受信エンドポイント
@app.route('/reserve', methods=['POST'])
def reserve():
    data = request.json

    name = data.get('name')
    line_id = data.get('lineId')
    date = data.get('date')
    time = data.get('time')
    menu = data.get('menu')
    note = data.get('note')

    # 認証処理
    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_PATH, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    # Google Sheets API 呼び出し
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
    app.run(debug=True)