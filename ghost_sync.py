import os
import re
import json
import jwt
import requests
import time
import yaml
from datetime import datetime
from markdown_it import MarkdownIt

# Configuration
WIKI_BASE_URL = "https://wiki.seekkey.eu.org"
GHOST_API_URL = "https://blog.seekkey.eu.org"
GHOST_ADMIN_KEY = "69fbe9db4076c7000180768b:fd4350040c541ecd088ab0d4ff44c10774cb04ad2414bb8fae2a0daf378bdef2"

def generate_token(key):
    id, secret = key.split(':')
    iat = int(time.time())
    
    header = {'alg': 'HS256', 'typ': 'JWT', 'kid': id}
    payload = {
        'iat': iat,
        'exp': iat + 5 * 60,
        'aud': '/admin/'
    }
    
    return jwt.encode(payload, bytes.fromhex(secret), algorithm='HS256', headers=header)

def parse_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_content = f.read()
    
    # Use regex to match frontmatter between the first two sets of ---
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', raw_content, re.DOTALL)
    if match:
        try:
            fm_text = match.group(1)
            md_content = raw_content[match.end():].strip()
            frontmatter = yaml.safe_load(fm_text)
            return frontmatter, md_content
        except Exception as e:
            print(f"⚠ Frontmatter error in {file_path}: {e}")
    
    return {}, raw_content.strip()

# 字体配置 (霞鹜文楷)
FONT_INJECTION = """
<link rel="stylesheet" href="https://npm.elemecdn.com/lxgw-wenkai-screen-webfont@1.1.0/style.css" />
<style>
  html, body, .gh-content, .gh-canvas, h1, h2, h3, h4, h5, h6, .gh-article-title {
    font-family: 'LXGW WenKai Screen', serif !important;
  }
  .gh-content p {
    font-size: 1.25rem !important;
    line-height: 1.85 !important;
    letter-spacing: 0.01em !important;
    text-align: justify;
    margin-bottom: 1.5em;
  }
  /* 标题稍微加粗 */
  h1, h2, h3 { font-weight: 700; color: #15171a; }
</style>
"""

def sync_post(file_path):
    frontmatter, md_content = parse_markdown(file_path)
    if not md_content:
        return

    title = frontmatter.get('title', os.path.basename(file_path).replace('.md', ''))
    rel_path = os.path.relpath(file_path, os.getcwd()).replace('.md', '')
    wiki_link = f"{WIKI_BASE_URL}/{rel_path}"
    
    # 构建内容
    wiki_footer = f"\n\n---\n\n**查看详细认知图谱与词根考据：** [{title}]({wiki_link})"
    full_md = md_content + wiki_footer
    
    # 转换为 HTML
    md = MarkdownIt()
    html_content = md.render(full_md)
    
    # 合并 FONT_INJECTION 和正文 HTML (将注入放在文章最前面)
    final_html = FONT_INJECTION + html_content
    
    print(f"DEBUG: {title} - Content Size: {len(md_content)} bytes")
    
    # 使用 Lexical 格式包装，确保 Ghost 5.x 接受内容
    import json
    lexical_data = {
        "root": {
            "children": [
                {
                    "type": "html",
                    "version": 1,
                    "html": final_html
                }
            ],
            "direction": None,
            "format": "",
            "indent": 0,
            "type": "root",
            "version": 1
        }
    }
    
    token = generate_token(GHOST_ADMIN_KEY)
    headers = {'Authorization': f'Ghost {token}'}
    
    slug = frontmatter.get('slug', rel_path.replace('/', '-'))
    lookup_url = f"{GHOST_API_URL}/ghost/api/admin/posts/slug/{slug}/"
    res = requests.get(lookup_url, headers=headers)
    
    # 准备 Payload
    post_payload = {
        "title": title,
        "lexical": json.dumps(lexical_data),
        "status": "published", # 改为发布状态，避免 404
        "slug": slug,
        "tags": frontmatter.get('tags', []),
        "codeinjection_head": FONT_INJECTION, # 这里是 Ghost 官方推荐的样式注入位
        "feature_image": frontmatter.get('image', frontmatter.get('feature_image'))
    }
    
    if res.status_code == 200:
        existing_post = res.json()['posts'][0]
        post_id = existing_post['id']
        update_url = f"{GHOST_API_URL}/ghost/api/admin/posts/{post_id}/?formats=html,lexical,mobiledoc"
        post_payload['updated_at'] = existing_post['updated_at']
        res = requests.put(update_url, json={"posts": [post_payload]}, headers=headers)
        action = "Updated"
    else:
        create_url = f"{GHOST_API_URL}/ghost/api/admin/posts/?formats=html,lexical,mobiledoc"
        res = requests.post(create_url, json={"posts": [post_payload]}, headers=headers)
        action = "Created"
    
    if res.status_code in [200, 201]:
        print(f"✓ {action} Ghost post: {title}")
        # Safely check returned content
        returned_post = res.json().get('posts', [{}])[0]
        html_out = returned_post.get('html')
        html_len = len(html_out) if html_out else 0
        lexical_out = returned_post.get('lexical')
        lexical_len = len(lexical_out) if lexical_out else 0
        print(f"   Ghost storage: HTML={html_len} bytes, Lexical={lexical_len} bytes")
    else:
        print(f"✗ Failed to sync {title}: Status {res.status_code}")
        print(f"   Error: {res.text}")

def sync_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md') and not file.startswith('index'):
                file_path = os.path.join(root, file)
                try:
                    sync_post(file_path)
                except Exception as e:
                    print(f"⚠ Failed to sync {file_path}: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if os.path.isdir(path):
            sync_directory(path)
        else:
            sync_post(path)
    else:
        print("Usage: python ghost_sync.py <path_to_markdown_or_dir>")
