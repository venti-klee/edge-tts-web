import numpy as np
from scipy.io import wavfile
from pystoi import stoi
import os

from scipy.signal import resample

# 打印当前工作目录
print("Current working directory:", os.getcwd())


def calculate_stoi(ref_signal, deg_signal, sample_rate):
    """
    计算STOI值。

    :param ref_signal: 原始语音信号（一维数组）
    :param deg_signal: 生成或降质的语音信号（一维数组）
    :param sample_rate: 采样率
    :return: STOI值
    """
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


# 读取原始和生成的语音文件
rate_orig, orig_audio = wavfile.read("./test/样本2_老爹.wav")
rate_gen, gen_audio = wavfile.read("./test/cosy_样本_老爹.wav")

# 调整采样率以匹配（如果需要）
if rate_orig != rate_gen:
    print("Adjusting sampling rate of generated audio to match original.")
    gen_audio = resample(gen_audio, int(len(gen_audio) * (rate_orig / rate_gen)))

# 计算STOI值
stoi_value = calculate_stoi(orig_audio, gen_audio, rate_orig)
print("STOI value:", stoi_value)