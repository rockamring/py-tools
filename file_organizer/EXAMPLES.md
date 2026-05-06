# 使用示例

## 示例1: 首次使用 - 预览模式

```bash
# 查看将要执行的操作，不实际移动文件
python file_organizer.py --preview
```

输出示例:
```
============================================================
游戏开发文档整理工具
============================================================
16:58:06 - INFO - 开始扫描 8 个源目录...
16:58:06 - INFO - 扫描目录: F:\luobin\book
16:58:06 - INFO -   找到 2 个支持的文件
...
16:58:06 - INFO - 扫描完成，共发现 118 个文件
16:58:06 - INFO - 开始分析文件...
16:58:13 - INFO - 分析完成
16:58:13 - INFO - 开始检测重复文件...
16:58:14 - INFO - 检测到 5 个重复文件
[模拟模式] 开始整理文件...
...

============================================================
文件整理报告
============================================================
生成时间: 2026-05-06 16:58:14

统计信息:
  总文件数: 118
  已整理: 113
  重复文件: 5
  归档文件: 2
  待分类: 44

============================================================
```

## 示例2: 扫描统计

```bash
# 仅扫描并显示分类统计
python file_organizer.py --scan-only
```

输出示例:
```
扫描完成，共发现 118 个文件

分类统计:
  01_Programming/Cpp: 3
  01_Programming/Lua: 3
  01_Programming/Memory: 7
  01_Programming/Network: 4
  01_Programming/Python: 1
  02_GameEngines/Unity: 4
  02_GameEngines/UnrealEngine: 18
  03_Rendering/GlobalIllumination: 3
  03_Rendering/Mobile: 4
  03_Rendering/PBR: 2
  03_Rendering/RayTracing: 3
  03_Rendering/RealTime: 4
  03_Rendering/Shaders: 1
  04_GraphicsPapers/Siggraph: 15
  05_Mathematics/LinearAlgebra: 1
  05_Mathematics/Probability: 1
  未分类: 44
```

## 示例3: 执行整理

```bash
# 执行实际的文件整理
python file_organizer.py --execute
```

交互提示:
```
============================================================
即将执行文件整理
============================================================
目标目录: F:\luobin\Library
删除源文件: 否

确认执行? (yes/no/preview): yes
```

执行后会:
1. 在 `F:\luobin\Library` 创建目录结构
2. 将文件移动到对应分类目录
3. 生成整理报告

## 示例4: 使用批处理脚本

```bash
# Windows 批处理脚本用法
run.bat preview   # 预览模式
run.bat scan      # 扫描统计
run.bat execute   # 执行整理
run.bat clean     # 执行整理并删除源文件（需确认）
```

## 示例5: 自定义配置文件

### 添加新的源目录

编辑 `file_organizer_config.py`:

```python
SOURCE_DIRS = [
    r"F:\luobin\book",
    r"F:\luobin\Books",
    # 添加新的源目录
    r"F:\Downloads\GameDev",
    r"G:\Papers",
]
```

### 添加新的分类规则

```python
CLASSIFICATION_RULES = {
    # 现有规则...

    # 添加新的分类规则
    "03_Rendering/Vulkan": [
        r"(?i)vulkan",
        r"(?i)spir-v",
    ],
    "03_Rendering/DirectX": [
        r"(?i)directx",
        r"(?i)dx12",
        r"(?i)d3d",
    ],
}
```

### 修改版本检测规则

```python
# 调整旧版本阈值（默认第3版以下算旧版本）
# 在 file_organizer.py 中修改第392行:
if file_info.version and file_info.version < 5:  # 改为第5版以下算旧版本
```

## 示例6: 处理待分类文件

运行工具后，查看 `99_Unsorted` 目录:

```bash
# 列出待分类文件
ls -la "F:\luobin\Library\99_Unsorted"
```

根据文件名，手动添加分类规则或手动移动文件到正确目录。

## 示例7: 定期维护

```python
# 创建定期维护脚本 maintain.py
import subprocess
import datetime

# 每周运行一次整理
result = subprocess.run(
    ['python', 'file_organizer.py', '--execute'],
    capture_output=True,
    text=True
)

# 记录日志
with open('maintenance.log', 'a') as f:
    f.write(f"[{datetime.datetime.now()}]\n")
    f.write(result.stdout)
    f.write(result.stderr)
    f.write("\n" + "="*60 + "\n")
```

## 示例8: 检查重复文件

```bash
# 查看重复文件目录
ls -la "F:\luobin\Library\.duplicates"

# 或查看报告文件
cat "F:\luobin\Library\organize_report_*.txt"
```

## 目录结构示例

整理后的目录结构:

```
F:\luobin\Library\
├── 01_Programming\
│   ├── Cpp\
│   │   ├── C++ Concurrency In Action.pdf
│   │   └── Boost程序库完全开发指南.pdf
│   ├── Lua\
│   │   └── Lua程序设计（第4版）.pdf
│   └── Memory\
│       └── Understanding iOS Memory.pdf
├── 02_GameEngines\
│   ├── UnrealEngine\
│   │   ├── UE4_Network_Compendium.pdf
│   │   └── 在UE4实现灯光之美.pdf
│   └── Unity\
│       └── URP渲染管线入门.pdf
├── 03_Rendering\
│   ├── PBR\
│   │   └── course-notes-moving-frostbite-to-pbr.pdf
│   └── RayTracing\
│       └── Ray Tracing in One Weekend.pdf
├── 04_GraphicsPapers\
│   └── Siggraph\
│       └── s2013_pbs_epic_notes_v2.pdf
├── 99_Unsorted\
│   └── (无法自动分类的文件)
└── organize_report_20260506_165814.txt
```

## 常见问题

### Q: 如何避免误分类？
A: 可以通过调整分类规则的精确度，或者在整理后检查每个目录的内容。

### Q: 文件重复检测是如何工作的？
A: 默认使用 `strict` 模式，基于文件内容的 MD5 哈希值检测重复。

### Q: 可以恢复已整理的文件吗？
A: 如果启用了 `CREATE_BACKUP = True`，备份会保存在 `.backup` 目录。

### Q: 如何添加对新文件格式的支持？
A: 在 `SUPPORTED_EXTENSIONS` 中添加新的扩展名。
