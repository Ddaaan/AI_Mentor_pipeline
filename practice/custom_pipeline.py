from typing import List, Union, Generator, Iterator
from schemas import OpenAIChatMessage
from pydantic import BaseModel, Field
import requests


class Pipeline:
    class Valves(BaseModel):
        NAME_PREFIX: str = Field(
            default="OPENAI/",
            description="Prefix to be added before model names.",
        )
        OPENAI_API_BASE_URL: str = Field(
            default="https://api.openai.com/v1",
            description="Base URL for accessing OpenAI API endpoints.",
        )
        OPENAI_API_KEY: str = Field(
            default="apikey",
            description="API key for authenticating requests to the OpenAI API.",
        )

    def __init__(self):
        # Optionally, you can set the id and name of the pipeline.
        # Best practice is to not specify the id so that it can be automatically inferred from the filename, so that users can install multiple versions of the same pipeline.
        # The identifier must be unique across all pipelines.
        # The identifier must be an alphanumeric string that can include underscores or hyphens. It cannot contain spaces, special characters, slashes, or backslashes.
        # self.id = "pipeline_example"

        # The name of the pipeline.
        self.name = "Pipeline Example"
        self.valves = self.Valves()

    def pipes(self):
        return [
            {
                "id": "local-fastapi-agent",
                "name": "FASTAPI/Local LLM",
            }
        ]
        
    async def on_startup(self):
        # This function is called when the server is started.
        print(f"on_startup:{__name__}")
        pass

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        print(f"on_shutdown:{__name__}")
        pass

    async def on_valves_updated(self):
        # This function is called when the valves are updated.
        pass

    async def inlet(self, body: dict, user: dict) -> dict:
        # This function is called before the OpenAI API request is made. You can modify the form data before it is sent to the OpenAI API.
        print(f"inlet:{__name__}")

        print(body)
        print(user)

        return body

    async def outlet(self, body: dict, user: dict) -> dict:
        # This function is called after the OpenAI API response is completed. You can modify the messages after they are received from the OpenAI API.
        print(f"outlet:{__name__}")

        print(body)
        print(user)

        return body

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        try:
            r = requests.post(
                url="http://localhost:7998/agent",
                json={"query": user_message},
                timeout=30
            )
            r.raise_for_status()
            return {
                "choices": [
                    {
                        "message": {
                            "content": r.json().get("message", "(응답 없음)")
                        }
                    }
                ]
            }
        except Exception as e:
            return {
                "choices": [
                    {
                        "message": {
                            "content": f"[FastAPI 오류] {str(e)}"
                        }
                    }
                ]
            }