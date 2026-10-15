import json
import os
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                               QSplitter, QMenuBar, QFileDialog, QMessageBox,
                               QStatusBar, QInputDialog)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

from core.article_manager import ArticleManager
from core.vocabulary_manager import VocabularyManager
from core.ai_engine import AIEngine
from core.text_processor import TextProcessor
from core.local_dictionary import LocalDictionary
from core.multilang_dict import MultiLangDict

from .article_view import ArticleView
from .vocabulary_panel import VocabularyPanel
from .translation_panel import TranslationPanel
from .dialogs.generate_article_dialog import GenerateArticleDialog
from .dialogs.settings_dialog import SettingsDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ReadXpert - AI阅读训练工具")
        self.resize(1200, 800)
        
        self.config = self._load_config()
        self.article_manager = ArticleManager()
        self.vocab_manager = VocabularyManager()
        self.ai_engine = AIEngine(self.config)
        self.text_processor = TextProcessor()
        self.local_dict = LocalDictionary()
        self.multilang_dict = MultiLangDict()
        
        self.current_article_id = ""
        self.current_article_content = ""
        
        self._init_ui()
        self._init_menu()
        self._refresh_vocabulary()

    def _load_config(self):
        config_path = "config/config.json"
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_config(self):
        with open("config/config.json", 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.main_splitter = QSplitter(Qt.Horizontal)
        
        self.article_view = ArticleView()
        self.article_view.word_added.connect(self._on_add_word)
        self.article_view.translate_requested.connect(self._on_translate)
        self.article_view.sentence_double_clicked.connect(self._on_double_click_sentence)
        self.article_view.font_size_changed.connect(self._on_font_size_changed)
        self.main_splitter.addWidget(self.article_view)
        
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        self.right_splitter = QSplitter(Qt.Vertical)
        
        self.vocab_panel = VocabularyPanel()
        self.vocab_panel.word_hovered.connect(self._on_word_hovered)
        self.vocab_panel.word_double_clicked.connect(self._on_word_double_clicked)
        self.vocab_panel.export_requested.connect(self._on_export_vocab)
        self.vocab_panel.import_requested.connect(self._on_import_vocab)
        self.vocab_panel.delete_word_requested.connect(self._on_delete_word)
        self.vocab_panel.set_mastery_requested.connect(self._on_set_mastery)
        self.right_splitter.addWidget(self.vocab_panel)
        
        self.translation_panel = TranslationPanel()
        self.translation_panel.lang_changed.connect(self._on_target_lang_changed)
        self.right_splitter.addWidget(self.translation_panel)
        
        self.right_splitter.setSizes([350, 350])
        
        right_layout.addWidget(self.right_splitter)
        self.main_splitter.addWidget(right_widget)
        
        self.main_splitter.setSizes([750, 450])
        main_layout.addWidget(self.main_splitter)
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")

    def _init_menu(self):
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("文件")
        
        import_act = QAction("导入文章...", self)
        import_act.triggered.connect(self._import_article)
        file_menu.addAction(import_act)
        
        import_vocab_act = QAction("导入词库...", self)
        import_vocab_act.triggered.connect(self._on_import_vocab)
        file_menu.addAction(import_vocab_act)
        
        file_menu.addSeparator()
        
        exit_act = QAction("退出", self)
        exit_act.triggered.connect(self.close)
        file_menu.addAction(exit_act)
        
        ai_menu = menubar.addMenu("AI工具")
        
        generate_act = QAction("生成阅读文章...", self)
        generate_act.triggered.connect(self._show_generate_dialog)
        ai_menu.addAction(generate_act)
        
        ai_menu.addSeparator()
        
        settings_act = QAction("AI设置...", self)
        settings_act.triggered.connect(self._show_settings)
        ai_menu.addAction(settings_act)
        
        view_menu = menubar.addMenu("视图")
        
        focus_act = QAction("专注模式", self)
        focus_act.setCheckable(True)
        focus_act.triggered.connect(self._toggle_focus_mode)
        view_menu.addAction(focus_act)
        
        # 我的项目菜单
        self.history_menu = menubar.addMenu("我的项目")
        
        translate_all_act = QAction("一键翻译整篇文章", self)
        translate_all_act.triggered.connect(self._translate_whole_article)
        self.history_menu.addAction(translate_all_act)
        
        self.history_menu.addSeparator()
        self._refresh_history()

    def _refresh_history(self):
        """刷新历史菜单列表"""
        # 清空旧的历史项
        for action in self.history_menu.actions()[2:]:
            self.history_menu.removeAction(action)
        
        articles = self.article_manager.get_article_list()
        if not articles:
            no_act = QAction("（暂无项目，导入或生成文章后自动保存）", self)
            no_act.setEnabled(False)
            self.history_menu.addAction(no_act)
            return
        
        # 按最近阅读排序
        articles.sort(key=lambda x: self.article_manager.progress.get(x, {}).get("last_read", ""), reverse=True)
        
        for article_id in articles:
            action = QAction(article_id, self)
            action.triggered.connect(lambda checked, aid=article_id: self._load_history_article(aid))
            self.history_menu.addAction(action)

    def _load_history_article(self, article_id):
        content = self.article_manager.get_article_content(article_id)
        if content:
            self._load_article(article_id, content)
            self.status_bar.showMessage(f"已打开历史文章：{article_id}")

    def _on_double_click_sentence(self, sentence):
        """双击单句自动翻译"""
        self._on_translate(sentence)

    def _on_word_double_clicked(self, word_info):
        """双击生词本词条，弹出完整详情窗口"""
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QDialogButtonBox
        import re
        
        word = word_info['base_form']
        # 查本地完整词典
        dict_info = self.local_dict.lookup(word)
        
        mastery_text = ["未掌握", "熟悉", "已掌握"][word_info["mastery_level"]]
        tag_text = ""
        phonetic = ""
        full_translation = word_info['definition']
        
        if dict_info:
            phonetic = dict_info["phonetic"]
            tags = dict_info["tag"].split()
            tag_map = {"zk": "考研", "cet4": "四级", "cet6": "六级", "ielts": "雅思", "toefl": "托福", "gk": "高考"}
            tag_text = "  ".join([f"[{tag_map.get(t, t)}]" for t in tags if t])
            # 如果生词本里的释义是简版，用词典里的完整释义替换
            if len(dict_info["translation"]) > len(full_translation):
                full_translation = dict_info["translation"]
        
        # 把释义按换行拆分，每个词性单独一行
        meaning_lines = [line.strip() for line in full_translation.split('\n') if line.strip()]
        meaning_html = ""
        for i, line in enumerate(meaning_lines, 1):
            meaning_html += f'<div style="margin:3px 0; padding-left:8px;">{i}. {line}</div>'
        
        # 构造详情文本
        detail_html = f"""
        <h2 style="margin-bottom:5px;">{word} <span style="color:#666; font-size:14px;">{phonetic}</span></h2>
        <div style="color:#0066cc; margin-bottom:10px;">{tag_text}</div>
        <h4>详细释义：</h4>
        <div style="line-height:1.8; margin-bottom:15px;">{meaning_html}</div>
        <hr>
        <div style="color:#666; font-size:12px; margin-top:10px;">
        掌握程度：{mastery_text} &nbsp;&nbsp;|&nbsp;&nbsp; 
        添加时间：{word_info['add_time'][:19]} &nbsp;&nbsp;|&nbsp;&nbsp; 
        出现次数：{len(word_info['source_articles'])} 篇文章
        </div>
        """
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"单词详情 - {word}")
        dialog.resize(600, 500)
        layout = QVBoxLayout(dialog)
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setHtml(detail_html)
        layout.addWidget(text_edit)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(dialog.accept)
        layout.addWidget(buttons)
        
        dialog.exec()

    def _translate_whole_article(self):
        if not self.current_article_content.strip():
            QMessageBox.information(self, "提示", "当前没有打开的文章")
            return
        
        if not self.ai_engine.is_available():
            # 离线翻译整篇文章
            self.status_bar.showMessage("正在离线翻译整篇文章...")
            result = self._offline_translate(self.current_article_content)
            self.translation_panel.set_translation(f"【离线整篇翻译】\n{result}\n\n（注：逐词匹配结果，仅供参考，配置AI后可获得流畅整句翻译）")
            self.status_bar.showMessage("离线整篇翻译完成")
            return
        
        try:
            self.status_bar.showMessage("正在翻译整篇文章...")
            target_lang = self.translation_panel.get_target_lang()
            result = self.ai_engine.translate_text(
                self.current_article_content,
                target_lang=target_lang,
                context=""
            )
            self.translation_panel.set_translation(result)
            self.status_bar.showMessage("整篇文章翻译完成")
        except Exception as e:
            QMessageBox.critical(self, "翻译失败", str(e))

    def _import_article(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "导入文章", "", 
            "支持格式 (*.txt *.md *.docx *.pdf);;文本文件 (*.txt *.md);;Word文档 (*.docx);;PDF文档 (*.pdf);;所有文件 (*.*)"
        )
        if file_path:
            article_id, content = self.article_manager.import_article(file_path)
            self._load_article(article_id, content)
            self.status_bar.showMessage(f"已导入文章：{article_id}")

    def _load_article(self, article_id, content):
        self.current_article_id = article_id
        self.current_article_content = content
        
        if article_id.endswith('.md') or content.startswith('#'):
            html = TextProcessor.markdown_to_html(content)
            self.article_view.setHtml(html)
        else:
            self.article_view.setPlainText(content)
        
        article_words = self.vocab_manager.get_article_words(article_id)
        self.vocab_panel.update_article_words(article_words)
        self.vocab_panel.set_current_article(article_id)
        
        # 刷新历史菜单
        self._refresh_history()

    def _on_add_word(self, word, selected_text):
        if not word.strip():
            return
            
        base_form = TextProcessor.simple_base_form(word)
        definition = ""
        
        # 第一步：先查本地内置词典
        local_result = self.local_dict.lookup(base_form)
        if local_result:
            definition = local_result["translation"]
        
        # 第二步：本地没查到，有AI的话用AI查
        if not definition and self.ai_engine.is_available():
            try:
                if self.config["vocabulary"]["auto_reduce_form"]:
                    base_form = self.ai_engine.get_base_form(word)
                definition = self.ai_engine.translate_text(word, self.config["language"]["target_lang"])
            except:
                pass
        
        # 第三步：都没查到，直接存入，不弹框打断阅读
        if not definition:
            definition = "（待补充释义）"
            self.status_bar.showMessage(f"已添加生词：{base_form}（本地未收录，可稍后补充释义）")
        
        self.vocab_manager.add_word(
            word, 
            base_form=base_form, 
            definition=definition,
            source_article=self.current_article_id
        )
        
        article_words = self.vocab_manager.get_article_words(self.current_article_id)
        self.vocab_panel.update_article_words(article_words)
        all_words = self.vocab_manager.get_all_words()
        self.vocab_panel.update_all_words(all_words)
        
        source = "本地词典" if local_result else ("AI" if self.ai_engine.is_available() else "手动")
        self.status_bar.showMessage(f"已添加生词：{base_form}（{source}匹配）")

    def _offline_translate(self, text):
        """离线优化翻译：根据目标语言匹配多语言词典"""
        import re
        
        target_lang = self.translation_panel.get_target_lang()
        lang_key = {
            "zh-CN": "zh", "en": "en", "ja": "ja", "ko": "ko",
            "fr": "fr", "de": "de", "ru": "ru", "es": "es"
        }.get(target_lang, "zh")
        
        # 常见虚词/冠词/介词，翻译时过滤掉
        skip_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 
                      'to', 'of', 'in', 'on', 'at', 'for', 'with', 'by', 'from',
                      'that', 'this', 'these', 'those', 'it', 'its', 'as', 'and',
                      'but', 'or', 'if', 'when', 'what', 'how', 'why', 'where'}
        
        def get_clean_meaning(word):
            base = TextProcessor.simple_base_form(word.lower())
            # 先查多语言词典
            meaning = self.multilang_dict.lookup(word.lower(), lang_key) or self.multilang_dict.lookup(base, lang_key)
            if meaning:
                return meaning
            # 中文目标时再查本地英中词典
            if lang_key == "zh":
                local_res = self.local_dict.lookup(word.lower()) or self.local_dict.lookup(base)
                if local_res:
                    meaning = local_res["translation"]
                    first_part = meaning.split('\n')[0]  # 取第一个释义行
                    return first_part
            return None

        # 拆分句子，按标点断句
        sentences = re.split(r'([.!?;:])', text)
        result_sentences = []
        
        for i in range(0, len(sentences), 2):
            sent = sentences[i].strip()
            punct = sentences[i+1] if i+1 < len(sentences) else ''
            if not sent:
                continue
                
            words = re.findall(r'\b\w+\b', sent)
            translated_words = []
            for w in words:
                wl = w.lower()
                if wl in skip_words:
                    continue
                meaning = get_clean_meaning(w)
                if meaning:
                    translated_words.append(meaning)
                else:
                    translated_words.append(f'[{w}]')
            
            if translated_words:
                result_sentences.append(' '.join(translated_words) + punct)
        
        return ' '.join(result_sentences)

    def _on_translate(self, text):
        if not text.strip():
            return
            
        if not self.ai_engine.is_available():
            # 无AI时用本地词典做离线基础翻译
            result = self._offline_translate(text)
            self.translation_panel.set_translation(f"【离线基础翻译】\n{result}\n\n（注：整句翻译为逐词匹配结果，仅供参考，配置AI后可获得更流畅的翻译）")
            self.status_bar.showMessage("离线翻译完成")
            return
            
        try:
            target_lang = self.translation_panel.get_target_lang()
            result = self.ai_engine.translate_text(
                text, 
                target_lang=target_lang,
                context=self.current_article_content[:500]
            )
            self.translation_panel.set_translation(result)
            self.status_bar.showMessage("AI翻译完成")
        except Exception as e:
            QMessageBox.critical(self, "翻译失败", str(e))

    def _on_word_hovered(self, word):
        pass

    def _on_font_size_changed(self, size):
        if self.current_article_id:
            self.article_manager.save_progress(
                self.current_article_id,
                self.article_view.get_scroll_position(),
                size
            )

    def _on_target_lang_changed(self, lang):
        self.config["language"]["target_lang"] = lang
        self._save_config()

    def _show_generate_dialog(self):
        dialog = GenerateArticleDialog(self)
        if dialog.exec():
            params = dialog.get_parameters()
            try:
                self.status_bar.showMessage("正在生成文章...")
                article = self.ai_engine.generate_article(
                    params["exam_type"],
                    params["theme"],
                    params["word_count"],
                    params["target_words"]
                )
                
                title = f"AI生成_{params['exam_type']}_{params['theme'][:10]}"
                article_id, content = self.article_manager.save_generated_article(title, article)
                self._load_article(article_id, content)
                self.status_bar.showMessage("文章生成完成")
                
            except Exception as e:
                QMessageBox.critical(self, "生成失败", str(e))
                self.status_bar.showMessage("生成失败")

    def _show_settings(self):
        dialog = SettingsDialog(self.config, self)
        if dialog.exec():
            self.config = dialog.get_config()
            self._save_config()
            self.ai_engine = AIEngine(self.config)
            self.status_bar.showMessage("设置已保存")

    def _toggle_focus_mode(self, checked):
        if checked:
            self.right_splitter.hide()
        else:
            self.right_splitter.show()

    def _on_import_vocab(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "导入词库", "", "支持格式 (*.txt *.csv *.xlsx)"
        )
        if file_path:
            try:
                count = self.vocab_manager.import_from_file(file_path, local_dict=self.local_dict)
                all_words = self.vocab_manager.get_all_words()
                self.vocab_panel.update_all_words(all_words)
                QMessageBox.information(self, "导入完成", f"成功导入 {count} 个单词，已自动匹配本地词典释义")
                self.status_bar.showMessage(f"导入词库：{count} 个单词")
            except Exception as e:
                QMessageBox.critical(self, "导入失败", str(e))

    def _on_export_vocab(self):
        file_path, filter = QFileDialog.getSaveFileName(
            self, "导出生词本", "", 
            "Excel文件 (*.xlsx);;CSV文件 (*.csv);;文本文件 (*.txt)"
        )
        if file_path:
            try:
                if filter.startswith("Excel"):
                    fmt = "xlsx"
                elif filter.startswith("CSV"):
                    fmt = "csv"
                else:
                    fmt = "txt"
                    
                words = self.vocab_manager.get_all_words()
                self.vocab_manager.export_to_file(file_path, words, format_type=fmt)
                QMessageBox.information(self, "导出完成", f"生词本已导出到：{file_path}")
                self.status_bar.showMessage("导出完成")
            except Exception as e:
                QMessageBox.critical(self, "导出失败", str(e))

    def _refresh_vocabulary(self):
        all_words = self.vocab_manager.get_all_words()
        self.vocab_panel.update_all_words(all_words)

    def _on_delete_word(self, word):
        self.vocab_manager.delete_word(word)
        # 刷新两个标签页
        all_words = self.vocab_manager.get_all_words()
        self.vocab_panel.update_all_words(all_words)
        if self.current_article_id:
            article_words = self.vocab_manager.get_article_words(self.current_article_id)
            self.vocab_panel.update_article_words(article_words)
        self.status_bar.showMessage(f"已删除单词：{word}")

    def _on_set_mastery(self, word, level):
        self.vocab_manager.update_mastery(word, level)
        # 刷新显示
        all_words = self.vocab_manager.get_all_words()
        self.vocab_panel.update_all_words(all_words)
        level_text = ["未掌握", "熟悉", "已掌握"][level]
        self.status_bar.showMessage(f"已标记 {word} 为：{level_text}")

    def closeEvent(self, event):
        if self.current_article_id:
            self.article_manager.save_progress(
                self.current_article_id,
                self.article_view.get_scroll_position(),
                self.article_view.base_font_size
            )
        event.accept()
