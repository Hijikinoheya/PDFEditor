#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifdef _WIN32
#include <windows.h>
#endif

void clearScreen() {
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif
}

void waitForEnter() {
    printf("\n続行するにはEnterキーを押してください...");
    getchar();
}

void showAgreement() {
    clearScreen();
    printf("PDF Master\n");
    printf("Version 3.0 Final Release\n");
    printf("? By Team Hijikinoheya. All rights reserved.\n\n");
    printf("本ソフトウェアは、簡易的にPDFを編集するためのツールです。\n\n");
    printf("免責事項:\n");
    printf("本ソフトウェアの使用によって生じたいかなる損害についても、開発者は責任を負いません。自己責任でご利用ください。\n\n");
    printf("本ソフトウェアは、GNU General Public License v2.0（以下「GPL-2.0」）に基づいて配布されています。以下の条件に同意する場合のみ、本ソフトウェアをご利用いただけます。\n\n");
    printf("【禁止事項】\n");
    printf("1. 本ソフトウェアの一部または全部を、GPL-2.0 に反する形で再配布すること。\n");
    printf("2. 本ソフトウェアに含まれるロゴファイル（例：logo.png）を、無断で商用利用または改変して再配布すること。\n");
    printf("3. 本ソフトウェアのソースコードを非公開のまま再配布すること。\n\n");
    printf("【GPL-2.0 ライセンスの概要】\n");
    printf("- 本ソフトウェアを自由に使用、複製、配布、改変することができます。\n");
    printf("- 改変したソフトウェアを配布する場合、同じGPL-2.0ライセンスの下で配布しなければなりません。\n");
    printf("- ソースコードを入手可能な形で提供する必要があります。\n");
    printf("- 本ソフトウェアは「現状のまま」提供され、いかなる保証もありません。\n\n");
    printf("詳細は、以下のURLをご参照ください：\n");
    printf("https://www.gnu.org/licenses/old-licenses/gpl-2.0.html\n\n");
    printf("【連絡先】\n");
    printf("本ソフトウェアに関するお問い合わせは、以下の連絡先までご連絡ください：\n");
    printf("Email: admin@hijikinoheya.com\n");
    printf("また、質問や技術的なサポートが必要な場合も同様にご連絡ください。\n\n");
    printf("【著作権】\n");
    printf("本ソフトウェアに関連するすべての著作権は、Team Hijikinoheyaに帰属します。許可なくソフトウェアの一部または全体を使用、コピー、改変、再配布することはできません。\n\n");
    printf("【最終確認】\n");
    printf("本ソフトウェアを使用することで、本ライセンス契約の内容に同意したものとみなされます。ユーザーは、本ライセンスに記載されたすべての条件を十分に理解し、同意した上で使用を開始してください。\n\n");
    printf("[1] 同意する\n[2] 同意しない\n");
    int choice;
    scanf("%d", &choice);
    getchar(); // Enterキー処理
    if (choice != 1) {
        printf("同意しなかったため終了します。\n");
        exit(0);
    }
}

void installLibraries() {
    printf("必要なライブラリをインストール中...\n\n");
#ifdef _WIN32
    system("chcp 65001 > nul"); // UTF-8に設定
#endif
    const char *libs[] = {
        "pip install PyQt5",
        "pip install PyPDF2",
        "pip install reportlab",
        "pip install pdf2image",
        "pip install Pillow"
    };
    for (int i = 0; i < sizeof(libs)/sizeof(libs[0]); i++) {
        printf("実行中: %s\n", libs[i]);
        system(libs[i]);
    }
    printf("\nライブラリのインストールが完了しました。\n");
    waitForEnter();
}

void runPythonScript() {
    printf("main/main.py を実行します...\n\n");
#ifdef _WIN32
    system("chcp 65001 > nul");
#endif
    system("python ./main/main.py");
    waitForEnter();
}

void openGitHub() {
#ifdef _WIN32
    system("start https://github.com/Hijikinoheya/PDFMaster/tree/main");
#else
    system("xdg-open https://github.com/Hijikinoheya/PDFMaster/tree/main");
#endif
    waitForEnter();
}

void showPopplerNotice() {
    printf("注意：pdf2imageを使用するには、別途popplerのインストールが必要です。\n");
    printf("Windows環境でのインストール方法については、以下のリンクを参照してください。\n");
    printf("https://github.com/oschwartz10612/poppler-windows/releases\n");
    printf("popplerのbinディレクトリをPATHに追加するか、コード内でpoppler_pathを指定してください。\n\n");
    waitForEnter();
}

int main() {
    showAgreement();
    int choice;
    while (1) {
        clearScreen();
        printf("===== メニュー =====\n");
        printf("1. 必要なライブラリをインストール\n");
        printf("2. Pythonスクリプトを実行 (main/main.py)\n");
        printf("3. GitHubリポジトリを開く\n");
        printf("4. popplerのインストール案内を見る\n");
        printf("5. 終了\n");
        printf("番号を入力してください: ");
        scanf("%d", &choice);
        getchar(); // 改行クリア

        switch (choice) {
            case 1:
                installLibraries();
                break;
            case 2:
                runPythonScript();
                break;
            case 3:
                openGitHub();
                break;
            case 4:
                showPopplerNotice();
                break;
            case 5:
                printf("終了します。\n");
                return 0;
            default:
                printf("無効な選択です。\n");
                waitForEnter();
        }
    }
}
