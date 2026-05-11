import os
import re
from pathlib import Path

BASE_DIR = Path("/home/ben/kunpengzhi")

def clean_duplicates(book_dir):
    print(f"Cleaning duplicates in {book_dir}...")
    files = list(book_dir.glob("*.md"))
    
    chapters = {}
    for f in files:
        # Match Chapter number or Preface
        match = re.match(r'^(第\d+章|00_序言)', f.name)
        if match:
            prefix = match.group(1)
            if prefix not in chapters: chapters[prefix] = []
            chapters[prefix].append(f)
            
    for prefix, f_list in chapters.items():
        if len(f_list) > 1:
            # We have duplicates. 
            # Strategy: Keep the one with spaces (like "第01章 Chapter Name")
            # Remove the one with underscores (like "第01章_Chapter_Name")
            with_spaces = [f for f in f_list if " " in f.name]
            # Underscore ones that are not the preface or index
            with_underscores = [f for f in f_list if "_" in f.name and f.name.name not in ["00_序言.md", "目录.md"]]
            
            if with_spaces and with_underscores:
                for f in with_underscores:
                    print(f"  - Deleting underscore version: {f.name}")
                    f.unlink()
            elif len(f_list) > 1:
                # Fallback: keep the first one
                f_list.sort(key=lambda x: len(x.name), reverse=True)
                for f in f_list[1:]:
                    print(f"  - Deleting extra duplicate: {f.name}")
                    f.unlink()

def regenerate_index(book_dir, book_name):
    print(f"Regenerating index for {book_name}...")
    files = sorted([f for f in book_dir.glob("*.md") if f.name != "目录.md"])
    index_items = []
    
    for f_path in files:
        with open(f_path, 'r', encoding='utf-8') as fr:
            content = fr.read()
            match = re.search(r'^title:\s*"(.*?)"', content, re.MULTILINE)
            title = match.group(1) if match else f_path.stem
            
        index_items.append(f"- [{title}]({f_path.stem})")
        
    index_content = f"---\ntitle: \"{book_name}：目录\"\npublished: \"true\"\neditor: \"markdown\"\n---\n\n# {book_name}：目录\n\n" + "\n".join(index_items)
    with open(book_dir / "目录.md", 'w', encoding='utf-8') as f:
        f.write(index_content)

def main():
    for book in ["牧人记", "牧兰记", "牧月记", "双约记"]:
        book_path = BASE_DIR / book
        if book_path.exists():
            clean_duplicates(book_path)
            regenerate_index(book_path, book)
    print("Cleanup successful.")

if __name__ == "__main__":
    main()
