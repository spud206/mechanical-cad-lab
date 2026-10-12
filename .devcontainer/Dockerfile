FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

ARG DEBIAN_FRONTEND=noninteractive
ARG NODE_MAJOR=22

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential ca-certificates curl wget git git-lfs gh jq unzip zip \
    locales tzdata graphviz imagemagick xvfb mesa-utils libgl1 libglib2.0-0 \
    libxrender1 libxext6 libsm6 libx11-6 libglu1-mesa \
    && sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen \
    && sed -i '/nl_NL.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen \
    && ln -snf /usr/share/zoneinfo/Europe/Amsterdam /etc/localtime \
    && echo Europe/Amsterdam > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    TZ=Europe/Amsterdam \
    CONDA_DIR=/opt/conda \
    PATH=/opt/conda/bin:/opt/conda/envs/cad/bin:${PATH}

RUN arch="$(uname -m)"; \
    case "$arch" in \
      x86_64) mf_arch="x86_64" ;; \
      aarch64|arm64) mf_arch="aarch64" ;; \
      *) echo "Unsupported architecture: $arch" >&2; exit 1 ;; \
    esac; \
    curl -fsSL "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-${mf_arch}.sh" -o /tmp/miniforge.sh; \
    bash /tmp/miniforge.sh -b -p /opt/conda; \
    rm /tmp/miniforge.sh; \
    /opt/conda/bin/conda config --system --set channel_priority strict

COPY environment.yml /tmp/environment.yml
RUN /opt/conda/bin/mamba env create -f /tmp/environment.yml \
    && /opt/conda/bin/conda clean -afy \
    && rm /tmp/environment.yml \
    && chown -R vscode:vscode /opt/conda

RUN curl -fsSL https://deb.nodesource.com/setup_${NODE_MAJOR}.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && npm install -g @openai/codex \
    && npm cache clean --force \
    && rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "-lc"]
RUN echo 'source /opt/conda/etc/profile.d/conda.sh && conda activate cad' >> /home/vscode/.bashrc \
    && echo 'export TZ=Europe/Amsterdam LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8' >> /home/vscode/.bashrc

# Writable Codex home for the isolated, persistent container volume.
RUN mkdir -p /home/vscode/.codex && chown -R vscode:vscode /home/vscode/.codex
