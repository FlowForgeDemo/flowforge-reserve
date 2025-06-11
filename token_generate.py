from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDENTIALS_PATH = 'credentials/client_secret_486682803199-n0so5fhs109e42ju53hv971akplkjikh.apps.googleusercontent.com.json'  # 実際のファイル名に置き換え
TOKEN_PATH = 'token.pickle'

def main():
    flow = InstalledAppFlow.from_client_secrets_file(
        CREDENTIALS_PATH, SCOPES)
    creds = flow.run_local_server(port=0)
    with open(TOKEN_PATH, 'wb') as token:
        pickle.dump(creds, token)
    print("token.pickle が生成されました ✅")

if __name__ == '__main__':
    main()