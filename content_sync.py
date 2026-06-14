#!/usr/bin/env python3
"""
鲲鹏志 · 内容分发自动化 (Content Distribution Pipeline)
========================================================
将 main 分支的源内容同步到各发布分支（ghost, bookstack, confluence 等），
处理分支特有的格式差异（frontmatter、文件命名、目录结构）。

用法:
  python3 content_sync.py --target ghost    # 同步到 ghost 分支
  python3 content_sync.py --target bookstack # 同步到 bookstack 分支
  python3 content_sync.py --all              # 同步所有目标分支
  python3 content_sync.py --status            # 仅检查差异
"""

import os
import sys
import shutil
import tempfile
import subprocess
import re
import yaml
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parent

# ============================================================
# 四书章节来源：main 分支上的标准目录
# ============================================================
BOOKS = {
    "牧月记": {
        "dir": "牧月记",
        "pattern": r"^第\d+章",
        "preface": "00_序言.md",
        "toc": "目录.md",
    },
    "牧兰记": {
        "dir": "牧兰记",
        "pattern": r"^第\d+章",
        "preface": "00_序言.md",
        "toc": "目录.md",
    },
    "牧人记": {
        "dir": "牧人记",
        "pattern": r"^第\d+章",
        "preface": None,
        "toc": "目录.md",
    },
    "双约记": {
        "dir": "双约记",
        "pattern": r"^第[一二三四五六七八九]",
        "preface": "双约记-序言.md",
        "toc": "双约记-目录.md",
    },
}

# ============================================================
# 目标分支配置
# ============================================================
TARGETS = {
    "ghost": {
        "description": "Ghost CMS (blog.seekkey.eu.org)",
        "branch": "ghost",
        "keep_files": [
            ".env",
            ".gitlab-ci.yml",
            "BRANCHING.md",
            "BRANCHING.md",
            "GOVERNANCE.md",
            "MANIFEST.md",
            "README.md",
            "agents.md",
            "deploy-drupal.yml",
            "etymology.md",
            "etymology/",
            "ghost_sync.py",
            "home.md",
            "murenji.md",
            "murenji/",
            "shuangyueji.md",
            "shuangyueji/",
            "wikijs_index_generator.py",
        ],
        "copy_books": True,
        "book_mapping": None,  # keep original filenames
        "frontmatter_transform": "ghost",
    },
    "bookstack": {
        "description": "BookStack 英文版",
        "branch": "bookstack",
        "keep_files": [
            ".env",
            ".gitlab-ci.yml",
            "BRANCHING.md",
            "GOVERNANCE.md",
            "MANIFEST.md",
            "README.md",
            "agents.md",
            "deploy-drupal.yml",
            "etymology.md",
            "etymology/",
            "ghost_sync.py",
            "home.md",
            "murenji.md",
            "murenji/",
            "shuangyueji.md",
            "shuangyueji/",
            "wikijs_index_generator.py",
        ],
        "copy_books": True,
        "book_mapping": None,
        "frontmatter_transform": "bookstack",
    },
}


def log(msg, level="INFO"):
    print(f"[{level}] {msg}")


