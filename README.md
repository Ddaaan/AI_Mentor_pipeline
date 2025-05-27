![image](https://github.com/user-attachments/assets/22e52cdc-d7fd-48d4-9bbe-95cc4d7100e3)# JBNU AI Mentor pipeline
### Code Review & Study (지속적 업데이트 예정)
> **✅ host.docker.internal 관련** 🔗[Code Review - host.docker.internal](https://sneaky-viscose-116.notion.site/Code-Review-host-docker-internal-1ff84dccb378801ebf23c039b1d15c22?pvs=4)

<br><br>

## 📅 ~ 2025-05-22
- Docker Desktop 설치 및 OpenWebUI 컨테이너 생성, 실행
- Ai_mentor 코드 분석
> **📌 코드 분석 정리 링크** 🔗[Ai_Mentor Github 분석](https://sneaky-viscose-116.notion.site/Ai_Mentor-Github-1e384dccb37880348f53df1e2ec0c95e?pvs=4)
<br>

## 📅 2025-05-23
- Ai_mentor 코드 분석
- Vector_DB 연결되지 않은 LLM 코드 실행 성공 (tool_dumb\main.py)

![image (12)](https://github.com/user-attachments/assets/d12528e1-02b4-4b97-98fd-7444e45b6d27)
- test.py 파일 만들어서 실행 성공 (post방식으로 링크 호출)

![image](https://github.com/user-attachments/assets/c5b2ec70-563f-424d-9f13-1174b0d16dd8)

<br>

## 📅 2025-05-26
- new_Ai_mentor 코드 분석 및 파악 (진행중)
- tool_dumb 폴더의 파일들에 import문 경로 수정
```python
# 기존코드
from controller.controller import router as agent_router

# 수정코드
from tool_dumb.controller.controller import router as agent_router
```
- Ai_Mentor_pipeline.py 파일을 생성해 tool_dumb 폴더에 연결된 모델로 openwebui 환경 구성 성공



> **📌 tool_dumb main.py 코드 실행**
> ```bash
> set PYTHONPATH=.
> python -m tool_dumb.main
> ```
<br>

- Web상에서 질문 및 응답, 터미널에서의 요청 로그
- 아직 Vector DB를 참조하지 않는 것으로 보임 <br>

![image](https://github.com/user-attachments/assets/26d7380f-22e6-4995-97c9-d707dc666dee)
![image](https://github.com/user-attachments/assets/a4ac129d-649c-472c-ace5-595294534ac6)

<br><br>
**DB까지 연결된 코드로 pipeline 연동 시도**
- faiss_search\main.py 실행(port : 7997) 
- llm_agent\main.py 실행 (port : 8001)
- Ai_Mentor_pipeline url부분 코드 수정
- AttributeError: 'NoneType' object has no attribute 'cursor' 오류 뜸 : DB 연결이 실패함

<br>

## 📅 2025-05-27
- coreService.py 파일까지 잘 들어가서 실행되는 것 확인
- OpenWebUI에서 입력한 질문 전달 성공 (CAD를 배우는 과목이 뭐야)

![image](https://github.com/user-attachments/assets/255d3dc9-73d1-4e35-82e2-acade737db99)

- 사용자가 질문 (인공지능과 관련된 과목 알려줘)을 보내면 faiss search가 돌아가서 비슷한 과목을 리스트 형태로 뽑아냄
- UI에는 출력 오류가 발생함

![image](https://github.com/user-attachments/assets/1d58391f-2d41-43dd-9381-94f0c9bc1fdd)

- 테스트를 위해 test.py 코드를 별도로 작성하여 json 응답이 어떤 형태로 나오는지 파악
> 예시 질문인 "전북대학교에서 인공지능 과목이 뭐가 있어?" 라는 질문은 json형식은 아래와 같음

```python3
import requests
res = requests.post(
    "http://localhost:8001/agent",
    json={"query": "전북대학교에서 인공지능 과목이 뭐가 있어?"}
)
print(res.json())
```
test.py 코드 <br>
```bash
{'message': {
  'steps': [
  {
  'step_number': 1,
  'tool_name': 'search',
  'tool_input': '{"count": 5, "key": "인공지능"}',
  'tool_response': {'key': "['인공지능', '인공지능', '인공지능', '인공지능', '공공정책입법과정']"},
  'reason': '인공지능 과목에 대한 정보를 찾기 위해 "search" 도구를  사용했습니다. 이 도구는 입력된 과목명과 유사한 수업을 추천하는 기능을 가지고 있습니다. "인공지능"에 대해 검색을 진행하였습니다.'
  }
],
'final_message': {
  'key': "['인공지능', '인공지능', '인공지능', '인공지능', '공공정책입법과정']"
    }
  }
}
```
test.py 파일에서 출력된 json 형식 구조 <br>

- json 구조를 분석 후 일단 형식 그대로 UI에 출력되게 코드 수정
- tool을 여러 번 사용해서 다양한 결과를 비교 후 가장 최적의 답변을 나오도록 prompt가 설계되어 있는 것 같음

![image](https://github.com/user-attachments/assets/37bbfbaf-072c-4298-8625-cf8dcfacad8f)

- final_message의 key를 사용한 응답을 만든 코드를 파악하거나 생성한 후 응답이 제대로 나오게 코드 수정 예정
