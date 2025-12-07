from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from .chatbot import get_bot_response
from .emotion_detector import analyze_image_bytes
from .db import get_db, save_session
from .alerts import check_and_send_alert


app = FastAPI(title="MANO-MITRA API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class ChatReq(BaseModel):
user_id: str
text: str


@app.post('/chat')
async def chat(req: ChatReq):
# get bot response
resp = get_bot_response(req.text, req.user_id)
# save session log
db = get_db()
save_session(db, req.user_id, {'type': 'chat', 'user': req.text, 'bot': resp})
# check alerting rules (very simple): if negative sentiment threshold hit
check_and_send_alert(db, req.user_id, resp)
return {'reply': resp}


@app.post('/emotion')
async def emotion(file: UploadFile = File(...), user_id: str = "anonymous"):
data = await file.read()
try:
result = analyze_image_bytes(data)
except Exception as e:
raise HTTPException(status_code=400, detail=str(e))
db = get_db()
save_session(db, user_id, {'type': 'emotion', 'result': result})
check_and_send_alert(db, user_id, result)
return result


if __name__ == '__main__':
uvicorn.run('api.main:app', host='0.0.0.0', port=8000, reload=True)