import os
import re
from pathlib import Path

BASE_DIR = Path("/home/ben/kunpengzhi")

def cn_num(n):
    units = ["", "一", "二", "三", "四", "五", "六", "七", "八", "九"]
    if n < 10: return units[n]
    elif n == 10: return "十"
    elif n < 20: return "十" + units[n % 10]
    else:
        d, r = divmod(n, 10)
        return units[d] + "十" + units[r]

def get_frontmatter(content):
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if match:
        fm_text = match.group(1)
        fm = {}
        for line in fm_text.split('\n'):
            if ':' in line:
                k, v = line.split(':', 1)
                fm[k.strip()] = v.strip().strip('"').strip("'")
        return fm, content[match.end():]
    return {}, content

def generate_frontmatter(data):
    lines = ["---"]
    for k, v in data.items():
        if isinstance(v, list): lines.append(f"{k}: {v}")
        else: lines.append(f"{k}: \"{v}\"")
    lines.append("---")
    return "\n".join(lines) + "\n"

def rebuild_book_properly(book_key, book_name, tags):
    print(f"Rebuilding {book_name} with cohesive chapters and linear numbering...")
    source_file = BASE_DIR / "murenji" / f"{book_key}.md"
    dest_dir = BASE_DIR / book_name
    
    if not source_file.exists(): return
    if dest_dir.exists():
        for f in dest_dir.glob("*.md"): f.unlink()
    else:
        dest_dir.mkdir(exist_ok=True)

    with open(source_file, 'r', encoding='utf-8') as f:
        full_text = f.read()
    
    _, content = get_frontmatter(full_text)
    lines = content.split('\n')
    
    # Identify positions of "第...章"
    # Note: We exclude internal chapters of the Technology book audit report (if they are nested)
    # But wait, user said "Merge what should be merged". 
    # For Technology, we already decided Ch 5 is one big block.
    
    chapter_indices = []
    for i, line in enumerate(lines):
        if re.match(r'^第[一二三四五六七八九十百]+章', line.strip()):
            # Special case for Technology nested chapters
            if book_key == "technology" and "第五章" in line:
                chapter_indices.append(i)
                # Skip internal chapters 1-6 of the audit report
                # These internal ones usually have titles like "第一章：$\pi$ 的本体论危机"
            elif book_key == "technology" and any(f"第{cn_num(j)}章" in line for r in range(1,7) for j in [r]):
                # If we are already past Ch 5 but before Ch 6, it might be nested
                # Actually, let's just manually check if it's the BIG Ch 6
                if "量子计算" in line:
                    chapter_indices.append(i)
                else:
                    # Likely nested
                    pass
            else:
                chapter_indices.append(i)
                
    # If no chapters found (unlikely), handle
    if not chapter_indices:
        # Just save the whole thing as one chapter?
        chapter_indices = [0]

    # Grouping Intros with following Chapters
    # We look backwards from each Chapter start to see if there's an Intro/Title
    refined_starts = []
    intro_patterns = [r'^引言', r'^引子', r'^题记', r'^前言', r'^序言', r'^序章', r'^\[.*\.m4a\]', r'^\[.*\.mp4\]']
    
    for start_idx in chapter_indices:
        actual_start = start_idx
        # Look back up to 10 lines for intros or titles
        for b in range(1, 15):
            prev_idx = start_idx - b
            if prev_idx < 0: break
            prev_line = lines[prev_idx].strip()
            if not prev_line: continue
            
            # If we hit the previous chapter's content, stop
            if refined_starts and prev_idx <= refined_starts[-1]['end']: break
            
            is_intro = any(re.match(p, prev_line) for p in intro_patterns)
            # Or if it's a short line that looks like a title (between Essays)
            is_essay_title = len(prev_line) < 50 and not prev_line.endswith('。') and not prev_line.endswith('”')
            
            if is_intro or is_essay_title:
                actual_start = prev_idx
            else:
                # If it's just regular text, we stop looking back
                break
        
        refined_starts.append({'start': actual_start, 'orig_ch_idx': start_idx})

    # Now we have the start points. Set the ends.
    for i in range(len(refined_starts)):
        if i + 1 < len(refined_starts):
            refined_starts[i]['end'] = refined_starts[i+1]['start'] - 1
        else:
            refined_starts[i]['end'] = len(lines) - 1

    # Before the first chapter, there might be a global Preface
    pre_chapter_content = []
    if refined_starts[0]['start'] > 0:
        pre_chapter_content = lines[0:refined_starts[0]['start']]
        # Check if there is actual content or just metadata
        if any(l.strip() for l in pre_chapter_content):
            with open(dest_dir / "00_序言.md", 'w', encoding='utf-8') as f:
                fm = {"title": "序言", "description": f"{book_name} - 序言", "book": book_name, "published": "true", "date": "2026-05-07T12:00:00.000Z", "tags": tags, "editor": "markdown"}
                f.write(generate_frontmatter(fm) + "\n" + "\n".join(pre_chapter_content))

    # Save chapters
    index_items = []
    if (dest_dir / "00_序言.md").exists():
        index_items.append("- [序言](00_序言)")

    for i, chunk in enumerate(refined_starts, 1):
        chunk_lines = lines[chunk['start'] : chunk['end']+1]
        
        # Original chapter line for title extraction
        orig_ch_line = lines[chunk['orig_ch_idx']].strip()
        match = re.match(r'^第[一二三四五六七八九十百]+章[：: ]?\s*(.*)$', orig_ch_line)
        raw_title = match.group(1) if match else "未命名章节"
        if not raw_title: raw_title = "未命名章节"
        
        # Correct the chapter number in the text
        chunk_lines[chunk['orig_ch_idx'] - chunk['start']] = f"第{cn_num(i)}章 {raw_title}"
        
        # Filename
        safe_title = raw_title.replace(":", "：").replace("/", "／").replace("\\", "＼").replace("*", "").replace("?", "？").replace(" ", "_")
        if len(safe_title) > 40: safe_title = safe_title[:40]
        filename = f"第{i:02d}章_{safe_title}.md"
        
        display_title = f"第{cn_num(i)}章 {raw_title}"
        fm = {"title": display_title, "description": f"{book_name} - {display_title}", "book": book_name, "published": "true", "date": "2026-05-07T12:00:00.000Z", "tags": tags, "editor": "markdown"}
        
        with open(dest_dir / filename, 'w', encoding='utf-8') as f:
            f.write(generate_frontmatter(fm) + "\n" + "\n".join(chunk_lines))
        
        index_items.append(f"- [{display_title}]({filename[:-3]})")
        print(f"  ✓ {filename}")

    # Index
    index_content = f"---\ntitle: \"{book_name}：目录\"\npublished: \"true\"\neditor: \"markdown\"\n---\n\n# {book_name}：目录\n\n" + "\n".join(index_items)
    with open(dest_dir / "目录.md", 'w', encoding='utf-8') as f:
        f.write(index_content)

def main():
    rebuild_book_properly("history", "牧人记", ["牧人记", "历史"])
    rebuild_book_properly("geology", "牧兰记", ["牧兰记", "地质"])
    rebuild_book_properly("technology", "牧月记", ["牧月记", "技术"])
    print("\nProper cohesive rebuild complete.")

if __name__ == "__main__":
    main()
