# Edge TTS Web

> 微软 Edge TTS 的 Web 前端，支持 50+ 语言在线语音合成

## 项目简介

Edge TTS Web 是基于 [edge-tts](https://github.com/rany2/edge-tts) Python 库的 Web 封装，提供浏览器端的文字转语音界面。用户无需命令行操作，直接在网页上输入文本即可生成语音，支持在线播放和 MP3 下载。

## 功能特性

- **浏览器端 TTS** — 网页界面直接文字转语音
- **50+ 语言** — 中文、英文、日文、韩文、法文、德文等
- **参数调节** — 语速、音量、音调滑块调节
- **性别选择** — 男声 / 女声切换
- **在线播放** — 生成后直接在浏览器播放
- **MP3 下载** — 一键下载生成的音频文件
- **RESTful API** — `/generate_audio` 接口，可集成到其他系统

## 技术栈

| 类别 | 技术 |
|------|------|
| 后端框架 | Quart（异步 Flask） |
| TTS 引擎 | edge-tts v7.0.0 |
| 前端 | 原生 HTML / JavaScript |
| 跨域 | quart-cors |

## 快速开始

```bash
# 安装依赖
pip install edge-tts quart quart-cors

# 启动服务
python flask_edge_tts_app.py

# 访问 http://localhost:50053
```

## API 接口

### POST /generate_audio

生成语音音频文件。

| 参数 | 类型 | 说明 |
|------|------|------|
| `text` | string | 要转换的文本 |
| `language` | string | 语言代码 |
| `gender` | string | Male / Female |
| `rate` | string | 语速（如 +50%、-20%） |
| `volume` | string | 音量 |
| `pitch` | string | 音调 |

## 与原版 edge-tts 的区别

| | edge-tts（原版） | Edge TTS Web（本项目） |
|---|---|---|
| 使用方式 | 命令行 / Python API | 浏览器网页 |
| 部署方式 | pip install | Web 服务器 |
| 适用场景 | 开发者集成 | 终端用户直接使用 |

## License

LGPL-3.0
