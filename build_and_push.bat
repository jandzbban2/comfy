@echo off
setlocal

set /p DOCKER_USER="Enter your Docker Hub username: "
set IMAGE_NAME=%DOCKER_USER%/runpod-comfyui-krea2:latest

echo.
echo ========================================================
echo Building Docker image: %IMAGE_NAME%
echo (This will download models and pack custom nodes)
echo ========================================================
echo.

docker build -t %IMAGE_NAME% -f Dockerfile .
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Docker build failed.
    pause
    exit /b 1
)

echo.
echo ========================================================
echo Logging in to Docker Hub...
echo ========================================================
docker login

echo.
echo ========================================================
echo Pushing image to Docker Hub...
echo ========================================================
docker push %IMAGE_NAME%
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Docker push failed.
    pause
    exit /b 1
)

echo.
echo ========================================================
echo [SUCCESS] Image pushed: %IMAGE_NAME%
echo.
echo Next steps in RunPod:
echo 1. Go to Serverless -> Endpoints -> Your Endpoint (or create new)
echo 2. Set 'Container Image' to: %IMAGE_NAME%
echo 3. Container Disk: Set to 30 GB (or minimum needed for container)
echo 4. Network Volume: NONE (Leave detached / unchecked)
echo ========================================================
pause
