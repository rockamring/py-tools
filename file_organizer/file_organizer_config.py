"""
文件整理工具 - 配置文件
Game Development Document Organizer Configuration
"""

import os

# =============================================================================
# 路径配置
# =============================================================================

# 源目录（需要整理的文件夹）
SOURCE_DIRS = [
    r"F:\luobin\book",
    r"F:\luobin\Books",
    r"F:\luobin\doc",
    r"F:\luobin\Papers",
    r"F:\luobin\Papers_Graphics",
    r"F:\luobin\Papers_Siggraph",
    r"F:\luobin\Papers_UE4",
    r"F:\luobin\Talking",
]

# 目标整理目录（新建的子目录）
TARGET_BASE_DIR = r"F:\luobin\Library"

# =============================================================================
# 目录结构配置 - 符合游戏技术行业标准
# =============================================================================

# 主分类目录结构
DIRECTORY_STRUCTURE = {
    "01_Programming": {
        "description": "编程与算法",
        "subdirs": {
            "Cpp": "C++ 语言与标准库",
            "CSharp": "C# 语言与.NET",
            "Lua": "Lua 脚本语言",
            "Python": "Python 语言",
            "Concurrency": "并发与多线程编程",
            "DesignPatterns": "设计模式",
            "Algorithms": "算法与数据结构",
            "Network": "网络编程",
            "Memory": "内存管理",
        }
    },
    "02_GameEngines": {
        "description": "游戏引擎",
        "subdirs": {
            "UnrealEngine": "虚幻引擎",
            "Unity": "Unity引擎",
            "Custom": "自研引擎",
        }
    },
    "03_Rendering": {
        "description": "图形渲染",
        "subdirs": {
            "RealTime": "实时渲染",
            "RayTracing": "光线追踪",
            "PBR": "基于物理的渲染",
            "Shaders": "着色器技术",
            "GlobalIllumination": "全局光照",
            "PostProcessing": "后处理技术",
            "Mobile": "移动端渲染",
        }
    },
    "04_GraphicsPapers": {
        "description": "图形学论文",
        "subdirs": {
            "Siggraph": "SIGGRAPH 论文集",
            "GDC": "GDC 技术分享",
            "PG": "图形学前沿论文",
            "Courses": "课程讲义与笔记",
        }
    },
    "05_Mathematics": {
        "description": "数学基础",
        "subdirs": {
            "LinearAlgebra": "线性代数",
            "Calculus": "微积分",
            "DiscreteMath": "离散数学",
            "Probability": "概率与统计",
            "Geometry": "计算几何",
        }
    },
    "06_AI_ML": {
        "description": "人工智能与机器学习",
        "subdirs": {
            "DeepLearning": "深度学习",
            "GameAI": "游戏AI",
            "NLP": "自然语言处理",
        }
    },
    "07_Tools": {
        "description": "工具与中间件",
        "subdirs": {
            "VersionControl": "版本控制",
            "Profiling": "性能分析",
            "DCC": "数字内容创作工具",
        }
    },
    "08_Archive": {
        "description": "归档资料",
        "subdirs": {
            "OldVersions": "旧版本书籍",
            "Deprecated": "已过时技术",
        }
    },
    "99_Unsorted": {
        "description": "待分类",
        "subdirs": {}
    },
}

# =============================================================================
# 文件分类规则 - 基于文件名关键词匹配
# =============================================================================

