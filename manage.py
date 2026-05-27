#!/usr/bin/env python
"""Django 的命令行管理工具，用于启动开发服务器、执行数据库迁移等操作"""
import os
import sys


def main():
    """运行 Django 管理任务的主函数"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "无法导入 Django，请确保已安装 Django 并且虚拟环境已激活"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
