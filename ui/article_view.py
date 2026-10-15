from PySide6.QtWidgets import QTextEdit, QMenu
from PySide6.QtGui import QAction, QFont, QTextCursor
from PySide6.QtCore import Signal, Qt

class ArticleView(QTextEdit):
    word_added = Signal(str, str)
    translate_requested = Signal(str)
    sentence_double_clicked = Signal(str)
    font_size_changed = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setLineWrapMode(QTextEdit.WidgetWidth)
        self.base_font_size = 14
        self.update_font()
        self.setMouseTracking(True)

    def mouseDoubleClickEvent(self, event):
        # 双击选中整句，自动触发单句翻译
        cursor = self.textCursor()
        cursor.select(QTextCursor.SelectionType.LineUnderCursor)
        sentence = cursor.selectedText().strip()
        if sentence:
            self.sentence_double_clicked.emit(sentence)
        super().mouseDoubleClickEvent(event)

    def update_font(self):
        font = self.font()
        font.setPointSize(self.base_font_size)
        self.setFont(font)
        self.font_size_changed.emit(self.base_font_size)

    def wheelEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self.base_font_size = min(self.base_font_size + 1, 30)
            else:
                self.base_font_size = max(self.base_font_size - 1, 8)
            self.update_font()
            event.accept()
        else:
            super().wheelEvent(event)

    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu()
        
        selected_text = self.textCursor().selectedText().strip()
        
        if selected_text:
            menu.addSeparator()
            
            add_vocab_action = QAction("加入生词本", self)
            add_vocab_action.triggered.connect(lambda: self.word_added.emit(selected_text, selected_text))
            menu.addAction(add_vocab_action)
            
            add_comment_action = QAction("加入生词本并添加文内注释", self)
            add_comment_action.triggered.connect(self._add_word_with_comment)
            menu.addAction(add_comment_action)
            
            menu.addSeparator()
            
            translate_action = QAction("翻译选中内容", self)
            translate_action.triggered.connect(lambda: self.translate_requested.emit(selected_text))
            menu.addAction(translate_action)
        
        menu.exec(event.globalPos())

    def _add_word_with_comment(self):
        selected_text = self.textCursor().selectedText().strip()
        self.word_added.emit(selected_text, selected_text)

    def set_font_size(self, size):
        self.base_font_size = size
        self.update_font()

    def get_scroll_position(self):
        return self.verticalScrollBar().value()

    def set_scroll_position(self, pos):
        self.verticalScrollBar().setValue(pos)
