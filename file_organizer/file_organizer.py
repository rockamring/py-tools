#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏开发文档整理工具
Game Development Document Organizer

功能:
1. 自动扫描并分类游戏开发相关文档
2. 智能识别文件类型和主题
3. 支持去重（基于文件内容哈希）
4. 支持版本检测和归档
5. 提供删除源文件选项
6. 待分类目录存放不确定文件
7. 归档目录存放旧版本书籍

作者: Claude
日期: 2026-05-06
"""

import os
import sys
import re
import shutil
import hashlib
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, asdict
from collections import defaultdict
import file_organizer_config as config


# =============================================================================
# 数据结构
# =============================================================================

@dataclass
class FileInfo:
    """文件信息数据类"""
    path: Path
    name: str
    extension: str
    size: int
    modified_time: float
    content_hash: Optional[str] = None
    category: Optional[str] = None
    version: Optional[int] = None

    def to_dict(self) -> dict:
        return {
            'path': str(self.path),
            'name': self.name,
            'extension': self.extension,
            'size': self.size,
            'modified_time': self.modified_time,
            'content_hash': self.content_hash,
            'category': self.category,
            'version': self.version,
        }


@dataclass
class OrganizeResult:
    """整理结果数据类"""
    total_files: int = 0
    organized_files: int = 0
    duplicate_files: int = 0
    archived_files: int = 0
    unsorted_files: int = 0
    errors: List[str] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []


# =============================================================================
# 日志配置
# =============================================================================

def setup_logging(log_level: str = 'INFO', log_file: Optional[str] = None) -> logging.Logger:
    """配置日志系统"""
    logger = logging.getLogger('FileOrganizer')
    logger.setLevel(getattr(logging, log_level.upper()))

    if logger.handlers:
        logger.handlers.clear()

    # 控制台输出
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # 文件输出
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


# =============================================================================
# 文件扫描器
# =============================================================================

class FileScanner:
    """文件扫描器 - 扫描源目录中的所有文件"""

    def __init__(self, source_dirs: List[str], logger: logging.Logger):
        self.source_dirs = [Path(d) for d in source_dirs]
        self.logger = logger
        self.supported_exts = set(config.SUPPORTED_EXTENSIONS.keys())

    def scan(self) -> List[FileInfo]:
        """扫描所有源目录，返回文件信息列表"""
        files = []
        self.logger.info(f"开始扫描 {len(self.source_dirs)} 个源目录...")

        for source_dir in self.source_dirs:
            if not source_dir.exists():
                self.logger.warning(f"源目录不存在: {source_dir}")
                continue

            self.logger.info(f"扫描目录: {source_dir}")
            count = 0

            for file_path in source_dir.rglob('*'):
                if file_path.is_file():
                    ext = file_path.suffix.lower()
                    if ext in self.supported_exts:
                        try:
                            stat = file_path.stat()
                            file_info = FileInfo(
                                path=file_path,
                                name=file_path.name,
                                extension=ext,
                                size=stat.st_size,
                                modified_time=stat.st_mtime,
                            )
                            files.append(file_info)
                            count += 1
                        except Exception as e:
                            self.logger.error(f"无法读取文件 {file_path}: {e}")

            self.logger.info(f"  找到 {count} 个支持的文件")

        self.logger.info(f"扫描完成，共发现 {len(files)} 个文件")
        return files


# =============================================================================
# 文件分析器
# =============================================================================

class FileAnalyzer:
    """文件分析器 - 分析文件内容、分类和版本"""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.classification_rules = config.CLASSIFICATION_RULES
        self.version_patterns = [re.compile(p) for p in config.VERSION_PATTERNS]

    def calculate_hash(self, file_path: Path, chunk_size: int = 8192) -> str:
        """计算文件内容的 MD5 哈希值"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(chunk_size), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            self.logger.error(f"计算哈希失败 {file_path}: {e}")
            return ""

    def detect_version(self, filename: str) -> Optional[int]:
        """从文件名中检测版本号"""
        for pattern in self.version_patterns:
            match = pattern.search(filename)
            if match:
                try:
                    return int(match.group(1))
                except (ValueError, IndexError):
                    continue
        return None

    def classify_file(self, file_info: FileInfo) -> Optional[str]:
        """根据文件名和规则分类文件"""
        filename = file_info.name

        for category, patterns in self.classification_rules.items():
            for pattern in patterns:
                try:
                    if re.search(pattern, filename):
                        return category
                except re.error as e:
                    self.logger.warning(f"正则表达式错误 '{pattern}': {e}")
                    continue

        return None

    def analyze(self, files: List[FileInfo]) -> List[FileInfo]:
        """分析所有文件"""
        self.logger.info("开始分析文件...")

        for i, file_info in enumerate(files):
            # 计算内容哈希
            if config.DUPLICATE_MODE == 'strict':
                file_info.content_hash = self.calculate_hash(file_info.path)

            # 检测版本
            file_info.version = self.detect_version(file_info.name)

            # 分类
            file_info.category = self.classify_file(file_info)

            if (i + 1) % 100 == 0:
                self.logger.info(f"  已分析 {i + 1}/{len(files)} 个文件")

        self.logger.info(f"分析完成")
        return files


