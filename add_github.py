import pandas as pd
import time
import requests
from tqdm import tqdm
import yaml

with open('test.yaml', 'rb') as f:
    yml = yaml.safe_load(f)

# ========== 設定 ==========
GITHUB_TOKEN = yml["GITHUB_API_KEY"]
ORG_NAME = yml["CSV_FILE"] 
CSV_FILE = yml["ORGNIZATION"]
SLEEP_SECONDS = 60  # 1分待機

# ========== ヘッダー ==========
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

# ========== GitHubユーザー名からIDを取得 ==========
def get_user_id(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("id")
    return None

# ========== 招待送信 ==========
def invite_user(user_id, username):
    url = f"https://api.github.com/orgs/{ORG_NAME}/invitations"
    data = {"invitee_id": user_id}
    response = requests.post(url, headers=HEADERS, json=data)
    if response.status_code == 201:
        print(f"[OK] 招待送信成功: {username}")
    else:
        print(f"[ERROR] 招待送信失敗: {username} | ステータス: {response.status_code} | 内容: {response.text}")

# ========== メイン処理 ==========
def main():
    df = pd.read_csv(CSV_FILE)
    print("read this csv data:{}".format(CSV_FILE))

    for _, row in tqdm(df.iterrows(), total=len(df), desc="招待処理中", unit="人"):
        student_id = row["学籍番号"]
        name = row["氏名"]
        username = row["githubアカウントID"]

        print(f"\n--- 処理中: {name} ({student_id}) | GitHub: {username} ---")
        user_id = get_user_id(username)

        if user_id:
            invite_user(user_id, username)
        else:
            print(f"[WARNING] ユーザー情報取得失敗（存在しない可能性）:")
            print(f"  学籍番号: {student_id}")
            print(f"  氏名    : {name}")
            print(f"  GitHub  : {username}")
            print(f"  ➤ このユーザーはスキップされました。")
        time.sleep(SLEEP_SECONDS)

if __name__ == "__main__":
    main()
