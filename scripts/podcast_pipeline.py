#!/usr/bin/env python3
"""
鲲鹏志播客生产管线 — L1→L6 矩阵乘法自动化
将双约记原文逐层透析为最终播客脚本

用法: python3 podcast_pipeline.py [chapter] [--layers L1-L6] [--dry-run]
"""
import os, sys, json, argparse, time, re
from pathlib import Path
from openai import OpenAI

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "双约记"
OUT_DIR = SRC_DIR / "podcast"
LITE_LLM_URL = os.environ.get("LITELLM_URL", "http://192.168.31.239:4000/v1")
LITE_LLM_KEY = os.environ.get("LITELLM_KEY", "sk-47318")
MODEL = os.environ.get("PODCAST_MODEL", "company-seed-2-0-lite")

client = OpenAI(base_url=LITE_LLM_URL, api_key=LITE_LLM_KEY)

CHAPTERS = {
    "00": "双约记-序言.md",
    "01": "第一章：1936-1941，旧秩序的崩塌.md",
    "02": "第二章：1941-1945，情报与血祭.md",
    "03": "第三章：1945-1949，冷战铁幕与北约的诞生.md",
    "04": "第四章：1949-1956，大自然厌恶真空：被截断的统一.md",
    "05": "第五章：1956-1966，裂痕对称：华约与北约的双重震荡.md",
    "06": "第六章：1966-1980，凝固的同心圆与燃烧的彗星.md",
    "07": "第七章：1980-2001，文明的脑前叶切除术：世界岛焦土上的记忆清洗.md",
    "08": "第八章：2001-2009，韩信的入场券：血债、英语与订单.md",
    "09": "第九章：2009-2022，雅尔塔的回声.md",
}

# ── Layer Prompts ─────────────────────────────────────────

L1_PROMPT = """你是一位内容提取专家。请对以下原文进行结构化提取：

规则：
1. 提取核心论点（骨架）— 本章最重要的3-5个论点
2. 提取支撑数据（血肉）— 关键数字、日期、人名、事件
3. 提取隐喻/段子（皮肤）— 生动的比喻和有趣的故事
4. 标注优先级：必讲 / 选讲 / 可删

输出格式：
## 骨架
- [必讲] ...
- [选讲] ...

## 血肉
- ...

## 皮肤
- ...

原文：
"""

L2_PROMPT = """你是一位播客对话结构设计师。基于以下结构化提纲，设计一期双人对话播客。

角色设定：
- 峨眉（63岁，川大历史副教授）：主讲人，宏大叙事，学术底色，四川人
- 青衣（38岁，财经记者）：质疑者，数据驱动，追问逻辑

结构要求（四段式）：
1. Warm-up（暖场，30秒）：青衣介绍自己和峨眉，预告主题
2. Opening（开场，1分钟）：峨眉讲缘起、受众、书的价值
3. Main Body（正文，15-18分钟）：峨眉讲骨架→青衣追问→峨眉深化，三拍节奏。禁止连续3句以上同一人独白
4. Closing（结尾，30秒）：青衣总结+下集预告+引导订阅

输出为对话脚本，格式：
[峨眉] ...
[青衣] ...

提纲：
"""

L3_PROMPT = """你是一位四川方言专家。请将以下对话脚本进行四川方言化处理。

规则：
1. 句式转换：是什么→是啥子、怎么了→咋个了、没有→没得、对吗→对不对嘛、是的→要得
2. 语气词：句首加"诶/哎/嚯"、句中加"嘛/撒/哈"、句尾加"咯/噻/嘞"
3. 方言词汇：厉害→凶、舒服→巴适、可以→要得、讨厌→烦、傻→瓜
4. 峨眉的方言程度 > 青衣（峨眉是四川本地人，青衣是从雅安来的）
5. 保持可读性，不要过度方言化导致听不懂

直接输出方言化后的完整对话脚本：
"""

L4_PROMPT = """你是一位文学润色师。请对以下方言对话中**峨眉的段落**进行文学润色。

规则：
1. 排比增强：把平铺直叙改为排比句式
2. 比喻深化：让比喻更加生动和有画面感
3. 适当引用古诗词/名言，但必须用四川话读出来不违和
4. 节奏控制：宏大叙事用长句，强调和转折用短句
5. 只润色峨眉的段落，青衣的段落保持不变

直接输出润色后的完整对话脚本：
"""

L5_PROMPT = """你是一位四川俗语专家。请对以下对话中**青衣的段落**和**两人交锋段落**进行俗语强化。

规则：
1. 四川俚语：龟儿子（强调）、瓜娃子（批评）、扯把子（质疑）、洗白（失败）、锤子（否定）
2. 网络用语适度：RNM退钱、这波在大气层、我直接好家伙
3. 底线：接地气但不低俗，可以用"龟儿子"但不能用真正的脏话
4. 只强化青衣和交锋段落，峨眉的文学段落保持不变

直接输出最终版对话脚本：
"""

