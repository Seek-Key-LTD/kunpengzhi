#!/usr/bin/env python3
"""
从 Hugo public 目录生成 URL 映射并修复内容文件中的链接
"""

import re
import unicodedata
from pathlib import Path

def slugify(text):
    """模拟 Hugo 的 URL slugification"""
    # 转为 unicode 规范化
    text = unicodedata.normalize('NFKC', text)
    # 转小写
    text = text.lower()
    # 替换空格和特殊字符为连字符
    text = re.sub(r'[^\w\u4e00-\u9fff-]', '-', text)
    # 移除连续的连字符
    text = re.sub(r'-+', '-', text)
    # 移除首尾连字符
    text = text.strip('-')
    return text

def get_url_map():
    """从 public 目录提取 URL 映射"""
    public_dir = Path('public')
    url_map = {}  # (section, original_filename) -> actual_url
    
    for html_file in public_dir.rglob('*.html'):
        rel_path = html_file.relative_to(public_dir)
        parts = list(rel_path.parts)
        
        if rel_path.name == 'index.html':
            if len(parts) == 1:  # 根目录的 index.html
                url = '/'
            else:
                url = '/' + '/'.join(parts[:-1]) + '/'
        else:
            url = '/' + '/'.join(parts)
        
        url = url.replace('\\', '/')
        
        # 提取原始文件名（用于匹配链接）
        if len(parts) >= 2:
            section = parts[0]
            filename = parts[-1]
            # 去掉 .html 扩展名
            filename = filename.replace('.html', '')
            url_map[(section, filename)] = url
            url_map[(section, filename.lower())] = url
        elif len(parts) == 1 and parts[0] != 'index.html':
            filename = parts[0].replace('.html', '')
            url_map[(filename,)] = url
            url_map[(filename.lower(),)] = url
    
    return url_map

def fix_content_links():
    """修复内容文件中的链接"""
    content_dir = Path('content')
    url_map = get_url_map()
    
    print(f"📊 生成了 {len(url_map)} 个 URL 映射\n")
    
    md_files = list(content_dir.rglob('*.md'))
    fixed_count = 0
    
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # 匹配 [text](path) 格式的链接
        def fix_link(match):
            text = match.group(1)
            url = match.group(2).rstrip('/')
            
            # 跳过外部链接、锚点
            if url.startswith(('http://', 'https://', 'mailto:', '#')):
                return match.group(0)
            
            # 处理绝对路径
            if url.startswith('/'):
                # 去掉开头的 /
                clean_url = url.lstrip('/')
                parts = clean_url.split('/')
                if len(parts) >= 2:
                    section = parts[0]
                    filename = parts[-1]
                    # 尝试匹配
                    for (sec, fn), actual_url in url_map.items():
                        if sec == section and slugify(fn) in slugify(filename):
                            return f'[{text}]({actual_url})'
                    # 直接尝试 slugify
                    slug = slugify(filename)
                    for (sec, fn), actual_url in url_map.items():
                        if sec == section and slugify(fn) == slug:
                            return f'[{text}]({actual_url})'
                elif len(parts) == 1:
                    for (sec, fn), actual_url in url_map.items():
                        if isinstance(sec, tuple) and sec[0] == slugify(parts[0]):
                            return f'[{text}]({actual_url})'
            else:
                # 相对路径 - 需要根据当前文件位置解析
                pass
            
            return match.group(0)
        
        # 匹配所有 markdown 链接
        pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        content = re.sub(pattern, fix_link, content)
        
        if content != original:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 修复: {md_file.relative_to(content_dir)}")
            fixed_count += 1
    
    print(f"\n{'='*60}")
    print(f"✅ 完成! 共修复 {fixed_count} 个文件")
    print(f"{'='*60}")

if __name__ == '__main__':
    fix_content_links()
