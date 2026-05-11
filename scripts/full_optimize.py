import re
import os
from pathlib import Path

def split_long_paragraphs(text, max_len=400):
    """
    如果段落过长，在句号、感叹号或问号处尝试分段。
    """
    paragraphs = text.split('\n\n')
    new_paragraphs = []
    
    for p in paragraphs:
        if len(p) <= max_len:
            new_paragraphs.append(p)
            continue
        
        # 尝试在句号、感叹号、问号后加换行，但要避免在双引号内或特殊情况下误伤
        # 这里使用正则：匹配 (。|！|？) 后面跟着非结束符的内容
        # 我们寻找最接近中间位置的标点符号进行拆分
        parts = re.split(r'([。！？])', p)
        
        current_p = ""
        sub_paragraphs = []
        
        # 重新组合句子，当长度超过阈值时断开
        for i in range(0, len(parts)-1, 2):
            sentence = parts[i] + parts[i+1]
            if len(current_p) + len(sentence) > max_len and current_p:
                sub_paragraphs.append(current_p.strip())
                current_p = sentence
            else:
                current_p += sentence
        
        if current_p:
            sub_paragraphs.append(current_p.strip())
        
        # 如果最后一段还是太长（可能没标点），就直接放进去
        if not sub_paragraphs:
            new_paragraphs.append(p)
        else:
            new_paragraphs.extend(sub_paragraphs)
            
    return '\n\n'.join(new_paragraphs)

def fix_content(content):
    """
    1. 标题标准化 (##)
    2. 段落拆分
    """
    # 分段处理 (跳过 frontmatter)
    parts = content.split('---', 2)
    if len(parts) < 3:
        # 没有 frontmatter
        body = content
        header = ""
    else:
        header = f"---{parts[1]}---"
        body = parts[2]

    # 1. 标题标准化 (##)
    # 匹配：第一节、楔子、尾声、第01章（有些文件名是这样的）
    patterns = [
        (r'^(第[一二三四五六七八九十]+节\s+.*)$', r'## \1'),
        (r'^(楔子[·\s].*)$', r'## \1'),
        (r'^(尾声\s+.*)$', r'## \1'),
        (r'^(引子[·\s].*)$', r'## \1'),
    ]
    
    for pattern, replacement in patterns:
        body = re.sub(pattern, replacement, body, flags=re.MULTILINE)
    
    # 2. 段落拆分
    body = split_long_paragraphs(body)
    
    return header + body

def process_all():
    books = ['牧人记', '牧兰记', '牧月记', '双约记', '词根考据']
    files_count = 0
    
    for book in books:
        book_path = Path(book)
        if not book_path.exists():
            continue
            
        for md_file in book_path.glob('*.md'):
            if md_file.name in ['目录.md', '_index.md']:
                continue
            
            with open(md_file, 'r', encoding='utf-8') as f:
                old_content = f.read()
            
            new_content = fix_content(old_content)
            
            if new_content != old_content:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Optimized: {md_file}")
                files_count += 1
                
    print(f"\nTotal files optimized: {files_count}")

if __name__ == "__main__":
    process_all()
