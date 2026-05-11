import os
import re
from pathlib import Path

BASE_DIR = Path("/home/ben/kunpengzhi")

def clean_duplicates(book_dir):
    print(f"Cleaning duplicates in {book_dir}...")
    files = list(book_dir.glob("*.md"))
    
    # We want to keep files that match the "Title" closely (often has spaces)
    # and remove the ones that have underscores replacing spaces.
    
    # Group files by their chapter number prefix (e.g. "第01章")
    chapters = {}
    for f in files:
        match = re.match(r'^(第\d+章|00_序言)', f.name)
        if match:
            prefix = match.group(1)
            if prefix not in chapters: chapters[prefix] = []
            chapters[prefix].append(f)
            
    for prefix, f_list in chapters.items():
        if len(f_list) > 1:
            # Decide which one to keep. Prefer the one with spaces.
            with_spaces = [f for f in f_list if " " in f.name]
            with_underscores = [f for f in f_list if "_" in f.name and f.name not in ["00_序言.md", "目录.md"]]
            
            # If we have both, remove underscore ones
            if with_spaces and with_underscores:
                for f in with_underscores:
                    print(f"  - Removing underscore duplicate: {f.name}")
                    f.unlink()
            elif len(f_list) > 1:
                # If no clear space/underscore distinction but still multiple, 
                # keep the longest name?
                f_list.sort(key=lambda x: len(x.name), reverse=True)
                for f in f_list[1:]:
                    print(f"  - Removing extra duplicate: {f.name}")
                    f.unlink()

def regenerate_index(book_dir, book_name):
    print(f"Regenerating index for {book_name}...")
    files = sorted([f for f in book_dir.glob("*.md") if f.name != "目录.md"])
    index_items = []
    
    for f in files:
        # Get title from frontmatter
        with open(f, 'r', encoding='utf-8') as fr:
            content = f.read()
            match = re.search(r'^title:\s*"(.*?)"', content, re.MULTILINE)
            title = match.group(1) if match else f.stem
            
        # Link to the filename without .md
        index_items.append(f"- [{title}]({f.stem})")
        
    index_content = f"---\ntitle: \"{book_name}：目录\"\npublished: \"true\"\neditor: \"markdown\"\n---\n\n# {book_name}：目录\n\n" + "\n".join(index_items)
    with open(book_dir / "目录.md", 'w', encoding='utf-8') as f:
        f.write(index_content)

def main():
    for book in ["牧人记", "牧兰记", "牧月记", "双约记"]:
        book_path = BASE_DIR / book
        if book_path.exists():
            clean_duplicates(book_path)
            regenerate_index(book_path, book)
    print("Cleanup complete.")

if __name__ == "__main__":
    main()
