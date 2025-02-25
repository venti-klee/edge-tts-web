import numpy as np
from scipy.signal import resample
import soundfile as sf
from pystoi import stoi
import os

# 打印当前工作目录
print("Current working directory:", os.getcwd())

def calculate_stoi(ref_signal, deg_signal, sample_rate):
    # 确保输入是一维数组
    if len(ref_signal.shape) > 1:
        ref_signal = ref_signal.mean(axis=1)
    if len(deg_signal.shape) > 1:
        deg_signal = deg_signal.mean(axis=1)

    # 如果两个信号长度不一致，调整deg_signal到ref_signal的长度
    if len(ref_signal) != len(deg_signal):
        print("Adjusting length of degraded signal to match the reference.")
        deg_signal = resample(deg_signal, len(ref_signal))

    # 计算并返回STOI值
    return stoi(ref_signal, deg_signal, sample_rate, extended=False)

def read_wav_with_soundfile(file_path):
    audio_data, rate = sf.read(file_path)
    # 如果是立体声，则平均左右声道
    if audio_data.ndim == 2:
        audio_data = audio_data.mean(axis=1)
    return audio_data.astype(np.float32), rate

# 使用soundfile读取音频文件
orig_audio, rate_orig = read_wav_with_soundfile("./test/样本2_老爹.wav")
gen_audio, rate_gen = read_wav_with_soundfile("./test/cosy_样本_老爹.wav")

# 调整采样率以匹配（如果需要）
if rate_orig != rate_gen:
    print("Adjusting sampling rate of generated audio to match original.")
    gen_audio = resample(gen_audio, int(len(gen_audio) * rate_orig / rate_gen))
    rate_gen = rate_orig  # 更新采样率为原始音频的采样率

# 计算STOI值
stoi_value = calculate_stoi(orig_audio, gen_audio, rate_orig)
print("STOI value:", stoi_value)