#!/root/venvs/cosyvoice-v1/bin/python
import sys, os, json, hashlib, time
sys.path.insert(0, '/mnt/workspace/CosyVoice')
os.environ['MODELSCOPE_CACHE'] = '/mnt/workspace/.cache/modelscope'
import torch
torch.use_deterministic_algorithms(True)
from cosyvoice.cli.cosyvoice import AutoModel
from cosyvoice.utils.common import set_all_random_seed
import numpy as np
from pydub import AudioSegment

cosyvoice = AutoModel(model_dir='/mnt/workspace/.cache/modelscope/hub/iic/CosyVoice-300M-SFT')

ROLE_MAP = [
    ('正方一辩', '中文女', 3044),
    ('反方一辩', '中文男', 2705),
    ('正方二辩', '英文女', 1265),
    ('反方二辩', '英文男', 4287),
    ('正方三辩', '日语男', 5592),
    ('反方三辩', '粤语女', 6710),
    ('正方四辩', '韩语女', 7893),
    ('反方四辩', '中文女', 9527),
]

short_texts = {
    '正方一辩': '白貂皮大衣是大同流亡军团理论的铁证。',
    '反方一辩': '用一件衣服论证历史，这是过度诠释。',
    '正方二辩': '纹饰的同源性说明这不是普通的转手贸易。',
    '反方二辩': '丝绸之路上的文化交融，不需要军团背书。',
    '正方三辩': '请问对方辩友如何解释墓葬中的工艺一致性？',
    '反方三辩': '你们先假设结论，再用结论论证证据。',
    '正方四辩': '我方从物证文献工艺三个维度构建了证据链。',
    '反方四辩': '最危险的是用一个宏大理论统摄所有碎片。',
}

print('角色       音色   seed  时长  MD5')
print('-' * 65)

hashes = {}
t0 = time.time()
for role_name, spk, seed in ROLE_MAP:
    text = short_texts[role_name]
    set_all_random_seed(seed)
    for result in cosyvoice.inference_sft(text, spk, stream=False):
        dur = result['tts_speech'].shape[1] / cosyvoice.sample_rate
        audio = result['tts_speech'].cpu().numpy()[0]
        seg = AudioSegment(
            (audio * 32767).clip(-32768, 32767).astype(np.int16).tobytes(),
            frame_rate=int(cosyvoice.sample_rate), sample_width=2, channels=1
        )
        path = '/mnt/workspace/tmp/debate_' + role_name + '.mp3'
        seg.export(path, format='mp3', bitrate='128k')
        md5 = hashlib.md5(open(path, 'rb').read()).hexdigest()
        hashes[role_name] = md5
        print(role_name + ' ' + spk + ' seed=' + str(seed) + ' ' + format(dur, '.1f') + 's ' + md5[:16])

total = time.time() - t0
print()
print('总耗时: ' + format(total, '.1f') + 's')

# 验证确定性：再跑一次正方一辩
set_all_random_seed(3044)
for result in cosyvoice.inference_sft(short_texts['正方一辩'], '中文女', stream=False):
    audio = result['tts_speech'].cpu().numpy()[0]
    seg = AudioSegment(
        (audio * 32767).clip(-32768, 32767).astype(np.int16).tobytes(),
        frame_rate=int(cosyvoice.sample_rate), sample_width=2, channels=1
    )
    seg.export('/mnt/workspace/tmp/debate_正方一辩_v2.mp3', format='mp3', bitrate='128k')
    md5_2 = hashlib.md5(open('/mnt/workspace/tmp/debate_正方一辩_v2.mp3', 'rb').read()).hexdigest()

if hashes['正方一辩'] == md5_2:
    print('种子确定性验证: 两次生成 MD5 完全一致!')
else:
    print('不一致: ' + hashes['正方一辩'] + ' vs ' + md5_2)
