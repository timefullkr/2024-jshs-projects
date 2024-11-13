import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import socket
from datetime import datetime



# 현재 디렉토리 경로를 가져옵니다
current_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(current_dir, "templates")

# 필요한 디렉토리 생성
if not os.path.exists(templates_dir):
    os.makedirs(templates_dir)

app = FastAPI()

# 템플릿 설정 (절대 경로 사용)
templates = Jinja2Templates(directory=templates_dir)

# 정적 파일 설정 추가 (절대 경로 사용)
app.mount("/static", StaticFiles(directory=templates_dir), name="static")

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("templates/favicon.ico")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    client_ip = request.client.host
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "client_ip": client_ip, "current_time": current_time}
    )

if __name__ == "__main__":
    
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(f"서버가 시작되었습니다.")
    print(f"로컬 접속 주소: http://localhost:8000")
    print(f"네트워크 접속 주소: http://{ip_address}:8000")
    
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)


