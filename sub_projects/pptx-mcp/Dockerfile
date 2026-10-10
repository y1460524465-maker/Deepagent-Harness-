FROM python:3.12-bullseye
# 设置阿里云镜像源
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list

# 删除 debian-security 源：Debian 11 (bullseye) 已于 2026-08-31 EOL，
# 安全仓库的索引永久过期、包文件也已被镜像站清理，留着会导致 apt 下载 404。
# LibreOffice 所需依赖在 bullseye main / bullseye-updates 里都有（已核对）。
RUN sed -i '/debian-security/d' /etc/apt/sources.list

# 安装最小化的 LibreOffice
RUN apt-get -o Acquire::Check-Valid-Until=false update && apt-get install -y --no-install-recommends \
    libreoffice-core \
    libreoffice-writer \
    libreoffice-impress \
    libreoffice-common \
    fonts-dejavu \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -e . -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
CMD ["python", "server.py"]