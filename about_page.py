from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class AboutPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # ロゴを表示
        logo_label = QLabel(self)
        logo_pixmap = QPixmap("logo.png")
        logo_pixmap = logo_pixmap.scaled(200, 60, Qt.KeepAspectRatio)  # サイズを200x60に調整
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Aboutテキスト
        about_text = QLabel("""
        <h1>PDF Master</h1>
        <p>Version 3.0 Final Release</p>
        <p>🄫 By Team Hijkinoheya. All rights reserved.</p>
        <p>本ソフトウェアは、簡易的にPDFを編集するためのツールです。</p>
        <font color="red"><p><strong>免責事項:</strong></p></font>
        <font color="red"><b><p>本ソフトウェアの使用によって生じたいかなる損害についても、開発者は責任を負いません。自己責任でご利用ください。</p></b></font>
        <p><a href="https://home.hijikinoheya.com">ホームページはこちら</a></p>
        <p><b>PDFを画像に変換するためには、Popplerをインストールしてください。</b></p>
        <p><a href="https://github.com/oschwartz10612/poppler-windows">こちらからダウンロードしてください。</a></p>
        <p><b>Popplerをダウンロードした後、PCのPathに通してお使いください。</b></p>              
        """)
        about_text.setFont(QFont("Arial", 12))
        about_text.setOpenExternalLinks(True)
        layout.addWidget(about_text)