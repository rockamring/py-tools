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
TARGET_BASE_DIR = r"G:\myproj\game_dev_docs"

def get_source_dirs():
    """
    获取完整的源目录列表
    - 待分类目录作为第一个源目录（优先处理）
    - 排除目标目录下的所有子目录（防止死循环）
    """
    dirs = []

    # 1. 首先添加待分类目录（始终优先处理）
    unsorted_full_path = os.path.join(TARGET_BASE_DIR, UNSORTED_DIR)
    dirs.append(unsorted_full_path)

    # 2. 添加其他源目录，但排除目标目录下的子目录
    target_norm = os.path.normpath(TARGET_BASE_DIR).lower()
    for d in SOURCE_DIRS:
        d_norm = os.path.normpath(d).lower()
        # 跳过目标目录及其子目录（防止死循环）
        if not d_norm.startswith(target_norm):
            dirs.append(d)

    return dirs

# =============================================================================
# 目录结构配置 - 符合游戏技术行业标准
# =============================================================================

# 主分类目录结构
DIRECTORY_STRUCTURE = {
    "01_编程": {
        "description": "编程与算法",
        "subdirs": {
            "Cpp": "C++",
            "CSharp": "C#",
            "Lua": "Lua",
            "Python": "Python",
            "并发": "Concurrency",
            "设计模式": "Design Patterns",
            "算法": "Algorithms",
            "网络": "Network",
            "内存": "Memory",
        }
    },
    "02_游戏引擎": {
        "description": "游戏引擎",
        "subdirs": {
            "Unreal": "虚幻引擎 Unreal Engine",
            "Unity": "Unity",
            "自研引擎": "Custom Engine",
        }
    },
    "03_渲染": {
        "description": "图形渲染",
        "subdirs": {
            "实时渲染": "Real-Time Rendering",
            "光线追踪": "Ray Tracing",
            "PBR": "PBR",
            "着色器": "Shaders",
            "全局光照": "Global Illumination",
            "后处理": "Post Processing",
            "移动端": "Mobile",
        }
    },
    "04_图形学论文": {
        "description": "图形学论文",
        "subdirs": {
            "Siggraph": "SIGGRAPH",
            "GDC": "GDC",
            "图形学": "Computer Graphics",
            "课程讲义": "Courses & Tutorials",
        }
    },
    "05_数学": {
        "description": "数学基础",
        "subdirs": {
            "线性代数": "Linear Algebra",
            "微积分": "Calculus",
            "离散数学": "Discrete Math",
            "概率统计": "Probability & Statistics",
            "几何": "Geometry",
        }
    },
    "06_人工智能": {
        "description": "人工智能与机器学习",
        "subdirs": {
            "深度学习": "Deep Learning",
            "游戏AI": "Game AI",
            "NLP": "NLP",
        }
    },
    "07_工具": {
        "description": "工具与中间件",
        "subdirs": {
            "版本控制": "Version Control",
            "性能分析": "Profiling",
            "DCC": "DCC",
        }
    },
    "98_归档": {
        "description": "归档资料",
        "subdirs": {
            "旧版本": "Old Versions",
            "已过时": "Deprecated",
        }
    },
    "99_待分类": {
        "description": "待分类",
        "subdirs": {}
    },
}

# =============================================================================
# 文件分类规则 - 基于文件名关键词匹配
# =============================================================================

CLASSIFICATION_RULES = {
    # 编程语言
    "01_编程/Cpp": [
        r"(?i)c\+\+", r"(?i)cpp", r"(?i)boost", r"(?i)stl",
        r"(?i)现代c\+\+", r"(?i)c\+\+11", r"(?i)c\+\+14", r"(?i)c\+\+17",
    ],
    "01_编程/Lua": [
        r"(?i)lua", r"(?i)luajit",
    ],
    "01_编程/Python": [
        r"(?i)python",
    ],
    "01_编程/并发": [
        r"(?i)concurrency", r"(?i)concurrent", r"(?i)多线程", r"(?i)并发",
        r"(?i)thread", r"(?i)atomic",
    ],
    "01_编程/内存": [
        r"(?i)memory", r"(?i)内存", r"(?i)gc", r"(?i)garbage",
    ],
    "01_编程/网络": [
        r"(?i)netty", r"(?i)network", r"(?i)网络",
    ],
    "01_编程/算法": [
        r"(?i)algorithm", r"(?i)数据结构",
    ],

    # 游戏引擎
    "02_游戏引擎/Unreal": [
        r"(?i)unreal", r"(?i)ue4", r"(?i)ue5", r"(?i)虚幻",
        r"(?i)frostbite",  # 寒霜引擎相关
    ],
    "02_游戏引擎/Unity": [
        r"(?i)unity", r"(?i)urp",
    ],

    # 图形渲染
    "03_渲染/实时渲染": [
        r"(?i)real.?time", r"(?i)实时渲染", r"(?i)modern.?rendering",
        r"(?i)metal",
    ],
    "03_渲染/光线追踪": [
        r"(?i)ray.?trac", r"(?i)光线追踪",
    ],
    "03_渲染/PBR": [
        r"(?i)pbr", r"(?i)physically.?based", r"(?i)物理.?渲染",
    ],
    "03_渲染/全局光照": [
        r"(?i)global.?illumination", r"(?i)gi\b", r"(?i)全局光照",
    ],
    "03_渲染/着色器": [
        r"(?i)shader", r"(?i)shading", r"(?i)着色器",
    ],
    "03_渲染/移动端": [
        r"(?i)mobile", r"(?i)ios", r"(?i)android", r"(?i)移动端",
    ],

    # 数学
    "05_数学/线性代数": [
        r"(?i)linear.?algebra", r"(?i)线性代数",
    ],
    "05_数学/微积分": [
        r"(?i)calculus", r"(?i)微积分",
    ],
    "05_数学/概率统计": [
        r"(?i)probability", r"(?i)statistic", r"(?i)概率", r"(?i)统计",
    ],

    # AI
    "06_人工智能/深度学习": [
        r"(?i)deep.?learn", r"(?i)深度学习", r"(?i)神经网络",
    ],

    # 论文分类
    "04_图形学论文/Siggraph": [
        r"(?i)siggraph", r"(?i)s20\d{2}", r"(?i)s201\d",
    ],
    "04_图形学论文/GDC": [
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
UNSORTED_DIR = "99_待分类"

# 归档目录
ARCHIVE_DIR = "98_归档"