# =============================================================================
# 重复文件检测器
# =============================================================================

class DuplicateDetector:
    """重复文件检测器"""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.seen_hashes: Dict[str, FileInfo] = {}
        self.seen_names: Dict[str, FileInfo] = {}
        self.duplicates: List[Tuple[FileInfo, FileInfo]] = []

    def find_duplicates(self, files: List[FileInfo]) -> Tuple[List[FileInfo], List[Tuple[FileInfo, FileInfo]]]:
        """
        查找重复文件
        返回: (唯一文件列表, 重复文件对列表)
        """
        self.logger.info("开始检测重复文件...")

        unique_files = []
        mode = config.DUPLICATE_MODE

        for file_info in files:
            is_duplicate = False
            original = None

            if mode == 'strict' and file_info.content_hash:
                if file_info.content_hash in self.seen_hashes:
                    is_duplicate = True
                    original = self.seen_hashes[file_info.content_hash]
                else:
                    self.seen_hashes[file_info.content_hash] = file_info

            elif mode == 'filename':
                key = f"{file_info.name}_{file_info.size}"
                if key in self.seen_names:
                    is_duplicate = True
                    original = self.seen_names[key]
                else:
                    self.seen_names[key] = file_info

            if is_duplicate and original:
                self.duplicates.append((original, file_info))
                self.logger.debug(f"发现重复: {file_info.name}")
            else:
                unique_files.append(file_info)

        self.logger.info(f"检测到 {len(self.duplicates)} 个重复文件")
        return unique_files, self.duplicates


# =============================================================================
# 目录管理器
# =============================================================================

class DirectoryManager:
    """目录管理器 - 创建和管理目标目录结构"""

    def __init__(self, base_dir: Path, logger: logging.Logger):
        self.base_dir = base_dir
        self.logger = logger
        self.created_dirs: Set[Path] = set()

    def setup(self) -> None:
        """初始化目录结构"""
        self.logger.info(f"初始化目录结构: {self.base_dir}")

        # 创建主目录
        self.base_dir.mkdir(parents=True, exist_ok=True)

        # 创建子目录
        for main_dir, info in config.DIRECTORY_STRUCTURE.items():
            main_path = self.base_dir / main_dir
            main_path.mkdir(exist_ok=True)

            for sub_dir in info.get('subdirs', {}).keys():
                sub_path = main_path / sub_dir
                sub_path.mkdir(exist_ok=True)
                self.created_dirs.add(sub_path)

        # 创建重复文件目录
        dup_dir = self.base_dir / ".duplicates"
        dup_dir.mkdir(exist_ok=True)

        self.logger.info(f"目录结构创建完成")

    def get_target_path(self, category: Optional[str], filename: str) -> Path:
        """获取文件的目标路径"""
        if category:
            target_dir = self.base_dir / category
            if target_dir.exists():
                return target_dir / filename

        # 默认放入待分类目录
        return self.base_dir / config.UNSORTED_DIR / filename


# =============================================================================
# 文件整理器
# =============================================================================

