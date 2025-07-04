from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

# LostArk API KEY 설정
API_KEY = os.getenv('LOA_API_KEY')
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


@app.route('/help', methods=['GET'])
def help_command():
    help_text = """📖 사용 가능한 명령어 목록

✅ 캐릭터 정보 조회:
  /character/text?name=캐릭터이름

✅ 상태 확인:
  /

✅ 도움말 보기:
  /help
"""
    return help_text, 200, {'Content-Type': 'text/plain; charset=utf-8'}


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
