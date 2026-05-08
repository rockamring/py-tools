# CLAUDE.md - File Organizer Project

## 项目概述

游戏开发文档自动整理工具，用于扫描、分类、去重和归档游戏开发相关的文档文件。

## 常用命令

```bash
# 预览模式（不实际移动文件）
python file_organizer/file_organizer.py --preview

# 执行整理
python file_organizer/file_organizer.py --execute

# 仅扫描统计
python file_organizer/file_organizer.py --scan-only
```

## 项目结构

```
file_organizer/
├── file_organizer.py         # 主程序入口
└── file_organizer_config.py  # 配置（目录结构、分类规则）
```

## 关键设计

### 目录创建策略
- **按需创建**：目录在实际有文件需要移动时才创建，避免空文件夹
- 基础目录 `.duplicates`（重复文件）始终创建

### 文件处理流程
1. **扫描** → 发现源目录中的支持格式文件
2. **分析** → 计算哈希、检测版本、分类
3. **去重** → 基于内容哈希或文件名去重
4. **整理** → 移动到目标分类目录
5. **报告** → 生成详细统计报告

### 防止死循环机制
- 跳过目标目录下的子目录（防止重复处理已整理的文件）
- 待分类目录优先处理（避免新文件堆积）

## 配置说明

配置文件：`file_organizer_config.py`

- `SOURCE_DIRS` - 源目录列表（待整理的文件夹）
- `TARGET_BASE_DIR` - 目标整理目录
- `DIRECTORY_STRUCTURE` - 分类目录结构
- `CLASSIFICATION_RULES` - 文件名匹配规则（正则）
- `DUPLICATE_MODE` - 去重模式（strict/filename/none）

## 支持的文件格式

PDF, EPUB, MOBI, AZW3, DJVU, CHM, DOC, DOCX, PPT, PPTX, TXT, MD
