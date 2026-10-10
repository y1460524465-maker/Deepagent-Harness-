# 使用Node.js 24作为基础镜像
FROM node:24-alpine

# 设置工作目录
WORKDIR /app

# 换用国内 npm 镜像源（registry.npmjs.org 在国内拉包会超时）
# 写在安装 pnpm 之前，这样 npm 和 pnpm 都会用它
RUN npm config set registry https://registry.npmmirror.com

# 安装 pnpm：版本必须与 package.json 里的 "packageManager": "pnpm@10.5.1" 一致。
# 否则 pnpm 会自动"切换版本"，去下载 @pnpm/exe 的原生二进制，
# 而它没有 linux-x64-musl 构建，在 Alpine 上会报 ERR_PNPM_PNPM_ENGINE_NO_NATIVE_BINARY。
RUN npm install -g pnpm@10.5.1

# 双保险：关闭 pnpm 的自动版本切换
ENV npm_config_manage_package_manager_versions=false

# 复制项目文件
COPY . .

# 安装依赖
RUN pnpm install --frozen-lockfile

# 构建生产版本
RUN pnpm build


# 启动应用
CMD ["pnpm", "start"]
