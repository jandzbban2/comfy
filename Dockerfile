# Base image: Official RunPod Serverless ComfyUI worker
FROM runpod/worker-comfyui:5.8.6-base

WORKDIR /comfyui

# 1. Install system utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    git \
    aria2 \
    && rm -rf /var/lib/apt/lists/*

# 2. Update ComfyUI core to v0.34.2 matching local desktop setup exactly
RUN git fetch --all --tags && \
    git checkout 169fcf35 || true

# 3. Install all Custom Nodes matching your local setup exactly
WORKDIR /comfyui/custom_nodes
RUN git clone https://github.com/chrisgoringe/cg-use-everywhere.git && \
    git clone https://github.com/kijai/ComfyUI-KJNodes.git && \
    git clone https://github.com/rgthree/rgthree-comfy.git && \
    git clone https://github.com/yolain/ComfyUI-Easy-Use.git && \
    git clone https://github.com/WASasquatch/was-node-suite-comfyui.git && \
    git clone https://github.com/chflame163/ComfyUI_LayerStyle.git && \
    git clone https://github.com/alexopus/ComfyUI-Image-Saver.git && \
    git clone https://github.com/ltdrdata/ComfyUI-Impact-Pack.git && \
    git clone https://github.com/capitan01R/ComfyUI-Krea2T-Enhancer.git && \
    git clone https://github.com/Azornes/Comfyui-Resolution-Master.git && \
    git clone https://github.com/ClownsharkBatwing/RES4LYF.git && \
    git clone https://github.com/pythongosssss/ComfyUI-Custom-Scripts.git && \
    git clone https://github.com/PGCRT/CRT-Nodes.git

# 4. Install all 204 exact dependencies exported from your working local setup
COPY requirements_custom.txt /tmp/requirements_custom.txt
RUN pip install --no-cache-dir -r /tmp/requirements_custom.txt || true

# 5. Apply fault-tolerant node initialization patches
COPY patches/layerstyle_init.py /comfyui/custom_nodes/ComfyUI_LayerStyle/__init__.py
COPY patches/crt_nodes_init.py /comfyui/custom_nodes/CRT-Nodes/__init__.py

# 6. Copy fast model downloader and entrypoint script
COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /

ENTRYPOINT ["/entrypoint.sh"]
