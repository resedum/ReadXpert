from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
                               QListWidget, QListWidgetItem, QLabel, QMenu,
                               QPushButton, QLineEdit)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QAction

class VocabularyPanel(QWidget):
    word_hovered = Signal(str)
    word_selected = Signal(str)
    word_double_clicked = Signal(dict)
    export_requested = Signal()
    import_requested = Signal()
    delete_word_requested = Signal(str)
    set_mastery_requested = Signal(str, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_article = ""
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        
        title_layout = QHBoxLayout()
        title_label = QLabel("生词本")
        title_label.setStyleSheet("font-weight:bold; font-size:12pt;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索单词...")
        self.search_input.setMaximumWidth(150)
        self.search_input.textChanged.connect(self._filter_words)
        title_layout.addWidget(self.search_input)
        
        layout.addLayout(title_layout)
        
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self._create_word_list(), "当前文章")
        self.tab_widget.addTab(self._create_word_list(), "全部词库")
        layout.addWidget(self.tab_widget)
        
        btn_layout = QHBoxLayout()
        import_btn = QPushButton("导入词库")
        import_btn.clicked.connect(self.import_requested.emit)
        export_btn = QPushButton("导出生词")
        export_btn.clicked.connect(self.export_requested.emit)
        btn_layout.addWidget(import_btn)
        btn_layout.addWidget(export_btn)
        layout.addLayout(btn_layout)

    def _create_word_list(self):
        list_widget = QListWidget()
        list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        list_widget.customContextMenuRequested.connect(self._show_context_menu)
        list_widget.itemEntered.connect(self._on_item_hover)
        list_widget.itemClicked.connect(self._on_item_clicked)
        list_widget.itemDoubleClicked.connect(self._on_item_double_clicked)
        list_widget.setMouseTracking(True)
        return list_widget
    
    def _on_item_double_clicked(self, item):
        if item:
            word_info = item.data(Qt.UserRole)
            self.word_double_clicked.emit(word_info)

    def update_article_words(self, words):
        list_widget = self.tab_widget.widget(0)
        list_widget.clear()
        for word_info in words:
            item = QListWidgetItem(f"{word_info['base_form']}  -  {word_info['definition'][:20]}...")
            item.setData(Qt.UserRole, word_info)
            list_widget.addItem(item)

    def update_all_words(self, words):
        list_widget = self.tab_widget.widget(1)
        list_widget.clear()
        for word_info in words:
            mastery = ["", "☆", "★"][word_info["mastery_level"]]
            item = QListWidgetItem(f"{mastery} {word_info['base_form']}  -  {word_info['definition'][:15]}...")
            item.setData(Qt.UserRole, word_info)
            list_widget.addItem(item)

    def _filter_words(self, text):
        current_list = self.tab_widget.currentWidget()
        for i in range(current_list.count()):
            item = current_list.item(i)
            word_info = item.data(Qt.UserRole)
            item.setHidden(text.lower() not in word_info["base_form"].lower())

    def _show_context_menu(self, pos):
        list_widget = self.tab_widget.currentWidget()
        item = list_widget.itemAt(pos)
        if not item:
            return
            
        word_info = item.data(Qt.UserRole)
        menu = QMenu(self)
        
        master_action = QAction("标记为已掌握", self)
        master_action.triggered.connect(lambda: self._set_mastery(word_info["base_form"], 2))
        menu.addAction(master_action)
        
        familiar_action = QAction("标记为熟悉", self)
        familiar_action.triggered.connect(lambda: self._set_mastery(word_info["base_form"], 1))
        menu.addAction(familiar_action)
        
        menu.addSeparator()
        
        delete_action = QAction("删除单词", self)
        delete_action.triggered.connect(lambda: self._delete_word(word_info["base_form"]))
        menu.addAction(delete_action)
        
        menu.exec(list_widget.mapToGlobal(pos))

    def _on_item_hover(self, item):
        if item:
            word_info = item.data(Qt.UserRole)
            self.word_hovered.emit(word_info["base_form"])

    def _on_item_clicked(self, item):
        if item:
            word_info = item.data(Qt.UserRole)
            self.word_selected.emit(word_info["base_form"])

    def _set_mastery(self, word, level):
        self.set_mastery_requested.emit(word, level)
        # 刷新显示
        self.update_all_words(self.parent().vocab_manager.get_all_words())

    def _delete_word(self, word):
        self.delete_word_requested.emit(word)
        # 刷新显示
        self.update_all_words(self.parent().vocab_manager.get_all_words())
        self.update_article_words(self.parent().vocab_manager.get_article_words(self.current_article))

    def set_current_article(self, article_id):
        self.current_article = article_id
