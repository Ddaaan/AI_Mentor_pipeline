# JBNU AI Mentor pipeline
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
