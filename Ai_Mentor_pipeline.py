from typing import List, Union, Generator, Iterator
from schemas import OpenAIChatMessage
from pydantic import BaseModel
import json
import requests

# pipeline 클래스 정의 - OpenWebUI가 호출할 커스텀 파이프라인 클래스
class Pipeline:
    # 내부 설정용 클래스 - OpenWebUI에서 사용하는 환경변수를 정의
    class Valves(BaseModel):
        pass

    # 생성자
    def __init__(self):
        self.name = "Ai_Mentor_pipeline" # 파이프라인 이름 지정
        self.valves = self.Valves()
        pass

    # 파이프 라인 이름을 설정, 위에서 정의한 Valves 객체 초기화
    async def on_startup(self):
        print(f"on_startup:{__name__}")

    async def on_shutdown(self):
        print(f"on_shutdown:{__name__}")

    # OpenWebUI에서 메시지를 보낼 때 실행
    def pipe(
        self,
        user_message: str, # 사용자 입력 메시지
        model_id: str,
        messages: List[dict], # 전체 대화 히스토리
        body: dict
    ) -> Union[str, Generator, Iterator]:

        # ----------------- Debug line ----------------------
        print(f"[PIPE] user_message: {user_message}")
        print(f"[PIPE] messages: {messages}")
        # ---------------------------------------------------

        # FastAPI에 보낼 입력 추출 (사용자 메시지 추출)
        last_user_msg = ""
        for m in messages:
            if m.get("role") == "user":
                last_user_msg = m.get("content", "")

        print(f"[PIPE] 마지막 유저 메시지: {last_user_msg}") # Debug line

        try:
            r = requests.post(
                url="http://host.docker.internal:8001/agent",
                json={"query": last_user_msg},
                timeout=2000
            )
            r.raise_for_status()

            result = r.json() # json 형태의 응답을 가져옴
            msg = result.get("message", {}) # 그중 message 키를 가져옴

            # 요약 텍스트 만들기
            final_message = msg.get("final_message")
            steps = msg.get("steps", [])

            # 문자열로 변환
            summary_text = ""

            # isinstance : 특정 값이 특정 클래스나 자료형의 인스턴스인지 확인 (isinstance (객체, 클래스) -> T/F 반환함)
            if isinstance(final_message, dict): # final_message가 dict 자료형이면
                summary_text += "최종 추천 결과:\n"
                summary_text += json.dumps(final_message, ensure_ascii=False) + "\n\n" # ensure_ascii : 한글 깨짐 방지

            if isinstance(steps, list):
                for step in steps:
                    summary_text += f"Step {step['step_number']} ({step['tool_name']})\n" # 몇 번째 실행인지 / 어떤 tool을 사용했는지지
                    summary_text += f"요청: {step['tool_input']}\n" # tool에 보낸 입력값
                    summary_text += f"응답: {json.dumps(step['tool_response'], ensure_ascii=False)}\n" # 응답값 출력 dict 형태인데 dumps를 활용해 json 문자열 형태로 변환해서 출력력 (dict : 딕셔너리 자료형 - key-value쌍의 집합)
                    summary_text += f"사유: {step['reason']}\n\n" # LLM이 이 도구를 사용한 이유

            return summary_text.strip() # 전체 요약된 문자열 반환 (앞뒤 공백을 제거하고고)

        except Exception as e:
            return f"FastAPI 호출 오류: {str(e)}"

