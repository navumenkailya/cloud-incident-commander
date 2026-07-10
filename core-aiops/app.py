from fastapi import FastAPI, Request
import requests
import json

app = FastAPI()

# Адрес нашего контейнера Ollama внутри сети Docker
OLLAMA_URL = "http://ollama-ai:11434/api/generate"

@app.post("/webhook")
async def receive_log(request: Request):
    # Получаем данные от Vector
    log_data = await request.json()
    
    # ХИТРОСТЬ: Если Vector прислал список (батч), работаем с ним. 
    # Если пришел один объект, заворачиваем его в список из одного элемента.
    if isinstance(log_data, list):
        logs_to_process = log_data
    else:
        logs_to_process = [log_data]

    # Итерируемся по всем логам в пакете
    for log in logs_to_process:
        cloud = log.get("cloud", "Unknown Cloud")
        service = log.get("service", "Unknown Service")
        message = log.get("message", "No message")
        status = log.get("status", "Unknown")

        print(f"\n🚨 [AI Core] Обнаружен инцидент в {cloud} (Сервис: {service})")
        print(f"Текст ошибки: {message}")
        
        # Формируем инженерный промпт для ИИ
        prompt = f"""
        You are an expert SRE (Site Reliability Engineer). Analyze this production error:
        Cloud Environment: {cloud}
        Microservice: {service}
        Error Message: {message}
        HTTP Status: {status}
        
        Provide a brief Root Cause Analysis (RCA) and 2-3 precise steps to fix this issue.
        Respond in Russian language. Be concise and professional.
        """
        
        # Отправляем запрос в Ollama
        try:
            response = requests.post(OLLAMA_URL, json={
                "model": "phi3",
                "prompt": prompt,
                "stream": False
            })
            
            ai_response = response.json().get("response")
            print("\n🤖 [Incident Commander AI Resolution]:")
            print(ai_response)
            print("=" * 60)
            
        except Exception as e:
            print(f"❌ Не удалось связаться с ИИ-движком: {e}")
        
    return {"status": "analyzed", "processed_count": len(logs_to_process)}