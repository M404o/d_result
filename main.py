from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from M's diagnostic system!"}

@app.get("/index.html", response_class=HTMLResponse)
async def serve_diagnosis():
    """診断画面を表示"""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    except FileNotFoundError:
        return HTMLResponse("<h1>Diagnosis page not found</h1>")

@app.get("/result-light", response_class=HTMLResponse)
async def serve_light_result():
    """軽いユーザー向け結果画面を表示"""
    try:
        with open("user_result_light.html", "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    except FileNotFoundError:
        return HTMLResponse("""
        <html>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>✨ Assessment Completed!</h1>
            <p>Thank you for completing the Mindscape assessment.</p>
            <p>Your results are being processed...</p>
            <a href="/index.html">Take Another Assessment</a>
        </body>
        </html>
        """)

# 既存のunified_backend.pyのルートも追加（もし必要なら）
@app.get("/api/export")
async def export_results():
    """結果ダウンロード機能"""
    return {"message": "Export functionality - download your results here"}
