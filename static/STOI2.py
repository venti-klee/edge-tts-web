import numpy as np
from scipy.io import wavfile
from scipy.signal import resample
from pystoi import stoi
import os


def calculate_stoi(ref_signal, deg_signal, sample_rate):
    """
    计算STOI值。

    :param ref_signal: 原始语音信号（一维数组）
    :param deg_signal: 合成或降质的语音信号（一维数组）
    :param sample_rate: 采样率
    :return: STOI值
    """
    # 确保输入是一维数组
    if len(ref_signal.shape) > 1:
        ref_signal = ref_signal.mean(axis=1)
    if len(deg_signal.shape) > 1:
        deg_signal = deg_signal.mean(axis=1)

    # 如果两个信号长度不一致，调整deg_signal到ref_signal的长度
    min_len = min(len(ref_signal), len(deg_signal))
    ref_signal = ref_signal[:min_len]
    deg_signal = deg_signal[:min_len]

    # 将信号转换为浮点数并进行峰值归一化
    ref_signal = ref_signal.astype(np.float32) / np.max(np.abs(ref_signal))
    deg_signal = deg_signal.astype(np.float32) / np.max(np.abs(deg_signal))

    # 检查信号的动态范围
    print(f"参考信号的动态范围: {np.max(ref_signal) - np.min(ref_signal)}")
    print(f"降级信号的动态范围: {np.max(deg_signal) - np.min(deg_signal)}")

    # 计算并返回STOI值
    return stoi(ref_signal, deg_signal, sample_rate, extended=False)


# 打印当前工作目录
print("当前工作目录:", os.getcwd())

# 读取原始和合成的语音文件
rate_orig, orig_audio = wavfile.read("./test/样本1zero.wav")
rate_gen, gen_audio = wavfile.read("./test/1官网.wav")

# 检查音频文件的基本信息
print(f"原始音频形状: {orig_audio.shape}, 采样率: {rate_orig}")
print(f"生成音频形状: {gen_audio.shape}, 采样率: {rate_gen}")

# 调整采样率以匹配（如果需要）
if rate_orig != rate_gen:
    print("正在调整生成音频的采样率以匹配原始音频。")
    gen_audio = resample(gen_audio, int(len(gen_audio) * (rate_orig / rate_gen)))
    rate_gen = rate_orig  # 更新采样率为原始音频的采样率

# 计算并返回STOI值
stoi_value = calculate_stoi(orig_audio, gen_audio, rate_orig)
if stoi_value is not None:
    print("STOI值:", stoi_value)

    # 检查清晰度得分是否达到要求
    if stoi_value >= 0.8:
        print("清晰度得分满足要求 (>= 0.8)。")
    else:
        print("清晰度得分未达到要求 (< 0.8)。")
else:
    print("无法计算STOI值。")