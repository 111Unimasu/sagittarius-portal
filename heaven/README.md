# Sagittarius Heaven ⚖️

基于 AI 的置信度裁定工具。输入环境背景、人物设定和人物发言，AI 将交叉分析并输出完整的置信度裁定报告。

## 功能

- 🎯 置信度评分与等级判定（虚假→高度可信）
- 🔍 深度交叉分析过程
- 📋 多维度裁定理由
- 💡 可操作建议
- 🔮 多场景概率预测（概率总和100%）

## 技术栈

- **后端**：Flask + OpenAI Python SDK
- **前端**：原生 HTML/CSS/JS（星空主题）
- **AI**：DeepSeek（OpenAI API 兼容）

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置 API
cp .env.example .env
# 编辑 .env，填入你的 DeepSeek API Key

# 3. 启动
python app.py
```

访问 http://localhost:5000

## 项目结构

```
├── app.py              # Flask 后端
├── index.html          # 前端页面
├── requirements.txt    # Python 依赖
├── .env.example        # 环境变量模板
└── .gitignore
```

## License

MIT
