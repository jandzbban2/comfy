#!/bin/bash
set -e

echo "=== 1. Checking & Downloading Model Weights ==="
mkdir -p /comfyui/models/diffusion_models \
         /comfyui/models/text_encoders \
         /comfyui/models/vae \
         /comfyui/models/checkpoints

# 1. Download VAE if not present (~250 MB)
if [ ! -f "/comfyui/models/vae/qwen_image_vae.safetensors" ]; then
    echo "Downloading Qwen Image VAE..."
    aria2c -x 16 -s 16 -k 1M --summary-interval=5 \
        "https://huggingface.co/Comfy-Org/Krea-2/resolve/main/vae/qwen_image_vae.safetensors" \
        -d /comfyui/models/vae -o qwen_image_vae.safetensors
fi

# 2. Download Text Encoder if not present (~4.5 GB)
if [ ! -f "/comfyui/models/text_encoders/qwen3vl_4b_fp8_scaled.safetensors" ] && [ ! -f "/comfyui/models/text_encoders/qwen3vl-4b-abliterated_fp8_e4m3fn.safetensors" ]; then
    echo "Downloading Qwen3-VL 4B FP8 Text Encoder..."
    aria2c -x 16 -s 16 -k 1M --summary-interval=5 \
        "https://huggingface.co/Comfy-Org/Krea-2/resolve/main/text_encoders/qwen3vl_4b_fp8_scaled.safetensors" \
        -d /comfyui/models/text_encoders -o qwen3vl-4b-abliterated_fp8_e4m3fn.safetensors
    ln -sf /comfyui/models/text_encoders/qwen3vl-4b-abliterated_fp8_e4m3fn.safetensors \
           /comfyui/models/text_encoders/qwen3vl_4b_fp8_scaled.safetensors
fi

# 3. Download Diffusion Model if not present (~13.5 GB)
if [ ! -f "/comfyui/models/diffusion_models/museByStableYogi_v35Int8Extended.safetensors" ]; then
    echo "Downloading Muse v3.5 Int8 Diffusion Model from Civitai..."
    aria2c -x 16 -s 16 -k 1M --summary-interval=5 \
        --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)" \
        "https://civitai.com/api/download/models/3258954?fileId=3142504&token=8e728b6705b6a2650183d127a74a3644" \
        -d /comfyui/models/diffusion_models -o museByStableYogi_v35Int8Extended.safetensors
fi

echo "=== All models ready! Executing RunPod Serverless startup script ==="
exec /start.sh "$@"
