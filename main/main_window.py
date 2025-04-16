import sys
import os
from PyQt5.QtWidgets import QMainWindow, QWidget,QApplication ,QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QListWidget, QMessageBox, QInputDialog, QLineEdit, QTextEdit, QTabWidget
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.errors import FileNotDecryptedError
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pdf2image import convert_from_path
from PIL import Image
from about_page import AboutPage

class PDFEditorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("PDF Editor")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("logo.png"))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.create_merge_tab()
        self.create_split_tab()
        self.create_delete_tab()
        self.create_rotate_tab()
        self.create_encrypt_tab()
        self.create_decrypt_tab()
        self.create_watermark_tab()
        self.create_metadata_tab()
        self.create_pdf_to_images_tab()
        self.create_images_to_pdf_tab()
        self.create_pdf_to_text_tab()
        self.create_reorder_tab()
        self.create_about_tab()

    def create_about_tab(self):
        tab = AboutPage()
        self.tabs.addTab(tab, "About")

    def create_merge_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        self.merge_list = QListWidget()
        layout.addWidget(self.merge_list)

        add_button = QPushButton("ファイルを追加")
        add_button.clicked.connect(self.add_merge_files)
        layout.addWidget(add_button)

        merge_button = QPushButton("PDFを結合")
        merge_button.clicked.connect(self.merge_pdfs)
        layout.addWidget(merge_button)

        self.tabs.addTab(tab, "PDFを結合")

    def add_merge_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "結合するPDFファイルを選択", "", "PDF Files (*.pdf)")
        if files:
            self.merge_list.addItems(files)

    def merge_pdfs(self):
        if self.merge_list.count() == 0:
            QMessageBox.warning(self, "警告", "結合するファイルが選択されていません。")
            return

        output_path, _ = QFileDialog.getSaveFileName(self, "出力ファイルを保存", "", "PDF Files (*.pdf)")
        if output_path:
            pdf_writer = PdfWriter()
            for i in range(self.merge_list.count()):
                file = self.merge_list.item(i).text()
                pdf_reader = PdfReader(file)
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)
            with open(output_path, 'wb') as out:
                pdf_writer.write(out)
            QMessageBox.information(self, "成功", "PDFが結合されました。")

    def create_split_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        self.split_file_label = QLabel("ファイルが選択されていません。")
        layout.addWidget(self.split_file_label)

        select_button = QPushButton("ファイルを選択")
        select_button.clicked.connect(self.select_split_file)
        layout.addWidget(select_button)

        split_button = QPushButton("PDFを分割")
        split_button.clicked.connect(self.split_pdf)
        layout.addWidget(split_button)

        self.tabs.addTab(tab, "PDFを分割")

    def select_split_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "分割するPDFファイルを選択", "", "PDF Files (*.pdf)")
        if file:
            self.split_file_label.setText(file)

    def split_pdf(self):
        file = self.split_file_label.text()
        if file == "ファイルが選択されていません。":
            QMessageBox.warning(self, "警告", "ファイルが選択されていません。")
            return

        output_folder = QFileDialog.getExistingDirectory(self, "出力フォルダを選択")
        if output_folder:
            pdf_reader = PdfReader(file)
            for i, page in enumerate(pdf_reader.pages):
                pdf_writer = PdfWriter()
                pdf_writer.add_page(page)
                output_path = os.path.join(output_folder, f'page_{i + 1}.pdf')
                with open(output_path, 'wb') as out:
                    pdf_writer.write(out)
            QMessageBox.information(self, "成功", "PDFが分割されました。")

    def create_delete_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        self.delete_file_label = QLabel("ファイルが選択されていません。")
        layout.addWidget(self.delete_file_label)

        select_button = QPushButton("ファイルを選択")
        select_button.clicked.connect(self.select_delete_file)
        layout.addWidget(select_button)

        self.delete_pages_input = QLineEdit()
        self.delete_pages_input.setPlaceholderText("削除するページ番号をカンマ区切りで入力 (例: 1,3,5)")
        layout.addWidget(self.delete_pages_input)

        delete_button = QPushButton("ページを削除")
        delete_button.clicked.connect(self.delete_pages)
        layout.addWidget(delete_button)

        self.tabs.addTab(tab, "ページを削除")

    def select_delete_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "ページを削除するPDFファイルを選択", "", "PDF Files (*.pdf)")
        if file:
            self.delete_file_label.setText(file)

    def delete_pages(self):
        file = self.delete_file_label.text()
        if file == "ファイルが選択されていません。":
            QMessageBox.warning(self, "警告", "ファイルが選択されていません。")
            return

        pages_to_delete = self.delete_pages_input.text()
        if not pages_to_delete:
            QMessageBox.warning(self, "警告", "削除するページ番号が入力されていません。")
            return

        pages_to_delete = list(map(int, pages_to_delete.split(',')))
        output_path, _ = QFileDialog.getSaveFileName(self, "出力ファイルを保存", "", "PDF Files (*.pdf)")
        if output_path:
            pdf_reader = PdfReader(file)
            pdf_writer = PdfWriter()
            for i, page in enumerate(pdf_reader.pages):
                if i + 1 not in pages_to_delete:
                    pdf_writer.add_page(page)
            with open(output_path, 'wb') as out:
                pdf_writer.write(out)
            QMessageBox.information(self, "成功", "ページが削除されました。")

    def create_rotate_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        self.rotate_file_label = QLabel("ファイルが選択されていません。")
        layout.addWidget(self.rotate_file_label)

        select_button = QPushButton("ファイルを選択")
        select_button.clicked.connect(self.select_rotate_file)
        layout.addWidget(select_button)

        self.rotate_angle_input = QLineEdit()
        self.rotate_angle_input.setPlaceholderText("回転角度を入力 (90, 180, 270)")
        layout.addWidget(self.rotate_angle_input)

        rotate_button = QPushButton("PDFを回転")
        rotate_button.clicked.connect(self.rotate_pdf)
        layout.addWidget(rotate_button)

        self.tabs.addTab(tab, "PDFを回転")

    def select_rotate_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "回転するPDFファイルを選択", "", "PDF Files (*.pdf)")
        if file:
            self.rotate_file_label.setText(file)

    def rotate_pdf(self):
        file = self.rotate_file_label.text()
        if file == "ファイルが選択されていません。":
            QMessageBox.warning(self, "警告", "ファイルが選択されていません。")
            return

        angle = self.rotate_angle_input.text()
        if not angle:
            QMessageBox.warning(self, "警告", "回転角度が入力されていません。")
            return

        angle = int(angle)
        output_path, _ = QFileDialog.getSaveFileName(self, "出力ファイルを保存", "", "PDF Files (*.pdf)")
        if output_path:
            pdf_reader = PdfReader(file)
            pdf_writer = PdfWriter()
            for page in pdf_reader.pages:
                page.rotate(angle)
                pdf_writer.add_page(page)
            with open(output_path, 'wb') as out:
                pdf_writer.write(out)
            QMessageBox.information(self, "成功", "PDFが回転されました。")

    def create_encrypt_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        self.encrypt_file_label = QLabel("ファイルが選択されていません。")
        layout.addWidget(self.encrypt_file_label)

        select_button = QPushButton("ファイルを選択")
        select_button.clicked.connect(self.select_encrypt_file)
        layout.addWidget(select_button)

        self.encrypt_password_input = QLineEdit()
        self.encrypt_password_input.setPlaceholderText("パスワードを入力")
        layout.addWidget(self.encrypt_password_input)

        encrypt_button = QPushButton("PDFを暗号化")
        encrypt_button.clicked.connect(self.encrypt_pdf)
        layout.addWidget(encrypt_button)

        self.tabs.addTab(tab, "PDFを暗号化")

    def select_encrypt_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "暗号化するPDFファイルを選択", "", "PDF Files (*.pdf)")
        if file:
            self.encrypt_file_label.setText(file)

    def encrypt_pdf(self):
        file = self.encrypt_file_label.text()
        if file == "ファイルが選択されていません。":
            QMessageBox.warning(self, "警告", "ファイルが選択されていません。")
            return

        password = self.encrypt_password_input.text()
        if not password:
            QMessageBox.warning(self, "警告", "パスワードが入力されていません。")
            return

        output_path, _ = QFileDialog.getSaveFileName(self, "出力ファイルを保存", "", "PDF Files (*.pdf)")
        if output_path:
            pdf_reader = PdfReader(file)
            pdf_writer = PdfWriter()
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)
            pdf_writer.encrypt(password)
            with open(output_path, 'wb') as out:
                pdf_writer.write(out)
            QMessageBox.information(self, "成功", "PDFが暗号化されました。")

    def create_decrypt_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        self.decrypt_file_label = QLabel("ファイルが選択されていません。")
        layout.addWidget(self.decrypt_file_label)

        select_button = QPushButton("ファイルを選択")
        select_button.clicked.connect(self.select_decrypt_file)
        layout.addWidget(select_button)

        self.decrypt_password_input = QLineEdit()
        self.decrypt_password_input.setPlaceholderText("パスワードを入力")
        layout.addWidget(self.decrypt_password_input)

        decrypt_button = QPushButton("PDFを復号化")
        decrypt_button.clicked.connect(self.decrypt_pdf)
        layout.addWidget(decrypt_button)

        self.tabs.addTab(tab, "PDFを復号化")

    def select_decrypt_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "復号化するPDFファイルを選択", "", "PDF Files (*.pdf)")
        if file:
            self.decrypt_file_label.setText(file)

    def decrypt_pdf(self):
        file = self.decrypt_file_label.text()
        if file == "ファイルが選択されていません。":
            QMessageBox.warning(self, "警告", "ファイルが選択されていません。")
            return

        password = self.decrypt_password_input.text()
        if not password:
            QMessageBox.warning(self, "警告", "パスワードが入力されていません。")
            return

        output_path, _ = QFileDialog.getSaveFileName(self, "出力ファイルを保存", "", "PDF Files (*.pdf)")
        if output_path:
            try:
                pdf_reader = PdfReader(file)
                if pdf_reader.is_encrypted:
                    pdf_reader.decrypt(password)
                pdf_writer = PdfWriter()
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)
                with open(output_path, 'wb') as out:
                    pdf_writer.write(out)
                QMessageBox.information(self, "成功", "PDFが復号化されました。")
            except FileNotDecryptedError:
                QMessageBox.warning(self, "エラー", "ファイルの復号化に失敗しました。パスワードが正しくない可能性があります。")

    def create_watermark_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        self.watermark_file_label = QLabel("ファイルが選択されていません。")
        layout.addWidget(self.watermark_file_label)

        select_button = QPushButton("ファイルを選択")
        select_button.clicked.connect(self.select_watermark_file)
        layout.addWidget(select_button)

        self.watermark_text_input = QLineEdit()
        self.watermark_text_input.setPlaceholderText("透かしテキストを入力")
        layout.addWidget(self.watermark_text_input)

        watermark_button = QPushButton("透かしを追加")
        watermark_button.clicked.connect(self.add_watermark)
        layout.addWidget(watermark_button)

        self.tabs.addTab(tab, "透かしを追加")

    def select_watermark_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "透かしを追加するPDFファイルを選択", "", "PDF Files (*.pdf)")
        if file:
            self.watermark_file_label.setText(file)

    def add_watermark(self):
        file = self.watermark_file_label.text()
        if file == "ファイルが選択されていません。":
            QMessageBox.warning(self, "警告", "ファイルが選択されていません。")
            return

        watermark_text = self.watermark_text_input.text()
        if not watermark_text:
            QMessageBox.warning(self, "警告", "透かしテキストが入力されていません。")
            return

        output_path, _ = QFileDialog.getSaveFileName(self, "出力ファイルを保存", "", "PDF Files (*.pdf)")
        if output_path:
            pdf_reader = PdfReader(file)
            pdf_writer = PdfWriter()

            for page in pdf_reader.pages:
                watermark_pdf = self.create_watermark_pdf(watermark_text)
                watermark_reader = PdfReader(watermark_pdf)
                watermark_page = watermark_reader.pages[0]
                page.merge_page(watermark_page)
                pdf_writer.add_page(page)

            with open(output_path, 'wb') as out:
                pdf_writer.write(out)
            QMessageBox.information(self, "成功", "透かしが追加されました。")

    def create_watermark_pdf(self, text):
        temp_pdf = "temp_watermark.pdf"
        c = canvas.Canvas(temp_pdf, pagesize=letter)
        c.setFont("Helvetica", 60)
        c.setFillColorRGB(0.5, 0.5, 0.5, alpha=0.5)
        c.drawString(100, 100, text)
        c.save()
        return temp_pdf

    def create_metadata_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        self.metadata_file_label = QLabel("ファイルが選択されていません。")
        layout.addWidget(self.metadata_file_label)

        select_button = QPushButton("ファイルを選択")
        select_button.clicked.connect(self.select_metadata_file)
        layout.addWidget(select_button)

        self.metadata_title_input = QLineEdit()
        self.metadata_title_input.setPlaceholderText("タイトルを入力")
        layout.addWidget(self.metadata_title_input)

        self.metadata_author_input = QLineEdit()
        self.metadata_author_input.setPlaceholderText("著者を入力")
        layout.addWidget(self.metadata_author_input)

        self.metadata_subject_input = QLineEdit()
        self.metadata_subject_input.setPlaceholderText("サブジェクトを入力")
        layout.addWidget(self.metadata_subject_input)

        metadata_button = QPushButton("メタデータを編集")
        metadata_button.clicked.connect(self.edit_metadata)
        layout.addWidget(metadata_button)

        self.tabs.addTab(tab, "メタデータを編集")

    def select_metadata_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "メタデータを編集するPDFファイルを選択", "", "PDF Files (*.pdf)")
        if file:
            self.metadata_file_label.setText(file)
            pdf_reader = PdfReader(file)
            metadata = pdf_reader.metadata
            self.metadata_title_input.setText(metadata.get('/Title', ''))
            self.metadata_author_input.setText(metadata.get('/Author', ''))
            self.metadata_subject_input.setText(metadata.get('/Subject', ''))

    def edit_metadata(self):
        file = self.metadata_file_label.text()
        if file == "ファイルが選択されていません。":
            QMessageBox.warning(self, "警告", "ファイルが選択されていません。")
            return

        title = self.metadata_title_input.text()
        author = self.metadata_author_input.text()
        subject = self.metadata_subject_input.text()

        output_path, _ = QFileDialog.getSaveFileName(self, "出力ファイルを保存", "", "PDF Files (*.pdf)")
        if output_path:
            pdf_reader = PdfReader(file)
            pdf_writer = PdfWriter()
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)
            if title:
                pdf_writer.add_metadata({'/Title': title})
            if author:
                pdf_writer.add_metadata({'/Author': author})
            if subject:
                pdf_writer.add_metadata({'/Subject': subject})
            with open(output_path, 'wb') as out:
                pdf_writer.write(out)
            QMessageBox.information(self, "成功", "メタデータが編集されました。")

    def create_pdf_to_images_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        self.pdf_to_images_file_label = QLabel("ファイルが選択されていません。")
        layout.addWidget(self.pdf_to_images_file_label)

        select_button = QPushButton("ファイルを選択")
        select_button.clicked.connect(self.select_pdf_to_images_file)
        layout.addWidget(select_button)

        convert_button = QPushButton("PDFを画像に変換")
        convert_button.clicked.connect(self.pdf_to_images)
        layout.addWidget(convert_button)

        self.tabs.addTab(tab, "PDFを画像に変換")

    def select_pdf_to_images_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "画像に変換するPDFファイルを選択", "", "PDF Files (*.pdf)")
        if file:
            self.pdf_to_images_file_label.setText(file)

    def pdf_to_images(self):
        file = self.pdf_to_images_file_label.text()
        if file == "ファイルが選択されていません。":
            QMessageBox.warning(self, "警告", "ファイルが選択されていません。")
            return

        output_folder = QFileDialog.getExistingDirectory(self, "出力フォルダを選択")
        if output_folder:
            images = convert_from_path(file)
            for i, image in enumerate(images):
                image.save(os.path.join(output_folder, f'page_{i + 1}.png'), 'PNG')
            QMessageBox.information(self, "成功", "PDFが画像に変換されました。")

    def create_images_to_pdf_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        self.images_to_pdf_list = QListWidget()
        layout.addWidget(self.images_to_pdf_list)

        add_button = QPushButton("画像を追加")
        add_button.clicked.connect(self.add_images_to_pdf)
        layout.addWidget(add_button)

        convert_button = QPushButton("画像をPDFに変換")
        convert_button.clicked.connect(self.images_to_pdf)
        layout.addWidget(convert_button)

        self.tabs.addTab(tab, "画像をPDFに変換")

    def add_images_to_pdf(self):
        files, _ = QFileDialog.getOpenFileNames(self, "画像ファイルを選択", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if files:
            self.images_to_pdf_list.addItems(files)

    def images_to_pdf(self):
        if self.images_to_pdf_list.count() == 0:
            QMessageBox.warning(self, "警告", "画像が選択されていません。")
            return

        output_path, _ = QFileDialog.getSaveFileName(self, "出力ファイルを保存", "", "PDF Files (*.pdf)")
        if output_path:
            pdf_writer = PdfWriter()
            for i in range(self.images_to_pdf_list.count()):
                image_path = self.images_to_pdf_list.item(i).text()
                img = Image.open(image_path)
                pdf_writer.add_page(img)
            with open(output_path, 'wb') as out:
                pdf_writer.write(out)
            QMessageBox.information(self, "成功", "画像がPDFに変換されました。")

    def create_pdf_to_text_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        self.pdf_to_text_file_label = QLabel("ファイルが選択されていません。")
        layout.addWidget(self.pdf_to_text_file_label)

        select_button = QPushButton("ファイルを選択")
        select_button.clicked.connect(self.select_pdf_to_text_file)
        layout.addWidget(select_button)

        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        layout.addWidget(self.text_output)

        convert_button = QPushButton("PDFをテキストに変換")
        convert_button.clicked.connect(self.pdf_to_text)
        layout.addWidget(convert_button)

        self.tabs.addTab(tab, "PDFをテキストに変換")

    def select_pdf_to_text_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "テキストに変換するPDFファイルを選択", "", "PDF Files (*.pdf)")
        if file:
            self.pdf_to_text_file_label.setText(file)

    def pdf_to_text(self):
        file = self.pdf_to_text_file_label.text()
        if file == "ファイルが選択されていません。":
            QMessageBox.warning(self, "警告", "ファイルが選択されていません。")
            return

        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        self.text_output.setText(text)
        QMessageBox.information(self, "成功", "PDFがテキストに変換されました。")

    def create_reorder_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        self.reorder_file_label = QLabel("ファイルが選択されていません。")
        layout.addWidget(self.reorder_file_label)

        select_button = QPushButton("ファイルを選択")
        select_button.clicked.connect(self.select_reorder_file)
        layout.addWidget(select_button)

        self.reorder_pages_input = QLineEdit()
        self.reorder_pages_input.setPlaceholderText("新しいページ順序をカンマ区切りで入力 (例: 3,1,2)")
        layout.addWidget(self.reorder_pages_input)

        reorder_button = QPushButton("ページ順序を変更")
        reorder_button.clicked.connect(self.reorder_pages)
        layout.addWidget(reorder_button)

        self.tabs.addTab(tab, "ページ順序を変更")

    def select_reorder_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "ページ順序を変更するPDFファイルを選択", "", "PDF Files (*.pdf)")
        if file:
            self.reorder_file_label.setText(file)

    def reorder_pages(self):
        file = self.reorder_file_label.text()
        if file == "ファイルが選択されていません。":
            QMessageBox.warning(self, "警告", "ファイルが選択されていません。")
            return

        pages_order = self.reorder_pages_input.text()
        if not pages_order:
            QMessageBox.warning(self, "警告", "ページ順序が入力されていません。")
            return

        pages_order = list(map(int, pages_order.split(',')))
        output_path, _ = QFileDialog.getSaveFileName(self, "出力ファイルを保存", "", "PDF Files (*.pdf)")
        if output_path:
            pdf_reader = PdfReader(file)
            pdf_writer = PdfWriter()
            for page_num in pages_order:
                pdf_writer.add_page(pdf_reader.pages[page_num - 1])
            with open(output_path, 'wb') as out:
                pdf_writer.write(out)
            QMessageBox.information(self, "成功", "ページ順序が変更されました。")

    def closeEvent(self, event):
        sys.exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFEditorApp()
    window.show()
    sys.exit(app.exec_())