from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core.config import settings
from app.core.database import engine
from app.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时：创建数据库表
    db_path = Path("./data")
    db_path.mkdir(exist_ok=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print(f"✓ Database initialized at {settings.DATABASE_URL}")

    yield

    # 关闭时：释放数据库连接
    await engine.dispose()
    print("✓ Database connection closed")


app = FastAPI(
    title=settings.APP_NAME,
    description="AI饮食助手 API",
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router)


@app.get("/")
async def root():
    """根路径"""
    return {"message": "Welcome to Aqua API"}


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "app_name": settings.APP_NAME
    }
