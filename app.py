# app.py
from flask import Flask, request, jsonify
import time
import uuid

app = Flask(__name__)

@app.route("/pipeline", methods=["POST"])
def pipeline_stub():
    """
    Open Web UI → Flask → Pipeline 더미 처리 엔드포인트
    들어온 payload의 마지막 user 메시지를 echo 형태로 돌려줍니다.
    """
    payload = request.get_json() or {}
    # 마지막 user 메시지 추출
    last_user = ""
    for m in payload.get("messages", []):
        if m.get("role") == "user":
            last_user = m.get("content", "")
            print(last_user)
    # 더미 응답 콘텐츠
    reply = f"나와라 얍: {last_user}"

    # 응답 포맷 조립
    resp = {
        "object": "chat.completion",
        "created": int(time.time()),
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": reply
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
    }
    return jsonify(resp)


if __name__ == "__main__":
    # pip install flask
    app.run(host="0.0.0.0", port=8000, debug=True)