"""
千鱼千寻 2.0 Web API
提供 RESTful API 接口供前端调用
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sys
import os

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(title="千鱼千寻 2.0 API", version="2.0.0")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件
web_dir = os.path.join(os.path.dirname(__file__))
app.mount("/static", StaticFiles(directory=web_dir), name="static")


# ==================== 数据模型 ====================

class CoachQuestion(BaseModel):
    question: str
    user_id: str = "web_user"


class WeatherQuery(BaseModel):
    city: str


class CatchRecord(BaseModel):
    user_id: str
    species: str
    weight: float
    location: str = ""


# ==================== API 端点 ====================

@app.get("/")
async def root():
    """返回首页"""
    return FileResponse(os.path.join(web_dir, "index.html"))


# ==================== 钓鱼教练 ====================

@app.post("/api/coach/ask")
async def coach_ask(question: CoachQuestion):
    """钓鱼教练问答"""
    try:
        # 这里需要调用实际的钓鱼教练服务
        # from skills.fishing_coach.service import FishingCoachService
        # service = FishingCoachService()
        # answer = service.ask_question(question.question, question.user_id)

        # 临时返回模拟数据
        return {
            "success": True,
            "answer": f"关于「{question.question}」的回答：\n\n这是一个很好的问题！根据我的知识库，我建议...\n\n（这是演示数据，实际需要连接到 AI 服务）",
            "sources": ["知识图谱", "RAG 检索"],
            "confidence": 0.85
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/coach/history")
async def coach_history(user_id: str = "web_user", limit: int = 10):
    """获取用户提问历史"""
    return {
        "success": True,
        "history": [
            {"question": "鲫鱼怎么钓？", "timestamp": "2026-03-12 10:00:00"},
            {"question": "今天适合钓鱼吗？", "timestamp": "2026-03-12 09:30:00"},
        ]
    }


# ==================== 鱼类识别 ====================

@app.post("/api/fish/identify")
async def fish_identify(image: UploadFile = File(...)):
    """鱼类识别"""
    try:
        # 读取图片
        contents = await image.read()

        # 这里需要调用实际的鱼类识别服务
        # from skills.fish_identifier.service import FishIdentifierService
        # service = FishIdentifierService()
        # result = service.identify_fish(contents)

        # 临时返回模拟数据
        return {
            "success": True,
            "species": "鲫鱼",
            "confidence": 0.92,
            "tips": "鲫鱼喜欢在水草丰富的地方活动，建议使用蚯蚓或红虫作为饵料。",
            "description": "鲫鱼是常见的淡水鱼类，体型较小，肉质鲜美。"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/fish/tips")
async def fish_tips(species: str):
    """获取鱼种钓鱼技巧"""
    return {
        "success": True,
        "species": species,
        "tips": f"关于{species}的钓鱼技巧：\n1. 选择合适的钓点\n2. 使用正确的饵料\n3. 掌握提竿时机"
    }


# ==================== 天气顾问 ====================

@app.get("/api/weather/current")
async def weather_current(city: str):
    """获取当前天气"""
    try:
        # 这里需要调用实际的天气服务
        # from skills.weather_advisor.service import WeatherAdvisorService
        # service = WeatherAdvisorService()
        # weather = service.get_current_weather(city)

        # 临时返回模拟数据
        return {
            "success": True,
            "city": city,
            "weather": "多云",
            "temperature": 22,
            "humidity": 65,
            "wind_speed": 3.5,
            "fishing_index": 85,
            "suggestion": "天气适宜钓鱼，建议选择上午或傍晚时段。"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/weather/forecast")
async def weather_forecast(city: str, days: int = 7):
    """获取天气预报"""
    return {
        "success": True,
        "city": city,
        "forecast": [
            {"date": "2026-03-12", "weather": "晴", "temp_high": 25, "temp_low": 18, "fishing_index": 90},
            {"date": "2026-03-13", "weather": "多云", "temp_high": 23, "temp_low": 17, "fishing_index": 85},
            {"date": "2026-03-14", "weather": "小雨", "temp_high": 20, "temp_low": 15, "fishing_index": 60},
        ]
    }


# ==================== 钓点管理 ====================

@app.get("/api/spots/nearby")
async def spots_nearby(lat: float, lon: float, radius: float = 10):
    """查找附近钓点"""
    return {
        "success": True,
        "spots": [
            {
                "id": 1,
                "name": "深圳湾公园",
                "distance": 2.5,
                "fish_species": ["鲫鱼", "草鱼"],
                "rating": 4.5
            },
            {
                "id": 2,
                "name": "西丽水库",
                "distance": 5.8,
                "fish_species": ["鲤鱼", "鲫鱼", "草鱼"],
                "rating": 4.8
            },
        ]
    }


@app.get("/api/spots/search")
async def spots_search(fish: str = None, keyword: str = None):
    """搜索钓点"""
    return {
        "success": True,
        "spots": [
            {
                "id": 1,
                "name": "深圳湾公园",
                "fish_species": ["鲫鱼", "草鱼"],
                "rating": 4.5
            },
        ]
    }


@app.get("/api/spots/{spot_id}")
async def spot_details(spot_id: int):
    """获取钓点详情"""
    return {
        "success": True,
        "spot": {
            "id": spot_id,
            "name": "深圳湾公园",
            "address": "深圳市南山区",
            "fish_species": ["鲫鱼", "草鱼", "鲤鱼"],
            "facilities": ["停车场", "洗手间", "小卖部"],
            "rating": 4.5,
            "reviews_count": 128,
            "description": "深圳湾公园是一个环境优美的钓鱼地点..."
        }
    }


# ==================== 渔获记录 ====================

@app.post("/api/catch/log")
async def catch_log(record: CatchRecord):
    """记录渔获"""
    return {
        "success": True,
        "message": "渔获记录成功",
        "catch_id": 123
    }


@app.get("/api/catch/list")
async def catch_list(user_id: str = "web_user", limit: int = 20):
    """获取渔获列表"""
    return {
        "success": True,
        "catches": [
            {
                "id": 1,
                "species": "鲫鱼",
                "weight": 0.5,
                "location": "深圳湾公园",
                "date": "2026-03-12",
                "photo": None
            },
            {
                "id": 2,
                "species": "草鱼",
                "weight": 1.2,
                "location": "西丽水库",
                "date": "2026-03-11",
                "photo": None
            },
        ]
    }


@app.get("/api/catch/stats")
async def catch_stats(user_id: str = "web_user"):
    """获取渔获统计"""
    return {
        "success": True,
        "stats": {
            "total_catches": 25,
            "total_weight": 18.5,
            "favorite_species": "鲫鱼",
            "favorite_location": "深圳湾公园",
            "best_month": "3月"
        }
    }


# ==================== 社交功能 ====================

@app.get("/api/social/posts")
async def social_posts(limit: int = 20):
    """获取帖子列表"""
    return {
        "success": True,
        "posts": [
            {
                "id": 1,
                "user": "钓鱼达人",
                "content": "今天在深圳湾钓了5条鲫鱼！",
                "images": [],
                "likes": 15,
                "comments": 3,
                "timestamp": "2026-03-12 10:00:00"
            },
        ]
    }


@app.get("/api/social/trending")
async def social_trending(period: str = "week"):
    """获取热门帖子"""
    return {
        "success": True,
        "posts": [
            {
                "id": 1,
                "user": "钓鱼大师",
                "content": "分享一个钓鲫鱼的秘诀...",
                "likes": 128,
                "comments": 45,
                "timestamp": "2026-03-10 15:00:00"
            },
        ]
    }


# ==================== 无人船控制 ====================

@app.get("/api/drone/status")
async def drone_status(device_id: str):
    """获取无人船状态"""
    return {
        "success": True,
        "device_id": device_id,
        "status": "online",
        "battery": 85,
        "location": {"lat": 22.5, "lon": 114.0},
        "speed": 2.5,
        "depth": 3.2
    }


@app.get("/api/drone/history")
async def drone_history(device_id: str, hours: int = 24):
    """获取无人船历史数据"""
    return {
        "success": True,
        "device_id": device_id,
        "data": [
            {"timestamp": "2026-03-12 10:00:00", "battery": 90, "depth": 3.0},
            {"timestamp": "2026-03-12 11:00:00", "battery": 85, "depth": 3.5},
        ]
    }


# ==================== 健康检查 ====================

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "services": {
            "coach": "available",
            "fish": "available",
            "weather": "available",
            "spots": "available",
            "catch": "available",
            "social": "available",
            "drone": "available"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
