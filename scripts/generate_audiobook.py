#!/usr/bin/env python3
"""
Audiobook 格式生成器
为双约记章节生成 audiobook 版本，添加 [章节开始]/[章节结束] 锚点
"""
import os
import re
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "双约记"
OUT_DIR = SRC_DIR / "audiobook"

# 章节映射 (文件名 -> 序号)
CHAPTER_MAP = {
    "双约记-序言.md": ("00", "序言"),
    "第一章：1936-1941，旧秩序的崩塌.md": ("01", "第一章：1936-1941，旧秩序的崩塌"),
    "第二章：1941-1945，情报与血祭.md": ("02", "第二章：1941-1945，情报与血祭"),
    "第三章：1945-1949，冷战铁幕与北约的诞生.md": ("03", "第三章：1945-1949，冷战铁幕与北约的诞生"),
    "第四章：1949-1956，大自然厌恶真空：被截断的统一.md": ("04", "第四章：1949-1956，大自然厌恶真空：被截断的统一"),
    "第五章：1956-1966，裂痕对称：华约与北约的双重震荡.md": ("05", "第五章：1956-1966，裂痕对称：华约与北约的双重震荡"),
    "第六章：1966-1980，凝固的同心圆与燃烧的彗星.md": ("06", "第六章：1966-1980，凝固的同心圆与燃烧的彗星"),
    "第七章：1980-2001，文明的脑前叶切除术：世界岛焦土上的记忆清洗.md": ("07", "第七章：1980-2001，文明的脑前叶切除术"),
    "第八章：2001-2009，韩信的入场券：血债、英语与订单.md": ("08", "第八章：2001-2009，韩信的入场券：血债、英语与订单"),
    "第九章：2009-2022，雅尔塔的回声.md": ("09", "第九章：2009-2022，雅尔塔的回声"),
}


def parse_markdown(file_path):
    """解析 markdown，提取 frontmatter 和正文"""
    raw = file_path.read_text(encoding="utf-8")
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', raw, re.DOTALL)
    if match:
        try:
            fm = yaml.safe_load(match.group(1))
        except Exception:
            fm = {}
        body = raw[match.end():].strip()
        return fm, body
    return {}, raw.strip()


def split_sections(body):
    """按 ## 标题拆分章节为小节"""
    # 匹配 ## 开头的标题行
    sections = []
    current_title = None
    current_lines = []
    
    for line in body.split('\n'):
        if re.match(r'^##\s', line):
            if current_title is not None:
                sections.append((current_title, '\n'.join(current_lines).strip()))
            current_title = line.strip()
            current_lines = []
        else:
            if current_title is None:
                current_title = "__preamble__"
            current_lines.append(line)
    
    if current_title is not None:
        sections.append((current_title, '\n'.join(current_lines).strip()))
    
    return sections


def generate_audiobook(src_filename):
    """生成单个文件的 audiobook 版本"""
    src_path = SRC_DIR / src_filename
    if not src_path.exists():
        print(f"  ⚠️ 源文件不存在: {src_path}")
        return None
    
    ch_id, ch_title = CHAPTER_MAP.get(src_filename, ("XX", src_filename.replace('.md', '')))
    
    fm, body = parse_markdown(src_path)
    
    # 更新 frontmatter
    fm["format"] = "audiobook"
    fm["chapter_id"] = ch_id
    fm["status"] = "draft"
    
    # 拆分小节
    sections = split_sections(body)
    
    # 构建 audiobook 内容
    lines = []
    lines.append(f"[章节开始] {ch_title}")
    lines.append("")
    
    for sec_title, sec_content in sections:
        if sec_title == "__preamble__":
            # 序言/诗部分
            if sec_content.strip():
                lines.append(sec_content)
                lines.append("")
        else:
            lines.append(f"[节开始] {sec_title}")
            lines.append("")
            lines.append(sec_content)
            lines.append("")
            lines.append("[节结束]")
            lines.append("")
    
    lines.append("[章节结束]")
    
    # 构建新 frontmatter
    new_fm = yaml.dump(fm, allow_unicode=True, sort_keys=False, default_flow_style=False).strip()
    new_body = '\n'.join(lines)
    new_content = f"---\n{new_fm}\n---\n\n{new_body}\n"
    
    # 写入
    out_path = OUT_DIR / f"ch{ch_id}.md"
    out_path.write_text(new_content, encoding="utf-8")
    print(f"  ✅ ch{ch_id}.md — {ch_title}")
    return out_path


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("🎧 生成双约记 Audiobook 格式...\n")
    
    files = sorted(CHAPTER_MAP.keys(), 
                   key=lambda f: CHAPTER_MAP[f][0])
    
    generated = []
    for f in files:
        result = generate_audiobook(f)
        if result:
            generated.append(result)
    
    print(f"\n✅ 完成: {len(generated)} 个 audiobook 文件 → {OUT_DIR}")
    return generated


if __name__ == "__main__":
    main()