CLASSIFICATION_RULES = {
    # 编程语言
    "01_Programming/Cpp": [
        r"(?i)c\+\+", r"(?i)cpp", r"(?i)boost", r"(?i)stl",
        r"(?i)现代c\+\+", r"(?i)c\+\+11", r"(?i)c\+\+14", r"(?i)c\+\+17",
    ],
    "01_Programming/Lua": [
        r"(?i)lua", r"(?i)luajit",
    ],
    "01_Programming/Python": [
        r"(?i)python",
    ],
    "01_Programming/Concurrency": [
        r"(?i)concurrency", r"(?i)concurrent", r"(?i)多线程", r"(?i)并发",
        r"(?i)thread", r"(?i)atomic",
    ],
    "01_Programming/Memory": [
        r"(?i)memory", r"(?i)内存", r"(?i)gc", r"(?i)garbage",
    ],
    "01_Programming/Network": [
        r"(?i)netty", r"(?i)network", r"(?i)网络",
    ],
    "01_Programming/Algorithms": [
        r"(?i)algorithm", r"(?i)数据结构",
    ],

    # 游戏引擎
    "02_GameEngines/UnrealEngine": [
        r"(?i)unreal", r"(?i)ue4", r"(?i)ue5", r"(?i)虚幻",
        r"(?i)frostbite",  # 寒霜引擎相关
    ],
    "02_GameEngines/Unity": [
        r"(?i)unity", r"(?i)urp",
    ],

    # 图形渲染
    "03_Rendering/RealTime": [
        r"(?i)real.?time", r"(?i)实时渲染", r"(?i)modern.?rendering",
        r"(?i)metal",
    ],
    "03_Rendering/RayTracing": [
        r"(?i)ray.?trac", r"(?i)光线追踪",
    ],
    "03_Rendering/PBR": [
        r"(?i)pbr", r"(?i)physically.?based", r"(?i)物理.?渲染",
    ],
    "03_Rendering/GlobalIllumination": [
        r"(?i)global.?illumination", r"(?i)gi\b", r"(?i)全局光照",
    ],
    "03_Rendering/Shaders": [
        r"(?i)shader", r"(?i)shading", r"(?i)着色器",
    ],
    "03_Rendering/Mobile": [
        r"(?i)mobile", r"(?i)ios", r"(?i)android", r"(?i)移动端",
    ],

    # 数学
    "05_Mathematics/LinearAlgebra": [
        r"(?i)linear.?algebra", r"(?i)线性代数",
    ],
    "05_Mathematics/Calculus": [
        r"(?i)calculus", r"(?i)微积分",
    ],
    "05_Mathematics/Probability": [
        r"(?i)probability", r"(?i)statistic", r"(?i)概率", r"(?i)统计",
    ],

    # AI
    "06_AI_ML/DeepLearning": [
        r"(?i)deep.?learn", r"(?i)深度学习", r"(?i)神经网络",
    ],

    # 论文分类
    "04_GraphicsPapers/Siggraph": [
        r"(?i)siggraph", r"(?i)s20\d{2}", r"(?i)s201\d",
    ],
    "04_GraphicsPapers/GDC": [
        r"(?i)gdc", r"(?i)devcon", r"(?i)fest",
    ],
}

# =============================================================================
# 文件类型配置
# =============================================================================

# 支持的文档格式
SUPPORTED_EXTENSIONS = {
    '.pdf': 'PDF Document',
    '.epub': 'EPUB eBook',
    '.mobi': 'MOBI eBook',
    '.azw3': 'Kindle eBook',
    '.djvu': 'DjVu Document',
    '.chm': 'Compiled HTML Help',
    '.doc': 'Word Document',
    '.docx': 'Word Document',
    '.ppt': 'PowerPoint',
    '.pptx': 'PowerPoint',
    '.txt': 'Text File',
    '.md': 'Markdown',
}

# 压缩包格式（可选解压处理）
ARCHIVE_EXTENSIONS = {
    '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2',
}

# =============================================================================
# 去重配置
# =============================================================================

# 去重模式: 'strict' (严格，基于内容哈希), 'filename' (基于文件名), 'none' (不去重)
DUPLICATE_MODE = 'strict'

# 重复文件处理方式: 'skip' (跳过), 'move' (移到重复文件夹), 'delete' (删除)
DUPLICATE_ACTION = 'move'

# =============================================================================
# 版本检测配置
# =============================================================================

# 版本号匹配模式（用于检测旧版本书籍）
VERSION_PATTERNS = [
    r'第\s*(\d+)\s*版',  # 中文版式：第X版
    r'第\s*(\d+)\s*版',  # 中文版式：第X版
    r'\b(\d+)\s*ed',      # 英文版式：X ed
    r'\bedition\s*(\d+)', # 英文版式：edition X
    r'\bv(\d+)',          # vX 版本号
    r'\bversion\s*(\d+)', # version X
]

# =============================================================================
# 操作配置
# =============================================================================

# 是否删除源文件（谨慎使用）
DELETE_SOURCE = False

# 是否创建备份
CREATE_BACKUP = True
BACKUP_DIR = r"F:\luobin\Library\.backup"

# 日志级别: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL = 'INFO'

# 是否启用交互模式（询问确认）
INTERACTIVE = True

# 待分类目录
UNSORTED_DIR = "99_Unsorted"

# 归档目录
ARCHIVE_DIR = "08_Archive"
