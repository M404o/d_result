from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from datetime import datetime

# FastAPI app
app = FastAPI(
    title="Mindscape Diagnosis - Separate System",
    description="セパレート式心理診断システム",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================================
# HTMLページ配信
# ========================================

@app.get("/", response_class=HTMLResponse)
async def serve_diagnosis():
    """診断画面を表示"""
    try:
        with open("diagnosis.html", "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    except FileNotFoundError:
        return HTMLResponse("""
        <html>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>🧠 Mindscape Diagnosis</h1>
            <p>診断ファイルが見つかりません</p>
            <p>diagnosis.html をアップロードしてください</p>
        </body>
        </html>
        """)

@app.get("/light-result", response_class=HTMLResponse)
async def serve_light_result():
    """軽い結果画面を表示"""
    try:
        with open("light_result.html", "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    except FileNotFoundError:
        return HTMLResponse("""
        <html>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>✨ Assessment Completed!</h1>
            <p>Thank you for completing the assessment.</p>
            <p>Your summary is ready!</p>
            <a href="/">← Take Another Assessment</a>
        </body>
        </html>
        """)

@app.get("/detailed-result", response_class=HTMLResponse)
async def serve_detailed_result():
    """詳細結果画面を表示"""
    try:
        with open("detailed_result.html", "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    except FileNotFoundError:
        return HTMLResponse("""
        <html>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>🧠 Detailed Analysis</h1>
            <p>詳細結果ページを準備中です</p>
            <a href="/light-result">← Back to Summary</a>
        </body>
        </html>
        """)

# ========================================
# API エンドポイント
# ========================================

@app.get("/api/health")
async def health_check():
    """ヘルスチェック"""
    return {
        "status": "healthy",
        "service": "Mindscape Diagnosis - Separate System",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "features": {
            "diagnosis": True,
            "light_results": True,
            "detailed_analysis": True,
            "custom_deployment": True
        }
    }

@app.get("/api/test")
async def test_api():
    """API動作テスト"""
    return {
        "message": "✨ セパレート式診断システム稼働中！",
        "endpoints": {
            "diagnosis": "/",
            "light_result": "/light-result", 
            "detailed_result": "/detailed-result",
            "health": "/api/health"
        },
        "status": "All systems operational"
    }

# ========================================
# データ処理エンドポイント
# ========================================

@app.post("/api/save-summary")
async def save_summary(data: dict):
    """軽い結果のサマリーを保存（オプション）"""
    try:
        # ファイルに保存する場合
        filename = f"summary_{data.get('profile', {}).get('name', 'anonymous')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(f"summaries/{filename}", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        return {
            "status": "success",
            "message": "Summary saved successfully",
            "filename": filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存エラー: {str(e)}")

@app.get("/api/download-template")
async def download_template():
    """サマリーダウンロード用テンプレート"""
    return {
        "template": {
            "name": "ユーザー名",
            "department": "部署名",
            "date": "診断日",
            "responses": {
                "department_questions": "部署別質問数",
                "personal_insights": "内省質問数", 
                "inner_landscape": "心の風景描写"
            },
            "quick_analysis": "簡易分析結果",
            "recommendations": [
                "推奨事項1",
                "推奨事項2"
            ]
        }
    }

# ========================================
# カスタマイズ用エンドポイント
# ========================================

@app.get("/api/customize")
async def get_customization_options():
    """企業向けカスタマイズオプション"""
    return {
        "available_customizations": {
            "colors": {
                "primary": "#667eea",
                "secondary": "#764ba2", 
                "success": "#48bb78",
                "customizable": True
            },
            "branding": {
                "company_name": "設定可能",
                "logo_url": "設定可能",
                "custom_message": "設定可能"
            },
            "questions": {
                "department_specific": True,
                "custom_questions": "追加可能",
                "language": "多言語対応可能"
            },
            "features": {
                "download_formats": ["JSON", "CSV", "PDF"],
                "email_notifications": "設定可能",
                "integration_apis": "設定可能"
            }
        },
        "deployment_info": {
            "type": "Individual Enterprise Deployment",
            "isolation": "Complete data separation",
            "customization_level": "Full customization available"
        }
    }

# ========================================
# 統計・モニタリング
# ========================================

@app.get("/api/stats")
async def get_basic_stats():
    """基本統計情報"""
    try:
        # 簡単な統計
        summary_count = len([f for f in os.listdir("summaries") if f.endswith('.json')]) if os.path.exists("summaries") else 0
        
        return {
            "total_assessments": summary_count,
            "last_assessment": datetime.now().isoformat(),
            "system_status": "operational",
            "deployment_type": "separate_enterprise"
        }
    except Exception as e:
        return {
            "total_assessments": 0,
            "error": "統計取得エラー",
            "system_status": "operational"
        }

# ========================================
# エラーハンドリング
# ========================================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return HTMLResponse("""
    <html>
    <body style="font-family: Arial; text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; min-height: 100vh;">
        <h1>🧠 Mindscape Diagnosis</h1>
        <h2>Page Not Found</h2>
        <p>お探しのページが見つかりません</p>
        <a href="/" style="color: white; text-decoration: underline;">診断を開始する</a>
    </body>
    </html>
    """, status_code=404)

@app.exception_handler(500)
async def server_error_handler(request, exc):
    return HTMLResponse("""
    <html>
    <body style="font-family: Arial; text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; min-height: 100vh;">
        <h1>🧠 Mindscape Diagnosis</h1>
        <h2>System Error</h2>
        <p>システムエラーが発生しました</p>
        <a href="/" style="color: white; text-decoration: underline;">トップページに戻る</a>
    </body>
    </html>
    """, status_code=500)

# ========================================
# アプリケーション起動設定
# ========================================

if __name__ == "__main__":
    import uvicorn
    
    # summariesディレクトリ作成
    os.makedirs("summaries", exist_ok=True)
    
    print("=" * 50)
    print("🚀 Mindscape Diagnosis - Separate System")
    print("=" * 50)
    print("📊 診断画面: http://localhost:8000/")
    print("✨ 軽い結果: http://localhost:8000/light-result")
    print("🧠 詳細結果: http://localhost:8000/detailed-result")
    print("🔧 API動作テスト: http://localhost:8000/api/test")
    print("💡 カスタマイズ: http://localhost:8000/api/customize")
    print("=" * 50)
    print("🎨 セパレート式システム稼働開始！")
    print("=" * 50)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
