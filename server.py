from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
import socket
import argparse
from typing import Dict
import os

# FastAPI 앱 인스턴스 생성
app = FastAPI()

# --- CORS 미들웨어 설정 ---
# 모든 외부 출처에서의 API 요청을 허용합니다.
# 프로덕션 환경에서는 보안을 위해 특정 도메인만 허용하는 것이 좋습니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # "*"는 모든 origin을 허용함을 의미합니다.
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드(GET, POST 등)를 허용합니다.
    allow_headers=["*"],  # 모든 HTTP 헤더를 허용합니다.
)

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
PUBLIC_IP = os.getenv('PUBLIC_IP', None)

# 외부에서 접속 가능한 IP 주소를 자동으로 찾기
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
except Exception:
    ip_address = "127.0.0.1"
    print("외부 IP 주소를 찾을 수 없습니다. 로컬 주소로 서버를 시작합니다.")

print("=" * 60)
print("FastAPI 서버를 시작합니다. 다른 기기에서 접속하여 테스트하세요.")
print(f"   - 로컬 접속: http://127.0.0.1:{PORT}")
print(f"   - 외부 접속 (Docker IP): http://{ip_address}:{PORT}")
if PUBLIC_IP is not None:
    print(f"   - 외부 접속 (Public IP): http://{PUBLIC_IP}:{PORT}")
print(f"   - API 문서 (Swagger UI): http://{ip_address}:{PORT}/docs")
print("=" * 60)
print("서버를 중지하려면 CTRL+C를 누르세요.")

# --- Pydantic 모델 정의 ---
# POST 요청 시 받을 데이터의 구조를 정의합니다.
class Message(BaseModel):
    content: str = Field(..., description="전송할 메시지 내용", example="안녕하세요!")

# --- API 엔드포인트 정의 ---

@app.get("/", summary="서버 상태 확인")
async def read_root() -> Dict[str, str]:
    """
    서버의 루트 경로로 접속했을 때, 서버가 정상적으로 실행 중임을 알리는 메시지를 반환합니다.
    """
    return {"status": "ok", "message": "FastAPI 서버가 정상적으로 실행 중입니다."}

@app.get("/hello", summary="간단한 인사 메시지")
async def say_hello(name: str = "World") -> Dict[str, str]:
    """
    쿼리 파라미터로 받은 이름(name)을 포함한 인사 메시지를 반환합니다.
    예: /hello?name=Gemini
    """
    return {"message": f"Hello, {name}!"}


@app.post("/send-message", summary="메시지 전송 (POST)")
async def send_message(message: Message) -> Dict[str, str]:
    """
    클라이언트로부터 메시지를 받아 성공적으로 수신했음을 응답합니다.
    """
    if not message.content:
        raise HTTPException(status_code=400, detail="메시지 내용이 비어있습니다.")

    print(f"수신된 메시지: {message.content}")
    return {"status": "success", "received_message": message.content}


# --- 서버 실행 ---
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="FastAPI 서버 실행 스크립트")
#     parser.add_argument("--port", type=int, default=8000, help="서버가 실행될 포트 번호")
#     args = parser.parse_args()

#     # 외부에서 접속 가능한 IP 주소를 자동으로 찾기
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.connect(("8.8.8.8", 80))
#         ip_address = s.getsockname()[0]
#         s.close()
#     except Exception:
#         ip_address = "127.0.0.1"
#         print("외부 IP 주소를 찾을 수 없습니다. 로컬 주소로 서버를 시작합니다.")

#     print("=" * 60)
#     print("FastAPI 서버를 시작합니다. 다른 기기에서 접속하여 테스트하세요.")
#     print(f"   - 로컬 접속: http://127.0.0.1:{args.port}")
#     print(f"   - 외부 접속: http://{ip_address}:{args.port}")
#     print(f"   - API 문서 (Swagger UI): http://{ip_address}:{args.port}/docs")
#     print("=" * 60)
#     print("서버를 중지하려면 CTRL+C를 누르세요.")

#     # 0.0.0.0 호스트를 사용하여 모든 인터페이스에서 접속을 허용
#     uvicorn.run("server:app", host="0.0.0.0", port=args.port, reload=True)
