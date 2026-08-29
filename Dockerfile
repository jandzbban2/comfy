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

# 2. Install all Custom Nodes matching your local setup exactly
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

# Install python dependencies for custom nodes
RUN pip install --no-cache-dir \
    torchvision \
    opencv-contrib-python \
    scikit-image \
    scikit-learn \
    colour-science \
    matplotlib \
    spandrel \
    scipy \
    timm \
    transformers \
    accelerate \
    pywavelets \
    diffusers \
    peft \
    sentencepiece \
    color-matcher \
    pymatting \
    blend_modes \
    loguru \
    ultralytics \
    einops \
    rotary-embedding-torch \
    soundfile \
    imageio-ffmpeg \
    huggingface_hub \
    tqdm \
    piexif \
    wordcloud \
    librosa

RUN for req in /comfyui/custom_nodes/*/requirements.txt; do [ -f "$req" ] && pip install --no-cache-dir -r "$req"; done || true

# Apply fault-tolerant node initialization patches
COPY patches/layerstyle_init.py /comfyui/custom_nodes/ComfyUI_LayerStyle/__init__.py
COPY patches/crt_nodes_init.py /comfyui/custom_nodes/CRT-Nodes/__init__.py

# 3. Create model directory structure
RUN mkdir -p /comfyui/models/diffusion_models \
             /comfyui/models/text_encoders \
             /comfyui/models/vae \
             /comfyui/models/checkpoints

# 4. Download Krea 2 / Muse models directly into image layers (Fast multi-connection via aria2)

# VAE: Qwen Image VAE (~250 MB)
RUN aria2c -x 16 -s 16 -k 1M \
    "https://huggingface.co/Comfy-Org/Krea-2/resolve/main/vae/qwen_image_vae.safetensors" \
    -d /comfyui/models/vae -o qwen_image_vae.safetensors

# Text Encoder: Qwen3-VL 4B FP8 (Saved as both abliterated and standard names)
RUN aria2c -x 16 -s 16 -k 1M \
    "https://huggingface.co/Comfy-Org/Krea-2/resolve/main/text_encoders/qwen3vl_4b_fp8_scaled.safetensors" \
    -d /comfyui/models/text_encoders -o qwen3vl-4b-abliterated_fp8_e4m3fn.safetensors && \
    ln -s /comfyui/models/text_encoders/qwen3vl-4b-abliterated_fp8_e4m3fn.safetensors \
          /comfyui/models/text_encoders/qwen3vl_4b_fp8_scaled.safetensors

# Diffusion Model: Muse by Stable Yogi v3.5 Int8 (~13.5 GB) using your Civitai Token
RUN aria2c -x 16 -s 16 -k 1M \
    --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)" \
    "https://civitai.com/api/download/models/3258954?fileId=3142504&token=8e728b6705b6a2650183d127a74a3644" \
    -d /comfyui/models/diffusion_models -o museByStableYogi_v35Int8Extended.safetensors

WORKDIR /

# The base runpod image provides the start script / handler
CMD ["/start.sh"]
