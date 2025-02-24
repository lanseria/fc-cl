## 安装Cmake
```sh
这个错误提示说明在构建 dlib 的 wheel 时，找不到合法的 CMake 安装。也就是说，dlib 在构建过程中依赖于 CMake，而你当前系统中可能没有安装官方的 CMake，或者安装的 CMake 存在问题（例如被 pip、conda 等非官方来源安装的版本覆盖）。

要解决这个问题，你可以按照以下步骤改进：

1. 确认是否已经安装了官方 CMake：
   - 在终端或命令行中执行：
     ```bash
     cmake --version
     ```
     如果提示命令不存在或者版本不正确，则需要安装或更新 CMake。

2. 根据操作系统安装官方 CMake：
   - **Windows**：前往 [cmake.org](https://cmake.org/download/) 下载最新版的 Windows 安装包，并确保在安装过程中选择“Add CMake to the system PATH”。
   - **Linux (Ubuntu/Debian)**：使用 apt 安装：
     ```bash
     sudo apt update
     sudo apt install cmake
     ```
   - **macOS**：可以使用 Homebrew 安装：
     ```bash
     brew install cmake
     ```

3. 确保安装后 CMake 在你的 PATH 中，以便 dlib 构建过程中能够正确调用官方版本。

4. 清理可能存在的 pip/conda 内置的（可能是错误的）CMake 副本，防止冲突。

5. 重新构建项目或重新运行 pip install 命令。

通过确保系统中安装官方的 CMake 并正确配置环境路径，构建 dlib 的过程应该能够顺利进行。
```

## 使用示例

```sh
# 创建虚拟环境（venv 是 Python 内置工具）
python3 -m venv fc-cl
# macOS/Linux
source fc-cl/bin/activate

# Windows (PowerShell)
.\fc-cl\Scripts\Activate.ps1
# 安装工具
pip install .

# 基础使用
face-compare person1.jpg person2.jpg

# 自定义阈值
face-compare photoA.png photoB.jpg -t 0.7

# 输出示例
Similarity Score: 89.34%
Match Result: MATCH (Threshold: 0.7)
```
