# aichatbot

一个基于 LangChain 和 Telegram 的 AI 聊天机器人，支持天气查询功能。

## 功能

- 通过 Telegram 与 AI 对话
- 使用工具调用（Tool Calling）查询实时天气
- 支持 OpenAI 及所有兼容 OpenAI 格式的第三方大模型服务商（DeepSeek、Together AI、Moonshot 等）

---

## 配置说明

项目使用 `config.yaml` 进行配置。复制下方模板并填入你的密钥：

```yaml
server:
  name: "aichatbot"
  description: "AI Chatbot Server"

telegram:
  token: "YOUR_TELEGRAM_BOT_TOKEN"   # 从 @BotFather 获取

llm:
  # 若使用第三方兼容 OpenAI 格式的服务商，填写其 API 基础 URL；
  # 使用官方 OpenAI 则留空或删除此行。
  api_url: ""                         # 例：https://api.deepseek.com/v1
  model: "gpt-4o-mini"               # 模型名称，如 deepseek-chat
  api_key: "YOUR_LLM_API_KEY"        # 对应服务商的 API Key
  temperature: 0.7
  max_tokens: 1000

weather:
  api_key: "YOUR_OPENWEATHERMAP_API_KEY"  # 从 openweathermap.org 获取
```

配置中的值也可以引用环境变量，例如：

```yaml
telegram:
  token: "$TELEGRAM_TOKEN"
llm:
  api_key: "$LLM_API_KEY"
```

启动时设置对应的环境变量即可，无需将密钥写入文件。

---

## 安装与启动

### 前置要求

- Python 3.11+
- [uv](https://github.com/astral-sh/uv)（推荐）或 pip

### 使用 uv（推荐）

```bash
# 1. 克隆项目
git clone https://github.com/BetaCat76/aichatbot.git
cd aichatbot

# 2. 安装依赖
uv sync

# 3. 填写配置
cp config.yaml config.yaml   # 直接编辑 config.yaml，填入各项密钥

# 4. 启动
uv run aichatbot
```

### 使用 pip

```bash
# 1. 克隆项目
git clone https://github.com/BetaCat76/aichatbot.git
cd aichatbot

# 2. 创建并激活虚拟环境
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. 安装依赖
pip install -e .

# 4. 填写配置（编辑 config.yaml）

# 5. 启动
aichatbot
```

也可通过环境变量指定配置文件路径：

```bash
CONFIG_PATH=/path/to/my-config.yaml aichatbot
```

---

## 第三方大模型服务商示例

| 服务商 | api_url | 模型名称示例 |
|---|---|---|
| OpenAI（官方） | （留空） | `gpt-4o-mini` |
| DeepSeek | `https://api.deepseek.com/v1` | `deepseek-chat` |
| Moonshot (Kimi) | `https://api.moonshot.cn/v1` | `moonshot-v1-8k` |
| Together AI | `https://api.together.xyz/v1` | `meta-llama/Llama-3-8b-chat-hf` |
| 阿里云百炼 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-turbo` |