def run_git(*args, cwd=REPO_ROOT):
    """执行 git 命令"""
    result = subprocess.run(
        ["git"] + list(args),
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        log(f"Git error: {result.stderr.strip()}", "WARN")
    return result.stdout.strip()


def get_current_branch():
    return run_git("rev-parse", "--abbrev-ref", "HEAD")


def ensure_branch(branch_name):
    """确保目标分支存在并切换到它"""
    branches = run_git("branch", "--list", branch_name)
    if not branches:
        log(f"创建新分支: {branch_name}")
        run_git("checkout", "-b", branch_name, "origin/main")
    else:
        run_git("checkout", branch_name)
    return True


def collect_chapter_files(book_name, book_config):
    """从 main 分支收集某本书的章节文件列表"""
    book_dir = REPO_ROOT / book_config["dir"]
    if not book_dir.exists():
        log(f"目录不存在: {book_dir}", "WARN")
        return []
    
    files = []
    for f in sorted(book_dir.iterdir()):
        if not f.is_file() or not f.suffix == ".md":
            continue
        name = f.name
        # 跳过非章节文件
        if name in (book_config.get("preface"), book_config.get("toc")):
            continue
        if re.match(book_config["pattern"], name):
            files.append(f)
    
    return files


def sync_branch(target_name):
    """同步内容到目标分支"""
    target = TARGETS[target_name]
    branch = target["branch"]
    
    log(f"开始同步 → {target_name} ({target['description']})")
    log(f"目标分支: {branch}")
    
    # 保存当前分支以便恢复
    orig_branch = get_current_branch()
    log(f"当前分支: {orig_branch}")
    
    try:
        # 切换到目标分支
        run_git("checkout", branch)
        
        # 复制四书内容
        if target["copy_books"]:
            log("复制四书章节文件...")
            for book_name, book_config in BOOKS.items():
                src_dir = REPO_ROOT / book_config["dir"]
                dst_dir = REPO_ROOT / book_config["dir"]
                
                if not src_dir.exists():
                    log(f"  源目录不存在: {src_dir} (可能需要在 main 分支)", "WARN")
                    continue
                
                os.makedirs(dst_dir, exist_ok=True)
                
                files = collect_chapter_files(book_name, book_config)
                log(f"  {book_name}: {len(files)} 个章节文件")
                
                for src_file in files:
                    dst_path = dst_dir / src_file.name
                    shutil.copy2(src_file, dst_path)
                    
                    # 应用 frontmatter 转换
                    if target.get("frontmatter_transform"):
                        transform_frontmatter(dst_path, book_name, target["frontmatter_transform"])
                
                # 复制 preface 和 toc
                for extra in ["preface", "toc"]:
                    extra_file = book_config.get(extra)
                    if extra_file:
                        src_extra = src_dir / extra_file
                        if src_extra.exists():
                            dst_extra = dst_dir / extra_file
                            shutil.copy2(src_extra, dst_extra)
                            log(f"    复制: {extra_file}")
        
        # 提交变更
        result = run_git("status", "--porcelain")
        if result:
            run_git("add", "-A")
            run_git("commit", "-m", f"chore(sync): 自动同步四书内容到 {branch} 分支 [{datetime.now().strftime('%Y-%m-%d %H:%M')}]")
            log("✅ 已提交变更")
            
            # 推送到远程
            run_git("push", "origin", branch)
            log(f"✅ 已推送到 origin/{branch}")
        else:
            log("📭 无变更，跳过提交")
    
    finally:
        # 切回原始分支
        run_git("checkout", orig_branch)
        log(f"已切回: {orig_branch}")


def transform_frontmatter(file_path, book_name, transform_type):
    """根据目标平台转换 frontmatter"""
    content = file_path.read_text(encoding="utf-8")
    
    # 解析现有 frontmatter
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return
    
    try:
        fm = yaml.safe_load(match.group(1))
    except Exception:
        return
    
    if not isinstance(fm, dict):
        return
    
    body = content[match.end():]
    
    if transform_type == "ghost":
        # Ghost 需要的 frontmatter 格式
        fm["published"] = fm.get("published", "true")
        if "date" not in fm:
            fm["date"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
        if "tags" not in fm or not fm["tags"]:
            fm["tags"] = [book_name]
        # 确保 description 存在
        if "description" not in fm:
            fm["description"] = fm.get("title", str(file_path.stem))
        # 确保 editor 字段
        fm["editor"] = "markdown"
    
    elif transform_type == "bookstack":
        # BookStack 用的格式
        fm["published"] = "true"
        fm["book"] = book_name
        if "tags" not in fm or not fm["tags"]:
            fm["tags"] = [book_name]
    
    # 重新写入
    new_frontmatter = yaml.dump(fm, allow_unicode=True, sort_keys=False, default_flow_style=False).strip()
    new_content = f"---\n{new_frontmatter}\n---\n\n{body.strip()}\n"
    file_path.write_text(new_content, encoding="utf-8")


def check_status():
    """检查各分支内容同步状态"""
    log("检查内容同步状态...\n")
    
    orig_branch = get_current_branch()
    
    for target_name, target in TARGETS.items():
        branch = target["branch"]
        run_git("checkout", branch)
        
        total = 0
        for book_name, book_config in BOOKS.items():
            files = collect_chapter_files(book_name, book_config)
            total += len(files)
        
        status = "✅" if total > 30 else "⚠️"
        log(f"  {status} {target_name} ({branch}): {total} 个章节文件")
    
    run_git("checkout", orig_branch)
    log(f"\n已切回: {orig_branch}")


def sync_all():
    """同步所有目标分支"""
    for target_name in TARGETS:
        sync_branch(target_name)


def setup_gitlab_ci():
    """更新 .gitlab-ci.yml 加入内容分发管线"""
    log("检查 .gitlab-ci.yml 是否需要更新...")
    
    ci_path = REPO_ROOT / ".gitlab-ci.yml"
    content = ci_path.read_text() if ci_path.exists() else ""
    
    # 如果已经有 sync 阶段且包含 copy-books，则跳过
    if "content-distribute" in content:
        log("✅ .gitlab-ci.yml 已包含分发管线")
        return
    
    new_stage = """
# =========================================
# 内容分发：main 更新时自动同步到各发布分支
# =========================================
content-distribute:
  stage: sync
  tags: [group]
  script:
    - |
      echo "🔄 开始内容分发..."
      # 同步到 ghost 分支
      python3 content_sync.py --target ghost
      # 同步到 bookstack 分支
      python3 content_sync.py --target bookstack
      echo "✅ 内容分发完成"
  only:
    - main
    
# =========================================
# Ghost 发布：同步内容后推送到 Ghost CMS
# =========================================
publish-ghost:
  stage: sync
  tags: [group]
  script:
    - |
      echo "📝 发布到 Ghost CMS..."
      # 切到 ghost 分支运行 ghost_sync.py
      git checkout ghost
      python3 ghost_sync.py 牧人记/
      python3 ghost_sync.py 牧兰记/
      python3 ghost_sync.py 牧月记/
      python3 ghost_sync.py 双约记/
      echo "✅ Ghost 发布完成"
  only:
    - ghost
"""
    
    # 追加到 stages 后
    if "stages:" in content:
        if "  - sync" not in content:
            content = content.replace("stages:", "stages:\n  - sync")
        content += new_stage
        ci_path.write_text(content)
        log("✅ .gitlab-ci.yml 已更新")
    else:
        log(".gitlab-ci.yml 格式异常，请手动检查", "WARN")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1]
    
    if command == "--status":
        check_status()
    elif command == "--target":
        if len(sys.argv) < 3:
            log("请指定目标分支: --target ghost|bookstack", "ERROR")
            return
        target = sys.argv[2]
        if target not in TARGETS:
            log(f"未知目标: {target}，可选: {list(TARGETS.keys())}", "ERROR")
            return
        sync_branch(target)
    elif command == "--all":
        sync_all()
    elif command == "--setup-ci":
        setup_gitlab_ci()
    else:
        print(f"未知命令: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()