L6_PROMPT = """你是一位深夜电台节目包装师。请为以下播客脚本添加电台包装。

节目设定：
- 节目名：《峨眉夜话》
- 频道：成都交通广播 FM103.7（虚构）
- 时段：午夜 00:00-01:00
- 风格：深夜电台 + 茶馆龙门阵

包装要求：
1. 开场：[电台音效: 收音机调频声 + 轻柔BGM淡入] → DJ声 → 青衣暖场
2. 结尾：青衣收束 → 峨眉"安逸。晚安。" → DJ声 → [音乐淡出]
3. 中间插入2-3个Addon（从以下选）：
   - 交通路况（制造直播感）
   - 天气预报（开头或结尾）
   - 听众互动（后半段，听众发短信提问）
   - 假广告（黑色幽默，如"峨眉山茶叶，喝一口，想两天"）
   - 时间提示（每隔5-8分钟）
4. 音效标注用 [方括号] 格式

直接输出完整电台化脚本：
"""

LAYERS = {
    "L1": ("content_extract", L1_PROMPT),
    "L2": ("dialogue_structure", L2_PROMPT),
    "L3": ("sichuan_dialect", L3_PROMPT),
    "L4": ("literary_polish", L4_PROMPT),
    "L5": ("colloquial_intensify", L5_PROMPT),
    "L6": ("radio_wrapper", L6_PROMPT),
}

# ── Pipeline ──────────────────────────────────────────────

def call_llm(prompt: str, content: str, model: str = None) -> str:
    """Call LiteLLM with retry."""
    m = model or MODEL
    for attempt in range(3):
        try:
            resp = client.chat.completions.create(
                model=m,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": content},
                ],
                max_tokens=16000,
                temperature=0.7,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            if attempt < 2:
                print(f"  ⚠ Retry {attempt+1}: {e}")
                time.sleep(3)
            else:
                raise

def read_chapter(ch_id: str) -> str:
    """Read chapter markdown, strip frontmatter."""
    path = SRC_DIR / CHAPTERS[ch_id]
    raw = path.read_text(encoding="utf-8")
    match = re.match(r'^---\s*\n.*?\n---\s*\n', raw, re.DOTALL)
    return raw[match.end():].strip() if match else raw.strip()

def process_chapter(ch_id: str, layers: list[str], dry_run: bool = False, model: str = None):
    """Process a chapter through specified layers."""
    print(f"\n{'='*60}")
    print(f"📖 处理: {CHAPTERS[ch_id]}")
    print(f"{'='*60}")

    content = read_chapter(ch_id)
    results = {"chapter": ch_id, "title": CHAPTERS[ch_id], "original_len": len(content)}

    for layer_id in layers:
        layer_name, prompt = LAYERS[layer_id]
        print(f"\n  ▶ {layer_id}: {layer_name}...")

        if dry_run:
            print(f"    [dry-run] would process {len(content)} chars")
            continue

        start = time.time()
        output = call_llm(prompt, content, model=model)
        elapsed = time.time() - start

        # Save intermediate result
        out_path = OUT_DIR / f"ch{ch_id}_{layer_id}_{layer_name}.md"
        out_path.write_text(output, encoding="utf-8")

        print(f"    ✅ {len(output)} chars, {elapsed:.1f}s → {out_path.name}")
        results[layer_id] = {"chars": len(output), "seconds": round(elapsed, 1), "file": str(out_path)}

        content = output  # chain to next layer

    # Save final script
    if not dry_run:
        final_path = OUT_DIR / f"ch{ch_id}_final.md"
        final_path.write_text(content, encoding="utf-8")
        results["final"] = str(final_path)
        print(f"\n  🎬 Final: {final_path}")

    return results

def main():
    parser = argparse.ArgumentParser(description="鲲鹏志播客生产管线")
    parser.add_argument("chapters", nargs="*", default=list(CHAPTERS.keys()),
                       help="章节 ID (00-09), 默认全部")
    parser.add_argument("--layers", default="L1,L2,L3,L4,L5,L6",
                       help="要跑的层 (逗号分隔), 默认 L1-L6")
    parser.add_argument("--model", default=MODEL, help="模型名")
    parser.add_argument("--dry-run", action="store_true", help="只打印不执行")
    args = parser.parse_args()

    model = args.model
    layers = [l.strip() for l in args.layers.split(",")]

    print(f"🚀 鲲鹏志播客管线 — 模型: {MODEL}, 层: {layers}")
    print(f"📋 章节: {args.chapters}")

    all_results = []
    for ch_id in args.chapters:
        if ch_id not in CHAPTERS:
            print(f"⚠ 未知章节: {ch_id}")
            continue
        result = process_chapter(ch_id, layers, args.dry_run, model=model)
        all_results.append(result)

    # Save manifest
    manifest_path = OUT_DIR / "pipeline_manifest.json"
    manifest_path.write_text(json.dumps(all_results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n📊 Manifest: {manifest_path}")
    print(f"🏁 完成 {len(all_results)} 章")

if __name__ == "__main__":
    main()
