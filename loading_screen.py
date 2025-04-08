from PyQt5.QtWidgets import QSplashScreen, QVBoxLayout, QWidget, QLabel, QProgressBar, QMessageBox
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer

class LoadingScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 白背景のウィジェットを作成
        self.setStyleSheet("background-color: white;")

        # レイアウトを設定
        layout = QVBoxLayout()
        self.setLayout(layout)

        # ロゴを表示（サイズを大きくする）
        logo_label = QLabel(self)
        logo_pixmap = QPixmap("logo.png")
        if logo_pixmap.isNull():
            QMessageBox.critical(self, "エラー", "ロゴ画像が見つかりません。")
            return
        logo_pixmap = logo_pixmap.scaled(300, 100, Qt.KeepAspectRatio)  # サイズを300x100に調整
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # バージョン情報を表示
        version_label = QLabel("PDF Editor Version 3.0 Final Release.\n🄫 By Team Hijkinoheya. All rights reserved.", self)
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setFont(QFont("Arial", 10))
        layout.addWidget(version_label)

        # メッセージを表示するラベル
        self.loading_text = QLabel("", self)
        self.loading_text.setAlignment(Qt.AlignCenter)
        self.loading_text.setFont(QFont("Arial", 12))
        layout.addWidget(self.loading_text)

        # プログレスバーを表示
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # ウィンドウ設定
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.resize(600, 400)  # ウィンドウサイズを大きくする

        # メッセージのリスト
        self.messages = [
            "GUIを読み込み中...",
            "機能を読み込み中...",
            "アップデートを確認中...",
            "設定を確認中...",
            "リソースをロード中...",
            "初期化中...",
            "準備中..."
        ]
        self.current_message_index = 0

        # メッセージ切り替え用のタイマー
        self.message_timer = QTimer()
        self.message_timer.timeout.connect(self.update_message)
        self.message_timer.start(1000)  # 1秒ごとにメッセージを更新

        # プログレスバーのアニメーション用のタイマー
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.update_progress)
        self.progress_timer.start(20)  # 40ミリ秒ごとに更新

    def update_message(self):
        # メッセージを順番に切り替える
        if self.current_message_index < len(self.messages):
            self.loading_text.setText(self.messages[self.current_message_index])
            self.current_message_index += 1
        else:
            # 最後のメッセージで止める
            self.loading_text.setText("準備中...")
            self.message_timer.stop()

    def update_progress(self):
        current_value = self.progress_bar.value()
        if current_value < 100:
            self.progress_bar.setValue(current_value + 1)
        else:
            self.progress_timer.stop()

    def finish(self, main_window):
        QTimer.singleShot(4000, lambda: self.close_and_show_main(main_window))  # 4秒後にメインウィンドウを表示

    def close_and_show_main(self, main_window):
        self.close()
        main_window.show()