#!/usr/bin/env python3
"""
鲲鹏志 · 擂台 — 4v4 大专辩论会 + 讲茶大堂
============================================
源于 Flow（4v4 辩论），高于 Flow（讲茶大堂场外评论）
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ─── 辩题 ─────────────────────────────────────────
DEBATE_TOPICS = {
    "1": {
        "title": "白貂皮大衣：全球贸易网络的铁证 vs 过度诠释的 cherry-picking",
        "pro": "白貂皮大衣是嚈哒帝国与东北亚保持联系的铁证，证明大同流亡军团理论",
        "con": "白貂皮大衣不过是转手贸易的结果，用来论证族群记忆是过度诠释",
        "background": "/home/ben/kunpengzhi/digest/小题大做/题1-白貂皮大衣.md",
    },
    "2": {
        "title": "木兰的哥哥：历史真相 vs 叙事虚构",
        "pro": "木兰无长兄的真正含义是长兄参加了大同流亡军团西征",
        "con": "木兰无长兄就是文学修辞，强行关联嚈哒帝国是过度解读",
        "background": "/home/ben/kunpengzhi/digest/小题大做/题2-木兰的哥哥.md",
    },
    "3": {
        "title": "产权分割理论：安史之乱的本质是经济规律 vs 庸俗经济学滥用",
        "pro": "安史之乱=大股东收购母公司，产权分割理论是理解政治史的利器",
        "con": "用企业并购解释安史之乱是削足适履，忽略历史复杂性",
        "background": "/home/ben/kunpengzhi/digest/小题大做/题3-产权分割与文明并购.md",
    },
}

OUTPUT_DIR = "/home/ben/kunpengzhi/digest/擂台"


class DebateArena:
    """4v4 辩论擂台 + 讲茶大堂"""

    def __init__(self, topic_id: str):
        if topic_id not in DEBATE_TOPICS:
            print(f"❌ 未知辩题: {topic_id}")
            print(f"可选: {', '.join(DEBATE_TOPICS.keys())}")
            for k, v in DEBATE_TOPICS.items():
                print(f"  {k}. {v['title']}")
            sys.exit(1)

        self.topic = DEBATE_TOPICS[topic_id]
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.transcript = []
        self.teahouse_comments = []

    # ─── 第一层：4v4 辩论 ────────────────────────

    async def run_debate(self):
        """运行 4v4 辩论"""
        print("=" * 70)
        print(f"🎬 鲲鹏志 · 大专辩论会")
        print(f"辩题：{self.topic['title']}")
        print("=" * 70)

        # 读取背景资料
        background = ""
        if os.path.exists(self.topic["background"]):
            with open(self.topic["background"]) as f:
                background = f.read()

        # 构建辩论 prompt
        debate_prompt = f"""
你是一个 4v4 辩论大赛的现场。辩题是：

## 辩题
{self.topic['title']}

## 正方立场
{self.topic['pro']}

## 反方立场
{self.topic['con']}

## 背景资料
{background[:3000]}

## 格式
这是一个完整的辩论赛记录。请模拟以下角色：

【正方一辩】开篇立论（3分钟）
【反方一辩】开篇立论（3分钟）
【正方二辩】驳论（2分钟）
【反方二辩】驳论（2分钟）
【正方三辩】自由辩论（攻防）
【反方三辩】自由辩论（攻防）
【正方四辩】总结陈词（2分钟）
【反方四辩】总结陈词（2分钟）

要求：
- 每个角色要有鲜明的个性和论证风格
- 正方要咄咄逼人、充满激情
- 反方要冷静拆解、犀利毒舌
- 自由辩论部分要有来回交锋
- 不许问"要不要继续"，直接输出完整辩论
"""

        # 通过 liteLLM 调用 Vertex AI
        import openai
        client = openai.AsyncOpenAI(
            base_url="http://localhost:4000/v1",
            api_key="sk-47318",
        )
        print("\n🎤 辩论开始...\n")
        response = await client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[{"role": "user", "content": debate_prompt}],
        )
        debate_text = response.choices[0].message.content

        if debate_text.strip():
            self.transcript.append(("辩论正赛", debate_text))
            print(debate_text[:500] + "...\n")
            print(f"✅ 辩论完成 ({len(debate_text)} 字符)")
        else:
            error_text = stderr.decode() if stderr else "无输出"
            print(f"❌ 辩论失败: {error_text[:200]}")

        return debate_text

    # ─── 第二层：讲茶大堂 ────────────────────────

    async def run_teahouse(self):
        """讲茶大堂：对辩论进行场外评论"""
        if not self.transcript:
            print("❌ 没有辩论内容，无法评论")
            return

        debate_text = self.transcript[0][1]
        print("\n" + "=" * 70)
        print("🍵 讲茶大堂 · 场外评论")
        print("=" * 70)

        teahouse_prompt = f"""
