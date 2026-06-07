#!/bin/bash
# 🎤 CosyVoice TTS → MP3 快捷工具
# 用法:
#   tts.sh v1 文字 [输出] [seed]          # 预设音色
#   tts.sh v2 文字 [输出] [seed] [提示]    # 零样本克隆
#   tts.sh v3 文字 [输出] [seed] [提示]    # 零样本+克隆
# 规则：所有交付必须 MP3

VER="${1:-v1}"
TEXT="${2:-鲲鹏之志，扶摇直上九万里。}"
OUT="${3:-/mnt/workspace/tmp/tts_$(date +%s).mp3}"
SEED="${4:-42}"
PROMPT="${5:-希望你以后能够做的比我还好呦。}"

mkdir -p /mnt/workspace/tmp
/root/venvs/cosyvoice-$VER/bin/python /mnt/workspace/scripts/tts_worker.py \
    "$VER" "$TEXT" "$OUT" \
    --seed "$SEED" \
    --prompt "$PROMPT"