class FileOrganizer:
    """文件整理器 - 执行文件移动和组织操作"""

    def __init__(self, target_dir: Path, logger: logging.Logger):
        self.target_dir = target_dir
        self.logger = logger
        self.dir_manager = DirectoryManager(target_dir, logger)
        self.result = OrganizeResult()

        # 记录已处理的文件（用于检测目标目录中的重复）
        self.target_files: Dict[str, Path] = {}

    def check_target_duplicate(self, file_info: FileInfo) -> Optional[Path]:
        """检查目标目录中是否已存在相同文件"""
        if file_info.content_hash and file_info.content_hash in self.target_files:
            return self.target_files[file_info.content_hash]
        return None

    def move_file(self, source: Path, target: Path, dry_run: bool = False) -> bool:
        """移动文件，处理重名情况"""
        try:
            if dry_run:
                self.logger.info(f"[模拟] 移动: {source} -> {target}")
                return True

            # 确保目标目录存在
            target.parent.mkdir(parents=True, exist_ok=True)

            # 处理重名
            final_target = target
            counter = 1
            while final_target.exists():
                stem = target.stem
                suffix = target.suffix
                final_target = target.parent / f"{stem}_{counter:03d}{suffix}"
                counter += 1

            shutil.move(str(source), str(final_target))
            self.logger.debug(f"移动成功: {source} -> {final_target}")
            return True

        except Exception as e:
            self.logger.error(f"移动失败 {source}: {e}")
            return False

    def organize(self, files: List[FileInfo], dry_run: bool = False,
                 delete_source: bool = False) -> OrganizeResult:
        """执行文件整理"""
        self.logger.info(f"{'[模拟模式] ' if dry_run else ''}开始整理文件...")

        # 初始化目录结构
        if not dry_run:
            self.dir_manager.setup()

        self.result.total_files = len(files)

        for file_info in files:
            # 检查是否是旧版本需要归档
            target_category = file_info.category
            if file_info.version and file_info.version < 3:  # 假设第3版以下算旧版本
                target_category = f"{config.ARCHIVE_DIR}/OldVersions"
                self.result.archived_files += 1

            # 如果没有分类，放入待分类
            if not target_category:
                target_category = config.UNSORTED_DIR
                self.result.unsorted_files += 1

            # 获取目标路径
            target_path = self.dir_manager.get_target_path(
                target_category,
                file_info.name
            )

            # 检查目标目录是否已有相同文件
            existing = self.check_target_duplicate(file_info)
            if existing:
                self.logger.debug(f"目标目录已存在相同文件: {file_info.name}")
                self.result.duplicate_files += 1
                continue

            # 执行移动
            if self.move_file(file_info.path, target_path, dry_run):
                self.result.organized_files += 1
                if file_info.content_hash:
                    self.target_files[file_info.content_hash] = target_path

                # 删除源文件（如果启用且不是模拟模式）
                if delete_source and not dry_run and file_info.path.exists():
                    try:
                        if file_info.path.is_file():
                            file_info.path.unlink()
                        elif file_info.path.is_dir():
                            shutil.rmtree(file_info.path)
                    except Exception as e:
                        self.logger.error(f"删除源文件失败 {file_info.path}: {e}")

        return self.result


# =============================================================================
# 报告生成器
# =============================================================================

class ReportGenerator:
    """报告生成器 - 生成整理报告"""

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def generate(self, result: OrganizeResult, output_path: Optional[Path] = None) -> str:
        """生成整理报告"""
        report_lines = [
            "=" * 60,
            "文件整理报告",
            "=" * 60,
            f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "统计信息:",
            f"  总文件数: {result.total_files}",
            f"  已整理: {result.organized_files}",
            f"  重复文件: {result.duplicate_files}",
            f"  归档文件: {result.archived_files}",
            f"  待分类: {result.unsorted_files}",
            "",
        ]

        if result.errors:
            report_lines.extend([
                "错误列表:",
                *[f"  - {e}" for e in result.errors],
                "",
            ])

        report_lines.append("=" * 60)

        report = "\n".join(report_lines)

        if output_path:
            output_path.write_text(report, encoding='utf-8')
            self.logger.info(f"报告已保存: {output_path}")

        return report


