# 游戏开发文档整理工具

一个智能化的文件整理工具，专门用于整理游戏开发相关的电子书籍、论文和技术文档。

## 功能特性

### 核心功能
- **智能分类** - 根据文件名自动识别主题并分类
- **目录结构** - 符合游戏技术行业标准的目录命名
- **去重处理** - 支持基于内容哈希的严格去重
- **版本检测** - 自动识别旧版本书籍并归档
- **待分类目录** - 存放无法确定分类的文件
- **归档目录** - 存放低版本或过时资料
- **删除源文件** - 可选整理后删除源文件

### 支持的文件格式
- PDF 文档
- EPUB/MOBI/AZW3 电子书
- DJVU 文档
- CHM 帮助文件
- Word/PowerPoint 文档
- 文本和 Markdown 文件

## 目录结构

```
Library/
├── 01_编程/                 # 编程与算法
│   ├── Cpp/                 # C++
│   ├── CSharp/              # C#
│   ├── Lua/                 # Lua
│   ├── Python/              # Python
│   ├── 并发/                # 并发与多线程
│   ├── 设计模式/            # Design Patterns
│   ├── 算法/                # 算法与数据结构
│   ├── 网络/                # 网络编程
│   └── 内存/                # 内存管理
├── 02_游戏引擎/             # 游戏引擎
│   ├── Unreal/              # 虚幻引擎 Unreal Engine
│   ├── Unity/               # Unity
│   └── General/            # 通用技术
├── 03_渲染/                 # 图形渲染
│   ├── 实时渲染/            # Real-Time Rendering
│   ├── 光线追踪/            # Ray Tracing
│   ├── PBR/                 # PBR
│   ├── 着色器/              # Shaders
│   ├── 全局光照/            # Global Illumination
│   ├── 后处理/              # Post Processing
│   └── 移动端/              # Mobile Rendering
├── 04_图形学论文/           # 图形学论文
│   ├── Siggraph/            # SIGGRAPH
│   ├── GDC/                 # GDC
│   ├── 图形学/              # Computer Graphics
│   └── 课程讲义/            # Courses & Tutorials
├── 05_数学/                 # 数学基础
│   ├── 线性代数/            # Linear Algebra
│   ├── 微积分/              # Calculus
│   ├── 离散数学/            # Discrete Math
│   ├── 概率统计/            # Probability & Statistics
│   └── 几何/                # Geometry
├── 06_人工智能/             # 人工智能与机器学习
│   ├── 深度学习/            # Deep Learning
│   ├── 游戏AI/              # Game AI
│   └── NLP/                 # NLP
├── 07_工具/                 # 工具与中间件
│   ├── 版本控制/            # Version Control
│   ├── 性能分析/            # Profiling
│   └── DCC/                 # DCC
├── 98_归档/                 # 归档资料
│   ├── 旧版本/              # Old Versions
│   └── 已过时/              # Deprecated
├── 99_待分类/               # 待分类
└── .duplicates/             # 重复文件
```

## 使用方法

### 1. 预览模式（推荐首次使用）
```bash
python file_organizer.py --preview
```
只显示将要执行的操作，不实际移动文件。

### 2. 仅扫描统计
```bash
python file_organizer.py --scan-only
```
扫描并显示文件分类统计，帮助了解将要整理的内容。

### 3. 执行整理
```bash
python file_organizer.py --execute
```
执行实际的文件整理操作。

### 4. 执行整理并删除源文件
```bash
python file_organizer.py --execute --delete-source
```
**⚠️ 警告**: 此操作会删除源文件，请确保已备份重要数据。

## 配置文件说明

编辑 `file_organizer_config.py` 来自定义配置：

### 源目录配置
```python
SOURCE_DIRS = [
    r"F:\luobin\book",
    r"F:\luobin\Books",
    # 添加更多源目录...
]
```

### 目标目录配置
```python
TARGET_BASE_DIR = r"F:\luobin\Library"
```

### 分类规则配置
可以添加自定义的分类规则，基于正则表达式匹配文件名：

```python
CLASSIFICATION_RULES = {
    "01_Programming/Cpp": [
        r"(?i)c\+\+",      # 匹配 c++
        r"(?i)cpp",        # 匹配 cpp
        r"(?i)boost",      # 匹配 boost
    ],
    # 添加更多规则...
}
```

### 去重模式配置
```python
# 去重模式: 'strict' (基于内容哈希), 'filename' (基于文件名), 'none' (不去重)
DUPLICATE_MODE = 'strict'

# 重复文件处理方式: 'skip' (跳过), 'move' (移到重复文件夹), 'delete' (删除)
DUPLICATE_ACTION = 'move'
```

### 版本检测配置
```python
# 版本号匹配模式
VERSION_PATTERNS = [
    r'第\s*(\d+)\s*版',  # 匹配: 第X版
    r'\b(\d+)\s*ed',      # 匹配: X ed
    r'\bv(\d+)',          # 匹配: vX
]
```

## 工作流程

1. **扫描** - 遍历所有源目录，收集支持的文件
2. **分析** - 计算文件哈希、检测版本、分类
3. **去重** - 根据配置模式检测并处理重复文件
4. **整理** - 移动文件到目标目录结构
5. **报告** - 生成整理报告

## 注意事项

1. **首次使用** - 强烈建议先使用 `--preview` 模式查看效果
2. **备份数据** - 执行整理前建议备份重要文件
3. **删除源文件** - 使用 `--delete-source` 前请确认文件已正确整理
4. **待分类文件** - 无法自动分类的文件会放入 `99_Unsorted` 目录，需要手动整理
5. **重复文件** - 重复文件会被跳过或移到 `.duplicates` 目录

## 扩展开发

### 添加新的分类规则

在 `file_organizer_config.py` 中添加规则：

```python
CLASSIFICATION_RULES = {
    # 现有规则...
    "NewCategory/SubCategory": [
        r"(?i)keyword1",
        r"(?i)keyword2",
    ],
}
```

### 添加新的文件格式支持

在 `file_organizer_config.py` 中添加扩展名：

```python
SUPPORTED_EXTENSIONS = {
    # 现有格式...
    '.newext': 'Description',
}
```

## 更新日志

### v1.0.0 (2026-05-06)
- 初始版本发布
- 支持智能分类和去重
- 支持版本检测和归档
- 提供预览和执行两种模式
