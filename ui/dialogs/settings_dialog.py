import json
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QTabWidget, QWidget,
                               QComboBox, QSpinBox)

class SettingsDialog(QDialog):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = json.loads(json.dumps(config))
        self.setWindowTitle("设置")
        self.resize(500, 400)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        tab_widget = QTabWidget()
        
        ai_page = QWidget()
        ai_layout = QVBoxLayout(ai_page)
        
        ai_layout.addWidget(QLabel("API Base URL："))
        self.base_url_input = QLineEdit(self.config["ai"]["base_url"])
        ai_layout.addWidget(self.base_url_input)
        
        ai_layout.addWidget(QLabel("API Key："))
        self.api_key_input = QLineEdit(self.config["ai"]["api_key"])
        self.api_key_input.setEchoMode(QLineEdit.Password)
        ai_layout.addWidget(self.api_key_input)
        
        ai_layout.addWidget(QLabel("模型名称："))
        self.model_input = QLineEdit(self.config["ai"]["model"])
        ai_layout.addWidget(self.model_input)
        
        ai_layout.addStretch()
        tab_widget.addTab(ai_page, "AI设置")
        
        display_page = QWidget()
        display_layout = QVBoxLayout(display_page)
        
        display_layout.addWidget(QLabel("默认字号："))
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 30)
        self.font_size_spin.setValue(self.config["display"]["font_size"])
        display_layout.addWidget(self.font_size_spin)
        
        display_layout.addWidget(QLabel("主题："))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["light", "dark"])
        self.theme_combo.setCurrentText(self.config["display"]["theme"])
        display_layout.addWidget(self.theme_combo)
        
        display_layout.addStretch()
        tab_widget.addTab(display_page, "显示设置")
        
        layout.addWidget(tab_widget)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("保存")
        save_btn.setDefault(True)
        save_btn.clicked.connect(self._save_and_accept)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)

    def _save_and_accept(self):
        self.config["ai"]["base_url"] = self.base_url_input.text().strip()
        self.config["ai"]["api_key"] = self.api_key_input.text().strip()
        self.config["ai"]["model"] = self.model_input.text().strip()
        self.config["display"]["font_size"] = self.font_size_spin.value()
        self.config["display"]["theme"] = self.theme_combo.currentText()
        self.accept()

    def get_config(self):
        return self.config
