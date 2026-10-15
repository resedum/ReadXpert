# ReadXpert - Multi-language Reading Companion
# ReadXpert - 多语言阅读训练工具

A cross-platform desktop reading assistant for language learners, fully usable offline, designed to support 8 languages and expandable with custom dictionary files.
一款面向语言学习者的跨平台桌面阅读辅助工具，支持离线使用，原生兼容8种语言，可通过自定义词典扩展更多语种。

---

## ✨ Core Features / 核心功能
- 📖 **Immersive Reading**: Left-side article view, Ctrl+scroll font zoom, distraction-free reading mode
  沉浸式阅读：左侧文章区，Ctrl+滚轮缩放字号，专注模式不被打断
- 📝 **Smart Vocabulary Book**: Select text → right-click to save as new word, auto-match local dictionary, double-click for full details (phonetics, exam tags, part-of-speech definitions)
  智能生词本：框选单词右键一键收录，自动匹配本地词典，双击查看完整信息（音标、考试标签、分词性释义）
- 🌍 **Offline Translation**: Built-in ECDICT 760k-entry English-Chinese dictionary, supports 8 target languages (Chinese/English/Japanese/Korean/French/German/Russian/Spanish)
  离线翻译：内置ECDICT 76万条英汉词典，支持8种目标语言互译（中/英/日/韩/法/德/俄/西）
- 🤖 **AI Enhancement**: Configure OpenAI-compatible API to generate exam-level reading passages (CET4/CET6/Graduate Entrance/IELTS/TOEFL) and fluent sentence/paragraph translation
  AI增强：配置OpenAI兼容API后，可生成考试难度阅读文章、流畅整句整段翻译
- 📂 **Project History**: Imported articles are auto-saved as projects, reopen anytime from "My Projects" menu
  项目历史：导入文章自动存为项目，从「我的项目」随时打开继续阅读
- 📤 **Import/Export**: Import txt/md/docx/pdf articles, export vocabulary list as csv/xlsx, import custom word lists
  导入导出：支持导入多种格式文章，生词本导出为csv/xlsx，支持导入自定义词库

---

## 🚀 Quick Start / 快速开始
### Requirements / 环境要求
- Windows 10/11
- Python 3.9+

### Run / 安装运行
```bash
# Install dependencies / 安装依赖
pip install -r requirements.txt
# Start app / 启动程序
python main.py
```

### Built-in Dictionaries / 内置词库
- English-Chinese: ECDICT 760k entries, with phonetics, exam tags (CET4/CET6/Graduate/IELTS/TOEFL), word frequency
  英中方向：ECDICT全量76万词条，带音标、考试标签、词频
- Core high-frequency dictionaries for Japanese/Korean/French/German/Russian, covering 1000+ most common words for basic offline translation
  日/韩/法/德/俄核心高频词典，覆盖1000+最常用词，支持基础离线互译

### Add Custom Dictionaries / 扩展自定义词典
Drop CSV dictionary files into `core/` directory, the app will auto-load on startup:
将CSV格式词典放入`core/`目录，程序启动时自动加载：
```csv
word,target_word
hello,こんにちは
```

---

## 🌐 Multi-language Support / 多语言支持
Out of the box, the app supports translation between 8 languages. You can expand to any language pair by adding custom dictionary files.
程序原生支持8种语言互译，你可以通过添加自定义词典扩展任意语言对。
| Source Language | Target Languages |
|-----------------|------------------|
| English | Chinese / Japanese / Korean / French / German / Russian / Spanish |
| Chinese | English / Japanese / Korean / French / German / Russian |
| Japanese | English / Chinese |
| Korean | English / Chinese |
| French | English / Chinese |
| German | English / Chinese |
| Russian | English / Chinese |

---

## 📄 License / 开源协议
For educational use only. Built-in ECDICT dictionary follows its original open-source license.
本项目仅用于学习用途，内置ECDICT词典遵循其原始开源协议。
