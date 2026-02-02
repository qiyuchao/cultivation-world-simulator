# EXE打包指南 (Executable Packaging Guide)

## 修仙世界模拟器 - 可执行文件构建指南

本指南详细说明如何将修仙世界模拟器打包为可独立运行的exe文件。

## 系统要求 (System Requirements)

### Windows
- Windows 10 或更高版本
- Python 3.10 或更高版本
- Node.js 16 或更高版本 (可选，用于构建前端)
- 至少 2GB 可用磁盘空间

### Linux/Mac
- Python 3.10 或更高版本
- Node.js 16 或更高版本 (可选)
- 至少 2GB 可用磁盘空间

## 快速开始 (Quick Start)

### Windows用户

1. **双击运行构建脚本**
   ```
   双击 build.bat
   ```

2. **等待构建完成**
   - 脚本会自动安装依赖
   - 构建前端（如果Node.js可用）
   - 打包可执行文件

3. **运行程序**
   ```
   cd dist\CultivationWorldSimulator
   双击 run.bat 或 CultivationWorldSimulator.exe
   ```

### Linux/Mac用户

1. **运行构建脚本**
   ```bash
   chmod +x build.sh
   ./build.sh
   ```

2. **运行程序**
   ```bash
   cd dist/CultivationWorldSimulator
   ./run.sh
   # 或
   ./CultivationWorldSimulator
   ```

## 详细步骤 (Detailed Steps)

### 步骤1: 准备环境

#### 安装Python依赖
```bash
pip install -r requirements.txt
pip install pyinstaller
```

#### 构建前端（可选但推荐）
```bash
cd web
npm install
npm run build
cd ..
```

### 步骤2: 配置打包选项

编辑 `cultivation-simulator.spec` 文件来自定义打包选项：

```python
# 添加图标（如果有）
icon='path/to/icon.ico'

# 排除不需要的模块
excludes=['pytest', 'test', 'tests', 'tkinter']

# 添加额外的数据文件
datas += [('your_data_dir', 'destination')]
```

### 步骤3: 运行PyInstaller

#### 使用spec文件打包
```bash
pyinstaller cultivation-simulator.spec --clean
```

#### 或使用命令行选项
```bash
pyinstaller src/server/main.py \
    --name CultivationWorldSimulator \
    --add-data "static:static" \
    --add-data "web/dist:web/dist" \
    --add-data "assets:assets" \
    --hidden-import src.classes.god_mode \
    --hidden-import fastapi \
    --hidden-import uvicorn \
    --onedir \
    --console
```

### 步骤4: 测试可执行文件

```bash
cd dist/CultivationWorldSimulator
./CultivationWorldSimulator  # Linux/Mac
CultivationWorldSimulator.exe  # Windows
```

访问: http://localhost:8123

## 打包选项说明 (Packaging Options)

### --onedir vs --onefile

**--onedir** (推荐)
- 生成一个包含所有依赖的文件夹
- 启动速度快
- 更新方便
- 文件大小可能较大

**--onefile**
- 生成单个可执行文件
- 便于分发
- 启动速度较慢
- 每次运行需要解压

### --console vs --windowed

**--console** (推荐用于本项目)
- 显示控制台窗口
- 方便查看日志
- 便于调试

**--windowed**
- 不显示控制台
- 适合GUI应用
- 不推荐用于服务器应用

## 常见问题 (Troubleshooting)

### 问题1: 模块导入失败

**错误**: `ModuleNotFoundError: No module named 'xxx'`

**解决方案**:
```python
# 在 spec 文件中添加 hidden imports
hiddenimports=[
    'xxx',
    'xxx.submodule',
]
```

### 问题2: 数据文件找不到

**错误**: `FileNotFoundError: [Errno 2] No such file or directory: 'static/xxx'`

**解决方案**:
```python
# 在 spec 文件中添加数据文件
datas += [
    ('static', 'static'),
    ('web/dist', 'web/dist'),
]
```

### 问题3: 构建后文件太大

**解决方案**:
1. 使用 UPX 压缩
   ```python
   upx=True,
   upx_exclude=[],
   ```

2. 排除不需要的模块
   ```python
   excludes=['pytest', 'test', 'matplotlib', 'scipy'],
   ```

3. 使用虚拟环境（只包含必要的包）

### 问题4: 前端资源加载失败

**检查**:
- 确保 web/dist 目录存在
- 检查 spec 文件中的 datas 配置
- 验证静态文件路径正确

**解决方案**:
```python
# 确保包含 web/dist
web_dist = os.path.join(project_root, 'web', 'dist')
if os.path.exists(web_dist):
    for root, dirs, files in os.walk(web_dist):
        for file in files:
            file_path = os.path.join(root, file)
            target_dir = os.path.relpath(root, project_root)
            datas.append((file_path, target_dir))
```

### 问题5: LLM配置丢失

**解决方案**:
- 确保 static/local_config.yml 包含在打包中
- 首次运行时在Web界面配置LLM
- 或手动编辑 static/local_config.yml

## 分发说明 (Distribution)

### 打包为压缩文件

**Windows**:
```cmd
cd dist
tar -czf CultivationWorldSimulator-win.zip CultivationWorldSimulator
```

**Linux/Mac**:
```bash
cd dist
tar -czf CultivationWorldSimulator-linux.tar.gz CultivationWorldSimulator
```

### 创建安装程序（高级）

可以使用以下工具创建安装程序：
- **Windows**: NSIS, Inno Setup
- **Mac**: create-dmg
- **Linux**: AppImage, Flatpak

## 性能优化 (Performance Optimization)

### 1. 减小包体积
```python
# 在 spec 文件中
excludes=[
    'pytest', 'test', 'tests',
    'tkinter', 'matplotlib',
    'scipy', 'pandas',  # 如果不需要
]
```

### 2. 加快启动速度
- 使用 --onedir 而不是 --onefile
- 启用 UPX 压缩
- 精简依赖

### 3. 优化运行时性能
- 确保 Python 代码已优化
- 使用生产模式运行
- 配置合适的日志级别

## 更新和维护 (Updates and Maintenance)

### 版本管理
```python
# 在 spec 文件中设置版本
version='2.0.0',
```

### 更新流程
1. 修改代码
2. 更新版本号
3. 重新构建
4. 测试新版本
5. 分发更新

## 最佳实践 (Best Practices)

1. **使用虚拟环境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. **测试完整流程**
   - 在干净的系统上测试
   - 验证所有功能正常
   - 检查资源文件完整

3. **提供说明文档**
   - 安装指南
   - 使用说明
   - 故障排除

4. **版本控制**
   - 标记发布版本
   - 保存构建配置
   - 记录变更日志

## 自动化构建 (Automated Build)

### 使用GitHub Actions (示例)

```yaml
name: Build Executable

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [windows-latest, ubuntu-latest, macos-latest]
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pyinstaller
    
    - name: Build executable
      run: pyinstaller cultivation-simulator.spec
    
    - name: Upload artifact
      uses: actions/upload-artifact@v2
      with:
        name: CultivationWorldSimulator-${{ matrix.os }}
        path: dist/CultivationWorldSimulator
```

## 技术支持 (Support)

如有问题，请：
1. 查看本指南的常见问题部分
2. 在GitHub上提交Issue
3. 加入QQ群讨论：1071821688

---

**最后更新**: 2026-02-02
**文档版本**: v1.0
**项目主页**: https://github.com/AI-Cultivation/cultivation-world-simulator
