from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QComboBox
from PySide6.QtCore import Signal

class TranslationPanel(QWidget):
    lang_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        
        title_layout = QVBoxLayout()
        title_label = QLabel("翻译结果")
        title_label.setStyleSheet("font-weight:bold; font-size:12pt;")
        title_layout.addWidget(title_label)
        
        lang_layout = QVBoxLayout()
        lang_label = QLabel("目标语言：")
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["中文", "英文", "日文", "韩文", "法文", "德文", "俄文", "西班牙文"])
        self.lang_combo.setCurrentText("中文")
        self.lang_combo.currentTextChanged.connect(self._on_lang_changed)
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.lang_combo)
        
        title_layout.addLayout(lang_layout)
        layout.addLayout(title_layout)
        
        self.result_edit = QTextEdit()
        self.result_edit.setReadOnly(True)
        self.result_edit.setPlaceholderText("选中文本后右键选择「翻译选中内容」，结果将显示在这里")
        layout.addWidget(self.result_edit)

    def set_translation(self, text):
        self.result_edit.setPlainText(text)

    def clear(self):
        self.result_edit.clear()

    def _on_lang_changed(self, lang):
        lang_map = {
            "中文": "zh-CN",
            "英文": "en",
            "日文": "ja",
            "韩文": "ko",
            "法文": "fr",
            "德文": "de",
            "俄文": "ru",
            "西班牙文": "es"
        }
        self.lang_changed.emit(lang_map.get(lang, "zh-CN"))

    def get_target_lang(self):
        lang_map = {
            "中文": "zh-CN",
            "英文": "en",
            "日文": "ja",
            "韩文": "ko",
            "法文": "fr",
            "德文": "de",
            "俄文": "ru",
            "西班牙文": "es"
        }
        return lang_map.get(self.lang_combo.currentText(), "zh-CN")
