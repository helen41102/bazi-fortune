"""
八字 AI 算命 — FastAPI 后端
启动命令：uvicorn main:app --host 0.0.0.0 --port 8000 --reload
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from bazi_calc import get_bazi
from ai_analyzer import analyze_bazi

load_dotenv()

app = FastAPI(
    title="八字 AI 算命",
    description="输入生日，AI 帮你解读八字命理",
    version="1.0.0",
)

# CORS 配置（允许前端跨域访问）
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── 请求/响应模型 ──────────────────────────────────────────

class FortuneRequest(BaseModel):
    year: int = Field(..., ge=1900, le=2100, description="出生年份")
    month: int = Field(..., ge=1, le=12, description="出生月份")
    day: int = Field(..., ge=1, le=31, description="出生日期")
    hour: int = Field(..., ge=0, le=23, description="出生小时（24小时制）")
    name: str = Field(default="", max_length=20, description="姓名（可选）")
    question: str = Field(default="", max_length=200, description="追加问题（可选）")


class BaziInfo(BaseModel):
    年柱: str
    月柱: str
    日柱: str
    时柱: str
    日主: str
    日主五行: str
    最旺五行: str
    最弱五行: str
    生肖: str
    星座: str
    五行统计: dict


class FortuneResponse(BaseModel):
    success: bool
    bazi: BaziInfo
    analysis: str
    message: str = ""


# ── 路由 ──────────────────────────────────────────────────

@app.get("/")
async def root():
    return {"message": "🔮 八字 AI 算命 API 正常运行", "docs": "/docs"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/fortune", response_model=FortuneResponse)
async def get_fortune(req: FortuneRequest):
    """
    根据生日计算八字并进行 AI 解读
    """
    try:
        # 1. 计算八字
        bazi_data = get_bazi(req.year, req.month, req.day, req.hour)

        # 2. AI 解读
        analysis = analyze_bazi(
            bazi_data,
            user_name=req.name,
            extra_question=req.question
        )

        # 3. 整理返回数据
        bazi_info = BaziInfo(
            年柱=bazi_data["四柱"]["年柱"],
            月柱=bazi_data["四柱"]["月柱"],
            日柱=bazi_data["四柱"]["日柱"],
            时柱=bazi_data["四柱"]["时柱"],
            日主=bazi_data["日主"],
            日主五行=bazi_data["日主五行"],
            最旺五行=bazi_data["最旺五行"],
            最弱五行=bazi_data["最弱五行"],
            生肖=bazi_data["阴历"]["生肖"],
            星座=bazi_data["阴历"]["星座"],
            五行统计=bazi_data["五行统计"],
        )

        return FortuneResponse(
            success=True,
            bazi=bazi_info,
            analysis=analysis,
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误：{str(e)}")


@app.post("/bazi-only")
async def get_bazi_only(req: FortuneRequest):
    """
    仅计算八字，不调用 AI（用于测试或离线场景）
    """
    try:
        bazi_data = get_bazi(req.year, req.month, req.day, req.hour)
        return {"success": True, "data": bazi_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
