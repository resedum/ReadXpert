from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QComboBox, QSpinBox, QLineEdit, QPushButton)
from PySide6.QtCore import Qt

class GenerateArticleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("AI生成阅读文章")
        self.resize(500, 400)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        layout.addWidget(QLabel("考试类型："))
        self.exam_combo = QComboBox()
        self.exam_combo.addItems([
            "大学英语四级", "大学英语六级", "考研英语一", 
            "雅思阅读", "托福阅读", "通用语言"
        ])
        layout.addWidget(self.exam_combo)
        
        layout.addWidget(QLabel("文章主题："))
        self.theme_input = QLineEdit()
        self.theme_input.setPlaceholderText("例如：人工智能、环境保护、教育发展")
        layout.addWidget(self.theme_input)
        
        layout.addWidget(QLabel("目标字数："))
        self.word_count_spin = QSpinBox()
        self.word_count_spin.setRange(100, 2000)
        self.word_count_spin.setValue(350)
        layout.addWidget(self.word_count_spin)
        
        layout.addWidget(QLabel("指定包含词汇（英文逗号分隔，可选）："))
        self.words_edit = QLineEdit()
        self.words_edit.setPlaceholderText("例如：technology, environment, education")
        layout.addWidget(self.words_edit)
        
        layout.addStretch()
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        generate_btn = QPushButton("生成文章")
        generate_btn.setDefault(True)
        generate_btn.clicked.connect(self.accept)
        btn_layout.addWidget(generate_btn)
        
        layout.addLayout(btn_layout)

    def get_parameters(self):
        words_text = self.words_edit.text().strip()
        target_words = []
        if words_text:
            target_words = [w.strip() for w in words_text.split(',') if w.strip()]
            
        return {
            "exam_type": self.exam_combo.currentText(),
            "theme": self.theme_input.text().strip() or "通用话题",
            "word_count": self.word_count_spin.value(),
            "target_words": target_words
        }
