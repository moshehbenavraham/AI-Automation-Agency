from abc import ABC, abstractmethod
import openai
from app.config import get_settings

settings = get_settings()
openai.api_key = settings.openai_api_key

class AIService(ABC):
    @abstractmethod
    async def process_request(self, prompt: str):
        pass

class GPTService(AIService):
    async def process_request(self, prompt: str):
        response = await openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

class DALLEService(AIService):
    async def process_request(self, prompt: str):
        response = await openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        return response.data[0].url

class AIServiceFactory:
    @staticmethod
    def get_service(service_type: str) -> AIService:
        services = {
            "gpt": GPTService(),
            "dalle": DALLEService(),
        }
        return services.get(service_type.lower())