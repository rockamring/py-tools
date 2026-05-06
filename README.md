# py-tools

个人Python工具集，包含各类实用工具脚本。

## 工具列表

### file_organizer - 游戏开发文档整理工具

智能整理游戏开发相关的电子书籍、论文和技术文档。

**功能特性：**
- 自动扫描并分类文档
- 智能识别文件类型和主题
- 支持去重（基于内容哈希）
- 支持版本检测和归档
- 提供删除源文件选项
- 待分类目录存放不确定文件
- 归档目录存放旧版本书籍

**使用方法：**
```bash
cd file_organizer
python file_organizer.py --preview  # 预览模式
python file_organizer.py --execute  # 执行整理
```

详见 [file_organizer/README.md](file_organizer/README.md)

## 项目结构

```
py-tools/
├── file_organizer/          # 文件整理工具
│   ├── file_organizer.py    # 主程序
│   ├── file_organizer_config.py  # 配置文件
│   ├── run.bat              # Windows批处理脚本
│   ├── README.md            # 使用说明
│   └── EXAMPLES.md          # 使用示例
├── .gitignore               # Git忽略文件
└── README.md                # 本文件
```

## 环境要求

- Python 3.8+
- Windows/Linux/macOS

## 使用建议

1. 每个工具放在独立的子目录中
2. 包含README.md说明文档
3. 配置文件与主程序分离，便于自定义

## 许可证

个人使用
