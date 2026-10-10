# 自驱 · 通用智能体

![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Docker](https://img.shields.io/badge/docker-required-blue.svg)

![main](assets/main.png)

**自驱（SelfDrive）** 是一个自规划、自执行、自交付的通用智能体。它不为某个单一业务写死流程，而是把「理解目标 → 拆解任务 → 调度工具 → 产出交付物」整条链路交给模型自己驱动：用户只在前端描述想要的结果，剩下的由它完成。

---

## 项目简介

自驱基于 **LangChain 1.0 + LangGraph + DeepAgents** 构建。它没有采用传统的「一问一答 + 单次函数调用」模式，而是装配出一个具备**长期自主执行能力**的深度智能体：可以自己规划步骤、反复调用工具、读写文件、派生专项子代理，直到任务真正完成才停止。

在智能体之外，工程侧用一层**中间件**承载横切关注点（会话文件隔离、路径虚拟化、限流重试、终端执行、产物交付），因此多用户、多会话、多产物并行时依然可管可控。

## 核心能力

### 自主执行

- **任务规划**：面对长链路需求自行拆解步骤并跟踪进度，而不是只做一次回答
- **工具调用**：按需选择工具并串联调用，形成完整的执行链路
- **多轮上下文**：跨轮次保持任务上下文，支持长任务的持续推进
- **子代理调度**：把 PPT、Excel 等专项任务交给子代理，主智能体负责编排

### 内容与文件

- 接收并解析图片、PDF、Word、Excel、PPT 等文件
- 生成文档、表格、演示文稿等交付物并回传给用户
- 通过对象存储统一管理产物，生成可直接下载的链接

### 多模态与联网

- 图片理解（VLM）与图像生成、图像编辑
- 联网搜索（Tavily），用于需要实时信息的任务

### 可扩展

- **中间件**：自定义智能体生命周期钩子
- **子代理**：按业务挂载独立子智能体
- **MCP**：接入标准 MCP 服务扩展工具集
- **Agent Skill**：以技能包的形式热插拔领域能力

### 平台化

- 支持多用户、多会话并行使用
- 每个会话拥有独立的工作目录，文件互不可见
- 前端界面、后端服务、对象存储、数据库全部容器化交付

## 技术栈

- **Python 3.11+** — 主要开发语言
- **LangChain 1.0 / LangGraph** — 智能体运行时与工作流编排
- **DeepAgents** — 提供规划、文件系统、子代理、技能等深度智能体能力
- **LangSmith** — 可观测性，提供追踪、评估与监控
- **MCP（Model Context Protocol）** — 工具接入协议
- **Agent Skill** — 可插拔技能模块
- **PostgreSQL（pgvector）** — 状态与检查点存储
- **MinIO** — 对象存储，管理文件与产物
- **Redis** — 缓存、会话与消息队列
- **Next.js + React** — 对话式前端界面
- **Docker & Docker Compose** — 容器化部署
- **SiliconFlow API** — 大模型服务（LLM / VLM / 图像生成）
- **Tavily Search** — 联网搜索

## 目录结构

```text
├── base/                 # 基础配置
├── conn/                 # 连接层（LLM、对象存储等）
├── content/              # 核心实现
│   ├── mcps/             # MCP 接入
│   ├── middles/          # 中间件
│   ├── mytools/          # 自定义工具
│   ├── others/           # 文件系统后端等服务实现
│   ├── skills/           # 初始技能目录
│   ├── subagents/        # 子代理
│   └── utils/            # 工具函数
├── sub_projects/
│   ├── agent-chat-ui/    # 前端对话界面
│   └── pptx-mcp/         # PPT 处理服务
├── docker/               # 镜像与编排配置
├── utils/                # 通用工具
├── all_agent.py          # 智能体入口
└── langgraph.json        # 服务图定义
```

## 快速开始

### 1. 准备配置

进入 `docker` 目录，复制环境变量模板：

```shell
cd docker
cp .env.example .env
```

然后填写 `.env` 中的必要项（模板文件内有逐项说明：[英文版](docker/.env.example) / [中文版](docker/.env.example.zh)）：

| 变量 | 必填 | 说明 |
| --- | --- | --- |
| `OPENAI_API_KEY` | 是 | 硅基流动 API 密钥，用于访问模型服务，注册地址：https://cloud.siliconflow.cn |
| `LANGSMITH_API_KEY` | 是 | LangSmith API 密钥，用于链路追踪与监控，注册地址：https://www.langsmith.com |
| `HOST_IP` | 是 | 服务器对外可访问的 IP 或域名，**不能填 `localhost` 或 `127.0.0.1`** |
| `TAVILY_SEARCH_KEY` | 否 | 填写后启用联网搜索，注册地址：https://tavily.com |

### 2. 启动服务

从源码构建并启动（推荐，避免使用到过期的镜像）：

```shell
docker compose up -d --build
```

### 3. 访问应用

服务启动完成后，浏览器打开：

- `http://<HOST_IP>:3000` — 前端对话界面
- `http://<HOST_IP>:8000/docs` — 后端接口文档

## 配置要求

| 配置级别 | CPU | 内存 | 适用场景 |
| --- | --- | --- | --- |
| 最低配置 | 2 核 | 4GB | 个人测试（较为极限） |
| 生产环境 | 4 核+ | 8GB+ | 高并发场景 |

## 常见问题

**Q：为什么必须填写 `HOST_IP`，不能用 `localhost`？**
A：前后端运行在不同的容器中，使用 `localhost` 会导致前端无法访问后端接口，产物的下载链接也会失效。

**Q：如何查看日志排查问题？**
A：使用 `docker compose logs -f <服务名>` 查看实时日志。

**Q：如何停止和重启服务？**
A：停止使用 `docker compose down`，重启使用 `docker compose restart`。

**Q：能否关闭 PPT / Excel 能力？**
A：可以。在 `.env` 中把 `USE_PPT`、`USE_EXCEL` 设为 `false` 即可，对应的子代理与 MCP 服务不会被装载。

## 贡献指南

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feature/AmazingFeature`
3. 提交修改：`git commit -m 'Add some AmazingFeature'`
4. 推送到分支：`git push origin feature/AmazingFeature`
5. 提交 Pull Request

## 路线图

- 增加音视频处理能力
- 支持更灵活的模型配置方式
- 优化前端交互体验
- 支持在界面中自行接入 MCP 服务
- 支持在界面中自行接入 Agent Skill

## 致谢

本项目在开发过程中参考并集成了以下优秀开源项目，特此致谢：

- **Agent Chat UI** — [langchain-ai/agent-chat-ui](https://github.com/langchain-ai/agent-chat-ui)
- **pptx-mcp** — [samos123/pptx-mcp](https://github.com/samos123/pptx-mcp)
- **excel-mcp-server** — [haris-musa/excel-mcp-server](https://github.com/haris-musa/excel-mcp-server)
- **MarkItDown** — [microsoft/markitdown](https://github.com/microsoft/markitdown)

## 开源协议

本项目采用 **Apache License 2.0** 开源协议，详见 [LICENSE](LICENSE)。
