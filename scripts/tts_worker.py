#!/usr/bin/env python3
"""CosyVoice TTS worker — 三版本统一入口"""
import sys, os

DIR = '/mnt/workspace/CosyVoice'
sys.path.insert(0, DIR)
sys.path.insert(0, f'{DIR}/third_party/Matcha-TTS')
os.environ['MODELSCOPE_CACHE'] = '/mnt/workspace/.cache/modelscope'

from cosyvoice.cli.cosyvoice import AutoModel
from cosyvoice.utils.common import set_all_random_seed
import numpy as np
from pydub import AudioSegment
import argparse

def main():
    parser = argparse.ArgumentParser(description='CosyVoice TTS → MP3')
    parser.add_argument('version', choices=['v1', 'v2', 'v3'])
    parser.add_argument('text', help='要合成的文本')
    parser.add_argument('output', help='输出 MP3 路径')
    parser.add_argument('--seed', type=int, default=42, help='随机种子')
    parser.add_argument('--prompt', default='希望你以后能够做的比我还好呦。', help='零样本提示文本')
    parser.add_argument('--ref', default='/mnt/workspace/tmp/ref_prompt.wav', help='参考音频')
    parser.add_argument('--speaker', default='中文女', help='v1 音色')
    args = parser.parse_args()

    set_all_random_seed(args.seed)

    if args.version == 'v1':
        model_dir = '/mnt/workspace/.cache/modelscope/hub/iic/CosyVoice-300M-SFT'
        cosyvoice = AutoModel(model_dir=model_dir)
        result_iter = cosyvoice.inference_sft(args.text, args.speaker, stream=False)

    elif args.version == 'v2':
        model_dir = '/mnt/workspace/.cache/modelscope/hub/iic/CosyVoice2-0.5B'
        cosyvoice = AutoModel(model_dir=model_dir)
        result_iter = cosyvoice.inference_zero_shot(
            args.text, args.prompt, args.ref, stream=False)

    else:  # v3
        model_dir = '/mnt/workspace/.cache/modelscope/hub/FunAudioLLM/Fun-CosyVoice3-0.5B'
        cosyvoice = AutoModel(model_dir=model_dir)
        v3_prompt = f'You are a helpful assistant.<|endofprompt|>{args.prompt}'
        result_iter = cosyvoice.inference_zero_shot(
            args.text, v3_prompt, args.ref, stream=False)

    for result in result_iter:
        speech = result['tts_speech']
        sr = cosyvoice.sample_rate
        audio = speech.cpu().numpy()
        if len(audio.shape) > 1:
            audio = audio[0]
        seg = AudioSegment(
            (audio * 32767).clip(-32768, 32767).astype(np.int16).tobytes(),
            frame_rate=sr, sample_width=2, channels=1
        )
        seg.export(args.output, format='mp3', bitrate='128k')
        size = os.path.getsize(args.output)
        dur = speech.shape[1] / sr
        print(f'✅ CosyVoice {args.version.upper()} MP3: {args.output}')
        print(f'   时长: {dur:.1f}s | 大小: {size/1024:.0f}KB | seed: {args.seed}')

if __name__ == '__main__':
    main()
