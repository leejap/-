from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

# LostArk API KEY 설정
API_KEY = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IktYMk40TkRDSTJ5NTA5NWpjTWk5TllqY2lyZyIsImtpZCI6IktYMk40TkRDSTJ5NTA5NWpjTWk5TllqY2lyZyJ9.eyJpc3MiOiJodHRwczovL2x1ZHkuZ2FtZS5vbnN0b3ZlLmNvbSIsImF1ZCI6Imh0dHBzOi8vbHVkeS5nYW1lLm9uc3RvdmUuY29tL3Jlc291cmNlcyIsImNsaWVudF9pZCI6IjEwMDAwMDAwMDA1ODM2NzMifQ.ToCVUsGvPh3HvhyFdanUOeBY0_X3TNdrQRMe-h9bx-thfLIxkx6vaQSLRagOsY9WXql20TgpoKcOeAITcUB3FX8SCatb14AzfMtmJ8tMQnaA_NliZNVjBG5gp0LdNtFGtr8TsajSgkWReR6paOdJPRuOsjxeFGdSJJPUOtFnsqDzxjW8uZiJNUP2sXIHhynR1iJFuXCKDJZgnCmnH66_lxzBonPmT5Kr95wUl6x1gI7ZkRoHufrserMX_Tu-uGx8v3LNpjB6aSgL7Nbyi6C9BUaSwYnHHruXuE7t46e2Ng6u8apswOUnDV-0I0FpodjxtiLOj3rzssvs407RwkM_uA'
headers = {
    'accept': 'application/json',
    'authorization': f'Bearer {API_KEY}'
}

@app.route('/', methods=['GET'])
def home():
    return "✅ 로스트아크 Flask 서버가 정상 실행 중입니다."


@app.route('/character/text', methods=['GET'])
def get_character_text():
    name = request.args.get('name')
    if not name:
        return "❗ 캐릭터 이름이 필요합니다.", 400

    url = f'https://developer-lostark.game.onstove.com/armories/characters/{name}/profiles'
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return f"❗ '{name}' 캐릭터 정보를 찾을 수 없습니다.", 404

    try:
        data = json.loads(response.text)
    except json.JSONDecodeError:
        return "❗ 응답을 JSON으로 파싱할 수 없습니다.", 500

    result_text = f"""📌 로스트아크 캐릭터 정보
닉네임: {data.get("CharacterName", "알 수 없음")}
서버: {data.get("ServerName", "알 수 없음")}
직업: {data.get("CharacterClassName", "알 수 없음")}
아이템 레벨: {data.get("ItemAvgLevel", "알 수 없음")}
길드: {data.get("GuildName", "없음")}"""

    return result_text, 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
