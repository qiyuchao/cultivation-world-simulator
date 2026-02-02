#!/bin/bash
# Build script for Cultivation World Simulator
# 修仙世界模拟器构建脚本

set -e  # Exit on error

echo "=================================="
echo "修仙世界模拟器 构建脚本"
echo "Cultivation World Simulator Build Script"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Step 1: Check Python version
print_info "Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
print_info "Python version: $python_version"

# Step 2: Install/upgrade PyInstaller
print_info "Installing PyInstaller..."
pip install --upgrade pyinstaller

# Step 3: Install project dependencies
print_info "Installing project dependencies..."
pip install -r requirements.txt

# Step 4: Build frontend (if Node.js is available)
if command -v npm &> /dev/null; then
    print_info "Building frontend..."
    cd web
    if [ ! -d "node_modules" ]; then
        print_info "Installing frontend dependencies..."
        npm install
    fi
    print_info "Building Vue frontend..."
    npm run build
    cd ..
    print_info "Frontend build complete!"
else
    print_warning "Node.js not found. Skipping frontend build."
    print_warning "Please build frontend manually with: cd web && npm run build"
fi

# Step 5: Clean previous builds
print_info "Cleaning previous builds..."
rm -rf build dist

# Step 6: Run PyInstaller
print_info "Running PyInstaller..."
if [ -f "cultivation-simulator.spec" ]; then
    pyinstaller cultivation-simulator.spec --clean
else
    print_error "cultivation-simulator.spec not found!"
    exit 1
fi

# Step 7: Verify build
if [ -d "dist/CultivationWorldSimulator" ]; then
    print_info "Build successful!"
    print_info "Executable location: dist/CultivationWorldSimulator/"
    
    # Create a run script
    cat > dist/CultivationWorldSimulator/run.sh << 'EOF'
#!/bin/bash
# Run Cultivation World Simulator
cd "$(dirname "$0")"
./CultivationWorldSimulator
EOF
    chmod +x dist/CultivationWorldSimulator/run.sh
    
    # Create README for distribution
    cat > dist/CultivationWorldSimulator/README.txt << 'EOF'
修仙世界模拟器 (Cultivation World Simulator)
==============================================

运行说明 (How to Run):
1. Linux/Mac: 执行 ./run.sh 或 ./CultivationWorldSimulator
2. Windows: 双击 CultivationWorldSimulator.exe

配置说明 (Configuration):
- 游戏配置位于 static/local_config.yml
- 首次运行请配置 LLM API 密钥

访问地址 (Access):
- 前端界面: http://localhost:8123
- 后端 API: http://localhost:8002

更多信息请访问项目主页:
https://github.com/AI-Cultivation/cultivation-world-simulator
EOF
    
    print_info ""
    print_info "=================================="
    print_info "构建完成！Build Complete!"
    print_info "=================================="
    print_info "可执行文件位于: dist/CultivationWorldSimulator/"
    print_info "运行方式: cd dist/CultivationWorldSimulator && ./run.sh"
    print_info ""
else
    print_error "Build failed! Executable not found."
    exit 1
fi