你是一个茶馆里的各路食客，正在观看刚才结束的一场辩论赛。

## 辩题
{self.topic['title']}

## 辩论实录（节选）
{debate_text[:4000]}

## 你的角色
请模拟以下四个角色，分别对这场辩论发表评论：

【茶博士】德高望重的老茶客，见多识广："呵呵，年轻人的辩论啊……依我看，正方最大的问题在于……反方虽然犀利，但忽略了……"

【店小二】消息灵通的跑堂："哎哟喂，您猜怎么着？我刚听说啊，正方那个论据是从……嗨，这事儿可有意思了！"

【神秘客】戴斗笠的独行客，压低声音说："你们都忽略了一个更关键的问题……"（抛出意想不到的视角）

【账房先生】拨着算盘珠子："我给你们算一笔账啊。正方用了三个核心论据，成功率……反方反驳了五次，但其中两次被正方化解了。按赔率算……"

要求：
- 每人至少说一段话
- 风格要鲜活，像真的在茶馆里聊天
- 可以互相对话、抬杠
- 不许问"要不要继续"
"""

        import openai
        client = openai.AsyncOpenAI(
            base_url="http://localhost:4000/v1",
            api_key="sk-47318",
        )
        print("\n🍵 讲茶大堂开张...\n")
        response = await client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[{"role": "user", "content": teahouse_prompt}],
        )
        teahouse_text = response.choices[0].message.content

        if teahouse_text.strip():
            self.teahouse_comments.append(("讲茶大堂", teahouse_text))
            print(teahouse_text[:500] + "...\n")
            print(f"✅ 讲茶大堂完成 ({len(teahouse_text)} 字符)")
        else:
            print(f"❌ 讲茶大堂失败")

        return teahouse_text

    # ─── 第三层：存档 ────────────────────────────

    def save(self):
        """保存完整的擂台记录"""
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # 生成完整报告
        report = []
        report.append(f"# 鲲鹏志 · 擂台\n")
        report.append(f"---\n")
        report.append(f"**辩题**: {self.topic['title']}\n")
        report.append(f"**日期**: {self.timestamp}\n")
        report.append(f"**正方**: {self.topic['pro']}\n")
        report.append(f"**反方**: {self.topic['con']}\n")
        report.append(f"---\n\n")

        # 辩论正赛
        for speaker, text in self.transcript:
            report.append(f"## 🎤 {speaker}\n\n")
            report.append(text)
            report.append("\n\n---\n\n")

        # 讲茶大堂
        if self.teahouse_comments:
            report.append(f"## 🍵 讲茶大堂\n\n")
            for speaker, text in self.teahouse_comments:
                report.append(text)
                report.append("\n\n---\n\n")

        # 赔率
        report.append("## 📊 赔率与统计\n\n")
        total_debate = sum(len(t) for _, t in self.transcript)
        total_teahouse = sum(len(t) for _, t in self.teahouse_comments)
        report.append(f"- 辩论正赛: {total_debate} 字符\n")
        report.append(f"- 讲茶大堂: {total_teahouse} 字符\n")
        report.append(f"- 总计: {total_debate + total_teahouse} 字符\n")
        report.append(f"- 模型: Google Vertex Gemini 2.5 Flash\n")

        content = "".join(report)
        filename = f"擂台-{self.topic['title'][:20]}-{self.timestamp}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)

        with open(filepath, "w") as f:
            f.write(content)

        print(f"\n💾 已保存: {filepath}")
        return filepath


async def main():
    print("=" * 70)
    print("🦅 鲲鹏志 · 擂台系统")
    print("源于 Flow（4v4 辩论），高于 Flow（讲茶大堂）")
    print("=" * 70)

    for k, v in DEBATE_TOPICS.items():
        print(f"\n  {k}. {v['title']}")

    topic_id = input("\n选择辩题 (1/2/3): ").strip() or "1"

    arena = DebateArena(topic_id)
    await arena.run_debate()
    await arena.run_teahouse()
    arena.save()

    print("\n" + "=" * 70)
    print("🎉 全部完成！")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
