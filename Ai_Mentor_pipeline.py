from typing import List, Union, Generator, Iterator
from schemas import OpenAIChatMessage
from pydantic import BaseModel
import requests

# pipeline 클래스 정의 - OpenWebUI가 호출할 커스텀 파이프라인 클래스
class Pipeline:
    # 내부 설정용 클래스 - OpenWebUI에서 사용하는 환경변수를 정의
    class Valves(BaseModel):
        pass

    # 생성자
    def __init__(self):
        self.name = "Custom FastAPI Pipeline" # 파이프라인 이름 지정
        self.valves = self.Valves()
        pass

    async def on_startup(self):
        print(f"on_startup:{__name__}")

    async def on_shutdown(self):
        print(f"on_shutdown:{__name__}")

    # OpenWebUI에서 메시지를 보낼 때 실행
    def pipe(
        self,
        user_message: str, # 사용자 입력 메시지
        model_id: str,
        messages: List[dict], # 전체 대화 히스토리리
        body: dict
    ) -> Union[str, Generator, Iterator]:

        print(f"[PIPE] user_message: {user_message}")
        print(f"[PIPE] messages: {messages}")

        # FastAPI에 보낼 입력 추출 (사용자 메시지 추출)
        last_user_msg = ""
        for m in messages:
            if m.get("role") == "user":
                last_user_msg = m.get("content", "")

        print(f"[PIPE] 마지막 유저 메시지: {last_user_msg}")

        try:
            # FastAPI로 POST 요청
            r = requests.post(
                url="http://host.docker.internal:7998/agent", # tool_dumb/main.py로 전달
                json={"query": last_user_msg},
                timeout=10
            )
            r.raise_for_status()

            # JSON 응답 처리
            result = r.json().get("message", "❌ 응답 없음")

            return result

        except Exception as e:
            return f"❌ FastAPI 호출 오류: {str(e)}"
