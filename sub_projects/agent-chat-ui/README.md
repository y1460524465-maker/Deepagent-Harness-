## Agent Chat UI

该项目基于 [langchain-ai/agent-chat-ui](https://github.com/langchain-ai/agent-chat-ui) 做了少量自定义的修改。

启动方式与详细介绍可参阅 [README_OLD.md](README_OLD.md)

## 改动处

1. 原来仅可接收 pdf 与图片文件，改为可接收所有文件。
2. 替换了 logo 与标题。
3. 界面文案由英文改为中文。

## 自定义标题

在 `src/config.ts` 中修改 `APP_CONFIG.name` 的值即可。

## 自定义 Logo

将 logo 图片放入 `public/` 目录（当前使用 `public/logo.png`），再修改
`src/components/icons/langgraph.tsx` 中 `img` 标签的 `src` 即可。

组件会按调用方传入的 `className`（如 `h-8`）或 `width` / `height` 自适应缩放，
因此只需替换图片文件，无需改动其他页面代码。