# =============================================================================
# 主程序
# =============================================================================

class OrganizerApp:
    """整理工具主程序"""

    def __init__(self):
        self.logger = setup_logging(config.LOG_LEVEL)
        self.scanner = FileScanner(config.SOURCE_DIRS, self.logger)
        self.analyzer = FileAnalyzer(self.logger)
        self.duplicate_detector = DuplicateDetector(self.logger)
        self.organizer = FileOrganizer(Path(config.TARGET_BASE_DIR), self.logger)
        self.report_generator = ReportGenerator(self.logger)

    def run(self, dry_run: bool = True, delete_source: bool = False) -> OrganizeResult:
        """运行整理流程"""
        self.logger.info("=" * 60)
        self.logger.info("游戏开发文档整理工具")
        self.logger.info("=" * 60)

        # 1. 扫描文件
        files = self.scanner.scan()

        if not files:
            self.logger.info("没有找到需要整理的文件")
            return OrganizeResult()

        # 2. 分析文件
        files = self.analyzer.analyze(files)

        # 3. 检测重复
        unique_files, duplicates = self.duplicate_detector.find_duplicates(files)

        if duplicates:
            self.logger.info(f"发现 {len(duplicates)} 个重复文件将跳过")

        # 4. 整理文件
        result = self.organizer.organize(unique_files, dry_run, delete_source)

        # 5. 生成报告
        report_path = Path(config.TARGET_BASE_DIR) / f"organize_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        report = self.report_generator.generate(result, report_path)

        self.logger.info("\n" + report)

        return result

    def preview(self) -> None:
        """预览整理结果（不执行实际移动）"""
        self.logger.info("运行预览模式...")
        self.run(dry_run=True)

    def organize_with_confirm(self, delete_source: bool = False) -> OrganizeResult:
        """带确认的执行模式"""
        if config.INTERACTIVE:
            print("\n" + "=" * 60)
            print("即将执行文件整理")
            print("=" * 60)
            print(f"目标目录: {config.TARGET_BASE_DIR}")
            print(f"删除源文件: {'是' if delete_source else '否'}")
            print("")

            response = input("确认执行? (yes/no/preview): ").lower().strip()

            if response == 'preview':
                self.preview()
                return self.organize_with_confirm(delete_source)
            elif response not in ('yes', 'y'):
                self.logger.info("操作已取消")
                return OrganizeResult()

        return self.run(dry_run=False, delete_source=delete_source)


def main():
    """主入口函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description='游戏开发文档整理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 预览模式（不实际移动文件）
  python file_organizer.py --preview

  # 执行整理
  python file_organizer.py --execute

  # 执行整理并删除源文件
  python file_organizer.py --execute --delete-source

  # 仅扫描并显示统计
  python file_organizer.py --scan-only
        """
    )

    parser.add_argument('--preview', action='store_true',
                        help='预览模式，不实际移动文件')
    parser.add_argument('--execute', action='store_true',
                        help='执行实际整理操作')
    parser.add_argument('--delete-source', action='store_true',
                        help='整理后删除源文件（谨慎使用）')
    parser.add_argument('--scan-only', action='store_true',
                        help='仅扫描并显示统计信息')

    args = parser.parse_args()

    app = OrganizerApp()

    if args.scan_only:
        files = app.scanner.scan()
        print(f"\n扫描完成，共发现 {len(files)} 个文件")
        # 显示分类统计
        categories = defaultdict(int)
        for f in app.analyzer.analyze(files):
            cat = f.category or '未分类'
            categories[cat] += 1
        print("\n分类统计:")
        for cat, count in sorted(categories.items()):
            print(f"  {cat}: {count}")

    elif args.preview:
        app.preview()

    elif args.execute:
        result = app.organize_with_confirm(delete_source=args.delete_source)
        sys.exit(0 if not result.errors else 1)

    else:
        parser.print_help()
        print("\n提示: 首次运行建议使用 --preview 查看效果")


if __name__ == '__main__':
    main()
