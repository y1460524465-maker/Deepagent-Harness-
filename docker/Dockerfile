FROM langchain/langgraph-api:3.11

# 非交互式安装，避免时区等交互提示
ENV DEBIAN_FRONTEND=noninteractive

# ========= 1. 配置 Debian 镜像源（阿里云；基础镜像是 Debian trixie）========
# 说明：清华源对部分网络返回 403，故改用阿里云。
# 用 grep 先校验"确实匹配到了"，避免"sed 没匹配也返回 0"导致换源静默失败。
# 版本号从 /etc/os-release 动态读取，不写死（基础镜像是 trixie，不是 bookworm）。
RUN set -eux; \
    rm -rf /var/lib/apt/lists/*; \
    replaced=0; \
    for f in /etc/apt/sources.list.d/debian.sources /etc/apt/sources.list; do \
        if [ -f "$f" ] && grep -qE 'deb\.debian\.org|security\.debian\.org' "$f"; then \
            sed -i 's|http://|https://|g; s|deb\.debian\.org|mirrors.aliyun.com|g; s|security\.debian\.org|mirrors.aliyun.com|g' "$f"; \
            replaced=1; \
        fi; \
    done; \
    if [ "$replaced" = "0" ]; then \
        . /etc/os-release; \
        codename="${VERSION_CODENAME:-trixie}"; \
        printf 'deb https://mirrors.aliyun.com/debian/ %s main contrib non-free non-free-firmware\n' "$codename" > /etc/apt/sources.list; \
        printf 'deb https://mirrors.aliyun.com/debian/ %s-updates main contrib non-free non-free-firmware\n' "$codename" >> /etc/apt/sources.list; \
        printf 'deb https://mirrors.aliyun.com/debian-security/ %s-security main contrib non-free non-free-firmware\n' "$codename" >> /etc/apt/sources.list; \
        rm -f /etc/apt/sources.list.d/debian.sources; \
    fi

# ========= 2. 系统依赖合并为一条（含 PDF 引擎 + 中文字体）========
RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends --fix-missing \
        curl \
        pandoc \
        texlive-xetex \
        texlive-latex-base \
        texlive-fonts-recommended \
        lmodern \
        fonts-wqy-microhei \
        fonts-wqy-zenhei \
        texlive-lang-chinese \
        fonts-noto-cjk \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# ========= 3. 复制项目源码 =========
# -- Adding non-package dependency selfdrive --
# ⚠️ 必须放在系统依赖之后：这样以后改代码/requirements.txt 时，
#    上面那层 texlive 安装（最慢，十几分钟）能命中缓存，只重跑下面的 pip。
ADD . /deps/outer-selfdrive/src

# ========= 4. 安装 Python 依赖 =========
RUN pip install -r /deps/outer-selfdrive/src/requirements.txt \
    -i https://mirrors.aliyun.com/pypi/simple/ \
    --trusted-host mirrors.aliyun.com

RUN set -ex && \
    for line in '[project]' \
                'name = "selfdrive"' \
                'version = "0.1"' \
                '[tool.setuptools.package-data]' \
                '"*" = ["**/*"]' \
                '[build-system]' \
                'requires = ["setuptools>=61"]' \
                'build-backend = "setuptools.build_meta"'; do \
        echo "$line" >> /deps/outer-selfdrive/pyproject.toml; \
    done
# -- End of non-package dependency selfdrive --

# -- Installing all local dependencies --
RUN for dep in /deps/*; do             echo "Installing $dep";             if [ -d "$dep" ]; then                 echo "Installing $dep";                 (cd "$dep" && PYTHONDONTWRITEBYTECODE=1 uv pip install --system --no-cache-dir -c /api/constraints.txt -e .);             fi;         done
# -- End of local dependencies install --

# 图入口（和你的 langgraph.json 一致，指向 all_agent.py）
ENV LANGSERVE_GRAPHS='{"agent": "/deps/outer-selfdrive/src/all_agent.py:agent"}'

# -- Ensure user deps didn't inadvertently overwrite langgraph-api
RUN mkdir -p /api/langgraph_api /api/langgraph_runtime /api/langgraph_license && touch /api/langgraph_api/__init__.py /api/langgraph_runtime/__init__.py /api/langgraph_license/__init__.py
RUN PYTHONDONTWRITEBYTECODE=1 uv pip install --system --no-cache-dir --no-deps -e /api

# ！！为了让 Agent 运行时更强大，不要删除 pip 和 setuptools
# ！！项目中的 excel-mcp 用到了 uv，所以保留 uv

WORKDIR /deps/outer-selfdrive/src
