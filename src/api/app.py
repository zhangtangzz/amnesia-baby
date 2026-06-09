"""
FastAPI应用

负责创建和配置FastAPI应用
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 创建FastAPI应用
app = FastAPI(
    title="失忆宝宝 API",
    description="数字人格重建系统 API",
    version="1.0.0",
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """根路径"""
    return {"message": "失忆宝宝 API"}


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}
