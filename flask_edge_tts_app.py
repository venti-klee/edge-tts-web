import sys
from quart import Quart, request, jsonify, send_from_directory
from quart_cors import cors  # 导入cors
import edge_tts
from edge_tts import VoicesManager
from datetime import datetime
import asyncio
import os

# 如果是在 Windows 平台且 Python 版本为 3.8.x，则设置事件循环策略
if sys.platform == "win32" and (3, 8, 0) <= sys.version_info < (3, 9, 0):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = Quart(__name__)
# 启用CORS支持，并允许所有来源、所有方法和一些常用的头部
app = cors(app, allow_origin="*", allow_methods=["GET", "POST"], allow_headers=["Content-Type"])

# 定义保存音频文件的目录
AUDIO_DIR = 'static/audio'
os.makedirs(AUDIO_DIR, exist_ok=True)

# 将中文的语音类型描述转换为对应的语言代码
def get_language_code(voicetype):
    language_map = {
        "中文": "zh-CN",
        "英语": "en-US",
        "日语": "ja-JP",
        "韩语": "ko-KR",
        "法语": "fr-FR",
        "德语": "de-DE",
        "俄语": "ru-RU",
        "西班牙语": "es-ES",
        "葡萄牙语": "pt-BR",
        "意大利语": "it-IT",
        "荷兰语": "nl-NL",
        "希腊语": "el-GR",
        "瑞典语": "sv-SE",
        "波兰语": "pl-PL",
        "土耳其语": "tr-TR",
        "阿拉伯语": "ar-SA",
        "希伯来语": "he-IL",
        "印地语": "hi-IN",
        "泰米尔语": "ta-IN",
        "泰语": "th-TH",
        "越南语": "vi-VN",
        "芬兰语": "fi-FI",
        "丹麦语": "da-DK",
        "挪威语": "nb-NO",
        "匈牙利语": "hu-HU",
        "捷克语": "cs-CZ",
        "罗马尼亚语": "ro-RO",
        "保加利亚语": "bg-BG",
        "克罗地亚语": "hr-HR",
        "斯洛伐克语": "sk-SK",
        "斯洛文尼亚语": "sl-SI",
        "塞尔维亚语": "sr-RS",
        "乌克兰语": "uk-UA",
        "立陶宛语": "lt-LT",
        "拉脱维亚语": "lv-LV",
        "爱沙尼亚语": "et-EE",
        "马来语": "ms-MY",
        "印尼语": "id-ID",
        "菲律宾语": "fil-PH",
        "波斯语": "fa-IR",
        "乌尔都语": "ur-PK",
        "旁遮普语": "pa-IN",
        "孟加拉语": "bn-BD",
        "泰卢固语": "te-IN",
        "马拉地语": "mr-IN",
        "古吉拉特语": "gu-IN",
        "加泰罗尼亚语": "ca-ES",
        "爱尔兰语": "ga-IE",
        "威尔士语": "cy-GB",
        "巴斯克语": "eu-ES",
        "苏格兰盖尔语": "gd-GB",
        "阿尔巴尼亚语": "sq-AL",
        "马其顿语": "mk-MK",
        "冰岛语": "is-IS",
        "哈萨克语": "kk-KZ",
        "斯瓦希里语": "sw-KE",
        "索马里语": "so-SO",
        "阿姆哈拉语": "am-ET",
        "提格里尼亚语": "ti-ET",
        "依地语": "yi-001",
        "科西嘉语": "co-FR",
        "威尔士语": "cy-GB",
        "弗里斯兰语": "fy-NL",
        # ... 其他语言代码
    }
    return language_map.get(voicetype, None)

def get_gender_code(gender):
    gender_map = {
        "男": "Male",
        "女": "Female",
    }
    return gender_map.get(gender, None)

async def generate_audio_async(text, voicetype, gender, rate, volume, pitch):
    language_code = get_language_code(voicetype)
    gender_code = get_gender_code(gender)
    if not language_code or not gender_code:
        return None, "Unsupported voice type or gender"

    try:
        voices = await VoicesManager.create()
    except Exception as e:
        app.logger.error(f"Failed to fetch voices: {str(e)}")
        return None, f"Failed to fetch voices: {str(e)}"

    for voice in voices.voices:
        if voice['Gender'] == gender_code and voice['Locale'].startswith(language_code):
            current_time = datetime.now().strftime('%H%M%S')
            filename_base = text[:10].strip().replace(' ', '_')
            filename = f"{current_time}_{filename_base}.mp3"
            filepath = os.path.join(AUDIO_DIR, filename)

            communicate = edge_tts.Communicate(
                text,
                voice['ShortName'],
                rate=f'{"+" if rate >= 0 else ""}{rate}%',
                volume=f'{"+" if volume >= 0 else ""}{volume}%',
                pitch=f'{"+" if pitch >= 0 else ""}{pitch}Hz'
            )
            try:
                await communicate.save(filepath)
                return filename, None
            except Exception as e:
                app.logger.error(f"Failed to save audio: {str(e)}")
                return None, f"Failed to save audio: {str(e)}"
    return None, "Voice type or gender not supported"

@app.route('/')
async def index():
    return await send_from_directory('.', 'index.html')

@app.route('/favicon.ico')
async def favicon():
    return await send_from_directory('.', 'favicon.ico')

@app.route('/static/<path:filename>')
async def serve_static(filename):
    # 首先尝试从 'static' 目录下提供文件
    full_path = os.path.join('static', filename)
    if os.path.exists(full_path):
        return await send_from_directory('static', filename)
    # 如果文件不存在于 'static' 目录下，尝试从 AUDIO_DIR 提供文件
    return await send_from_directory(AUDIO_DIR, filename)

@app.route('/generate_audio', methods=['POST'])
async def generate_audio():
    form = await request.form
    text = form.get('text')
    voicetype = form.get('voicetype')
    gender = form.get('gender')
    rate = int(form.get('rate', 0))  # 默认值为0
    volume = int(form.get('volume', 0))  # 默认值为0
    pitch = int(form.get('pitch', 0))  # 默认值为0

    if not text or not voicetype or not gender:
        return jsonify({'error': 'Missing required parameters'}), 400

    try:
        filename, error = await generate_audio_async(text, voicetype, gender, rate, volume, pitch)
        if error:
            app.logger.error(f"Error generating audio: {error}")
            return jsonify({'error': error}), 500
        else:
            # 返回相对路径给前端
            return jsonify({'filename': f"/static/audio/{filename}"}), 200
    except Exception as e:
        app.logger.error(f"Unexpected error during audio generation: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred.'}), 500

if __name__ == '__main__':
    # 使用host='0.0.0.0'使得服务可以从外部访问，并指定端口
    app.run(host='0.0.0.0', port=50053)