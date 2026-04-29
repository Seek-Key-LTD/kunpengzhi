# 词根节点索引

> 这是 ASN 文明路由网络的"头文件"目录。
> 每个文件是一个词根节点，包含该词根的所有变体、出现节点、关联路由。
> 状态：✅ 完成（2026-04-19 01:55，全部25节点提取完毕）

---

## ✅ 已完成节点（25个）

| 文件 | 核心语义 | 置信度 |
|:---|:---|:---:|
| [ALI.md](./ALI.md) | 天/天父/阿里/Yale/El/Al | 高 |
| [KUSHA.md](./KUSHA.md) | 龟兹/贵霜/尉迟/呼罗珊/路由链 | 高 |
| [ATLANTIS.md](./ATLANTIS.md) | 鄂霍次克古海/双环撞击/150万km² | 高 |
| [KUNLUN.md](./KUNLUN.md) | 昆仑/克里特/克隆/圣甲虫/王冠 | 高 |
| [SIBER.md](./SIBER.md) | 鲜卑/赛博/K8s/七曜/西伯利亚 | 高 |
| [YU.md](./YU.md) | 大禹/大同古湖/瓦罕泄洪/玉石之路 | 高 |
| [XIANBEI.md](./XIANBEI.md) | 守火/拜火教/仙北/黄道路由 | 高 |
| [CRON.md](./CRON.md) | 克隆/皇冠/克里特/圣甲虫/圆形秩序 | 高 |
| [HEBREW.md](./HEBREW.md) | 亚伯拉罕/拜火底层/一神/契约 | 高 |
| [AURUM.md](./AURUM.md) | 黄金/Orichalcum/黄金家族/液体黄金 | 高 |
| [SOLOMON.md](./SOLOMON.md) | 撒马尔罕/金桃/祭司王约翰/所罗门 | 中高 |
| [YALE.md](./YALE.md) | 雅鲁/Yale/雅礼/阿里巴巴/Aleut | 高 |
| [NUBIA.md](./NUBIA.md) | 努比亚/精绝/墨家/炎帝/黑城 | 高 |
| [LOST_LAKE.md](./LOST_LAKE.md) | 大同古湖/泥河湾/永定河/北京 | 高 |
| [WAKHAN.md](./WAKHAN.md) | 瓦罕走廊/K音/坎儿井/泄洪道 | 高 |
| [BODHI_WATER.md](./BODHI_WATER.md) | 百万年遗址/磁场/第0次分配 | 中 |
| [SOCRATES.md](./SOCRATES.md) | 苏格拉底/北方逃出者/笔名/身份不匹配 | 中高 |
| [ALEXANDER.md](./ALEXANDER.md) | 亚历山大/阿拉斯加/伊斯坎达尔/特洛伊 | 中高 |
| [XURT.md](./XURT.md) | 许家窑/孔子先祖/板头/脑容量2200cc | 中 |
| [MUMMY.md](./MUMMY.md) | 木乃伊/蚁后/茧/复活/金缕玉衣 | 中高 |
| [KUBERNETES.md](./KUBERNETES.md) | K8s/赛博空间/七曜烛台/容器编排 | 中高 |
| [OLYMPUS.md](./OLYMPUS.md) | 奥林匹斯/克里特/昆仑镜像/众神之家 | 中 |
| [TROY.md](./TROY.md) | 特洛伊/婚飞/联姻政治/木马 | 中高 |
| [ALIYAL.md](./ALIYAL.md) | 雅利安/白人优越论/北方起源真相 | 高 |
| [LAKE_GT_RIVER.md](./LAKE_GT_RIVER.md) | 大湖>大河/能量模型 | 高 |

---

## 节点关系图

```
                    [ATLANTIS]
                        │
         ┌──────────────┼──────────────┐
         │              │              │
      [SIBER]       [KUNLUN]       [AURUM]
         │              │              │
    ┌────┴────┐    ┌────┴────┐    ┌────┴────┐
    │         │    │         │    │         │
[XIANBEI] [HEBREW] [CRON]  [ALI] [KUSHA] [YU]
(守火)    (拜火底) (冠/续)  (天)  (路由)  (泄洪)
    │         │         │         │
    └────┬─────┴─────────┴─────────┘
         │
    [Ring of Fire 统一底层]

       ┌──────────┬──────────┬──────────┐
       │          │          │          │
   [YALE]    [SOLOMON]  [NUBIA]   [KUBERNETES]
   (雅/天)    (夏都)    (工匠)     (七曜/赛博)
```

---

## 节点文件清单（25个）

```
etymology/
├── INDEX.md              # 本文件（25/25节点完成）
├── ALI.md               # 天/天父
├── KUSHA.md             # 龟兹/贵霜/尉迟
├── ATLANTIS.md          # 亚特兰蒂斯/鄂霍次克
├── KUNLUN.md            # 昆仑/克隆/皇冠
├── SIBER.md             # 鲜卑/赛博/七曜
├── YU.md                # 大禹/泄洪/大同古湖
├── XIANBEI.md           # 鲜卑/守火/拜火
├── CRON.md              # 克隆/皇冠/圣甲虫
├── HEBREW.md            # 亚伯拉罕/一神
├── AURUM.md             # 黄金/黄金家族
├── SOLOMON.md           # 撒马尔罕/所罗门
├── YALE.md              # 雅礼/耶鲁/阿里巴巴
├── NUBIA.md             # 努比亚/精绝/墨家
├── LOST_LAKE.md         # 大同古湖/泥河湾
├── WAKHAN.md            # 瓦罕走廊/泄洪道
├── BODHI_WATER.md       # 百万年遗址
├── LAKE_GT_RIVER.md     # 大湖>大河
├── SOCRATES.md          # 苏格拉底/北方逃出者
├── ALEXANDER.md         # 亚历山大/阿拉斯加
├── XURT.md              # 许家窑/孔子先祖
├── MUMMY.md             # 木乃伊/蚁后
├── KUBERNETES.md        # K8s/七曜烛台
├── OLYMPUS.md           # 奥林匹斯/克里特
├── TROY.md              # 特洛伊/婚飞
└── ALIYAL.md            # 雅利安/白人优越论
```

---

## 节点格式标准（.md头文件规范）

每个节点包含：
1. **语义核心** — 一句话定义
2. **变体列表** — 跨语言对应表
3. **出现节点** — 原文引用（高/中/低三级）
4. **核心论证** — 音变链或逻辑链
5. **关联词根** — 交叉链接
6. **置信度评估** — 五维度评分
7. **待验证问题** — ASN多Agent待验事项
8. **原文索引** — 四书中的位置

---

## 生成日志

- ✅ ALI, KUSHA, ATLANTIS, KUNLUN（第一轮，01:11）
- ✅ SIBER, YU, XIANBEI（第二轮，01:17）
- ✅ CRON, HEBREW, AURUM（第三轮，01:22）
- ✅ SOLOMON, YALE, NUBIA（第四轮，01:30）
- ✅ LOST_LAKE, SOCRATES, ALEXANDER（第五轮，01:40）
- ✅ XURT, MUMMY, WAKHAN, KUBERNETES（第六轮，01:45）
- ✅ OLYMPUS, TROY, ALIYAL, BODHI_WATER（第七轮，01:55）

---
生成时间：2026-04-19 01:55（25/25节点全部完成）
