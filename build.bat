@echo off
REM Build script for Cultivation World Simulator (Windows)
REM 修仙世界模拟器构建脚本 (Windows版本)

echo ==================================
echo 修仙世界模拟器 构建脚本
echo Cultivation World Simulator Build Script
echo ==================================
echo.

REM Step 1: Check Python
echo [INFO] Checking Python...
python --version
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.10+
    pause
    exit /b 1
)

REM Step 2: Install PyInstaller
echo [INFO] Installing PyInstaller...
pip install --upgrade pyinstaller

REM Step 3: Install dependencies
echo [INFO] Installing project dependencies...
pip install -r requirements.txt

REM Step 4: Build frontend
where npm >nul 2>nul
if %errorlevel% == 0 (
    echo [INFO] Building frontend...
    cd web
    if not exist "node_modules" (
        echo [INFO] Installing frontend dependencies...
        call npm install
    )
    echo [INFO] Building Vue frontend...
    call npm run build
    cd ..
    echo [INFO] Frontend build complete!
) else (
    echo [WARNING] Node.js not found. Skipping frontend build.
    echo [WARNING] Please build frontend manually with: cd web && npm run build
)

REM Step 5: Clean previous builds
echo [INFO] Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

REM Step 6: Run PyInstaller
echo [INFO] Running PyInstaller...
if exist "cultivation-simulator.spec" (
    pyinstaller cultivation-simulator.spec --clean
) else (
    echo [ERROR] cultivation-simulator.spec not found!
    pause
    exit /b 1
)

REM Step 7: Verify build
if exist "dist\CultivationWorldSimulator" (
    echo [INFO] Build successful!
    echo [INFO] Executable location: dist\CultivationWorldSimulator\
    
    REM Create a run batch file
    echo @echo off > dist\CultivationWorldSimulator\run.bat
    echo cd /d "%%~dp0" >> dist\CultivationWorldSimulator\run.bat
    echo start CultivationWorldSimulator.exe >> dist\CultivationWorldSimulator\run.bat
    
    REM Create README
    echo 修仙世界模拟器 (Cultivation World Simulator) > dist\CultivationWorldSimulator\README.txt
    echo ============================================== >> dist\CultivationWorldSimulator\README.txt
    echo. >> dist\CultivationWorldSimulator\README.txt
    echo 运行说明 (How to Run): >> dist\CultivationWorldSimulator\README.txt
    echo 双击 run.bat 或 CultivationWorldSimulator.exe >> dist\CultivationWorldSimulator\README.txt
    echo. >> dist\CultivationWorldSimulator\README.txt
    echo 配置说明 (Configuration): >> dist\CultivationWorldSimulator\README.txt
    echo - 游戏配置位于 static\local_config.yml >> dist\CultivationWorldSimulator\README.txt
    echo - 首次运行请配置 LLM API 密钥 >> dist\CultivationWorldSimulator\README.txt
    echo. >> dist\CultivationWorldSimulator\README.txt
    echo 访问地址 (Access): >> dist\CultivationWorldSimulator\README.txt
    echo - 前端界面: http://localhost:8123 >> dist\CultivationWorldSimulator\README.txt
    echo - 后端 API: http://localhost:8002 >> dist\CultivationWorldSimulator\README.txt
    echo. >> dist\CultivationWorldSimulator\README.txt
    echo 更多信息请访问项目主页: >> dist\CultivationWorldSimulator\README.txt
    echo https://github.com/AI-Cultivation/cultivation-world-simulator >> dist\CultivationWorldSimulator\README.txt
    
    echo.
    echo ==================================
    echo 构建完成！Build Complete!
    echo ==================================
    echo 可执行文件位于: dist\CultivationWorldSimulator\
    echo 运行方式: 进入文件夹后双击 run.bat
    echo.
) else (
    echo [ERROR] Build failed! Executable not found.
    pause
    exit /b 1
)

pause
