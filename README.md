# 🔮 AI 八字测算小程序

根据生日生成八字四柱，调用 DeepSeek AI 进行命理解读。

## 项目结构

```
bazi-fortune/
├── backend/
│   ├── main.py          # FastAPI 后端入口
│   ├── bazi_calc.py     # 八字计算（lunar-python）
│   ├── ai_analyzer.py   # AI 解读（DeepSeek）
│   ├── requirements.txt # Python 依赖
│   └── .env.example     # 环境变量模板
└── frontend/
    └── index.html       # 单页前端（无需构建）
```

## 快速启动

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置 API Key

```bash
cp .env.example .env
# 编辑 .env，填入你的 DeepSeek API Key
# 申请地址：https://platform.deepseek.com/
```

### 3. 启动后端

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

API 文档：http://localhost:8000/docs

### 4. 打开前端

直接用浏览器打开 `frontend/index.html`，或部署到任意静态托管。

> 注意：前端 `index.html` 中的 `API_BASE` 默认指向 `http://localhost:8000`，
> 部署时需改为实际服务器地址。

## 部署到服务器

### 后端（腾讯云/阿里云轻量服务器）

```bash
# 安装依赖
pip install -r requirements.txt

# 后台运行（使用 nohup 或 screen）
nohup uvicorn main:app --host 0.0.0.0 --port 8000 &

# 或者用 systemd 管理服务（推荐）
```

### 前端（Cloudflare Pages / Vercel / GitHub Pages）

1. 修改 `index.html` 中 `API_BASE` 为你的服务器地址
2. 上传 `index.html` 到任意静态托管
3. 分享链接给实习生圈！

## API 接口

### POST /fortune

请求：
```json
{
  "year": 1999,
  "month": 8,
  "day": 15,
  "hour": 10,
  "name": "小明",
  "question": "今年适合跳槽吗？"
}
```

响应：
```json
{
  "success": true,
  "bazi": {
    "年柱": "己卯",
    "月柱": "甲申",
    "日柱": "丁酉",
    "时柱": "戊午",
    ...
  },
  "analysis": "🌟 命格概述 ..."
}
```

## 费用估算

- DeepSeek API：约 0.001 元/次请求
- 1000 人使用：约 1 元
- 服务器：腾讯云轻量 24 元/月（或用免费额度）
