#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
牧人三部曲文档拆分脚本
将三个大文件按章节拆分为Wiki.js格式的小文件
"""

import os
import re
from pathlib import Path

BASE_DIR = Path("/home/ben/kunpengzhi")
SOURCE_DIR = BASE_DIR / "murenji"
TARGET_DIRS = {
    "technology": BASE_DIR / "牧月记",
    "geology": BASE_DIR / "牧兰记", 
    "history": BASE_DIR / "牧人记"
}

def generate_frontmatter(title, description, tags):
    """生成Wiki.js格式的YAML frontmatter"""
    return f"""---
title: "{title}"
description: "{description}"
published: true
date: 2026-05-07T12:00:00.000Z
tags: {tags}
editor: markdown
dateCreated: 2026-05-07T12:00:00.000Z
---
"""

def split_by_chapters(file_path, target_dir, base_tags):
    """按章节拆分文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配章节标题的模式
    chapter_pattern = r'^(第[一二三四五六七八九十]+章|引言|引子|题记|结语|结论|后记|序章|终章)[：:]?\s*(.+?)(?=\n)'
    
    # 找到所有章节位置
    chapters = []
    for match in re.finditer(chapter_pattern, content, re.MULTILINE):
        chapters.append({
            'start': match.start(),
            'title': match.group(0).strip(),
            'chapter_num': match.group(1),
            'chapter_name': match.group(2).strip()
        })
    
    if not chapters:
        print(f"警告: {file_path} 未找到章节")
        return
    
    # 拆分每个章节
    for i, chapter in enumerate(chapters):
        start_pos = chapter['start']
        end_pos = chapters[i+1]['start'] if i+1 < len(chapters) else len(content)
        
        chapter_content = content[start_pos:end_pos].strip()
        
        # 生成文件名(限制长度)
        safe_title = re.sub(r'[^\w\s\u4e00-\u9fff]', '', chapter['title'])
        safe_title = safe_title.replace(' ', '_')
        # 限制文件名长度(最多50个字符)
        if len(safe_title) > 50:
            safe_title = safe_title[:50]
        filename = f"{safe_title}.md"
        
        # 生成完整内容
        full_content = generate_frontmatter(
            title=chapter['title'],
            description=f"{base_tags[0]} - {chapter['title']}",
            tags=str(base_tags)
        ) + "\n" + chapter_content
        
        # 写入文件
        output_path = target_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        print(f"✓ 已创建: {output_path}")

def main():
    """主函数"""
    print("开始拆分牧人三部曲...")
    
    # 确保目标目录存在
    for dir_path in TARGET_DIRS.values():
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # 处理每个文件
    file_configs = [
        ("technology.md", "牧月记", ["牧月记", "技术"]),
        ("geology.md", "牧兰记", ["牧兰记", "地质"]),
        ("history.md", "牧人记", ["牧人记", "历史"])
    ]
    
    for filename, series_name, tags in file_configs:
        source_file = SOURCE_DIR / filename
        target_dir = TARGET_DIRS[filename.split('.')[0]]
        
        if not source_file.exists():
            print(f"✗ 文件不存在: {source_file}")
            continue
        
        print(f"\n处理: {filename}")
        split_by_chapters(source_file, target_dir, tags)
    
    print("\n拆分完成!")

if __name__ == "__main__":
    main()
