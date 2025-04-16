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
    printf("\n���s����ɂ�Enter�L�[�������Ă�������...");
    getchar();
}

void showAgreement() {
    clearScreen();
    printf("PDF Master\n");
    printf("Version 3.0 Final Release\n");
    printf("? By Team Hijikinoheya. All rights reserved.\n\n");
    printf("�{�\�t�g�E�F�A�́A�ȈՓI��PDF��ҏW���邽�߂̃c�[���ł��B\n\n");
    printf("�Ɛӎ���:\n");
    printf("�{�\�t�g�E�F�A�̎g�p�ɂ���Đ����������Ȃ鑹�Q�ɂ��Ă��A�J���҂͐ӔC�𕉂��܂���B���ȐӔC�ł����p���������B\n\n");
    printf("�{�\�t�g�E�F�A�́AGNU General Public License v2.0�i�ȉ��uGPL-2.0�v�j�Ɋ�Â��Ĕz�z����Ă��܂��B�ȉ��̏����ɓ��ӂ���ꍇ�̂݁A�{�\�t�g�E�F�A�������p���������܂��B\n\n");
    printf("�y�֎~�����z\n");
    printf("1. �{�\�t�g�E�F�A�̈ꕔ�܂��͑S�����AGPL-2.0 �ɔ�����`�ōĔz�z���邱�ƁB\n");
    printf("2. �{�\�t�g�E�F�A�Ɋ܂܂�郍�S�t�@�C���i��Flogo.png�j���A���f�ŏ��p���p�܂��͉��ς��čĔz�z���邱�ƁB\n");
    printf("3. �{�\�t�g�E�F�A�̃\�[�X�R�[�h�����J�̂܂܍Ĕz�z���邱�ƁB\n\n");
    printf("�yGPL-2.0 ���C�Z���X�̊T�v�z\n");
    printf("- �{�\�t�g�E�F�A�����R�Ɏg�p�A�����A�z�z�A���ς��邱�Ƃ��ł��܂��B\n");
    printf("- ���ς����\�t�g�E�F�A��z�z����ꍇ�A����GPL-2.0���C�Z���X�̉��Ŕz�z���Ȃ���΂Ȃ�܂���B\n");
    printf("- �\�[�X�R�[�h�����\�Ȍ`�Œ񋟂���K�v������܂��B\n");
    printf("- �{�\�t�g�E�F�A�́u����̂܂܁v�񋟂���A�����Ȃ�ۏ؂�����܂���B\n\n");
    printf("�ڍׂ́A�ȉ���URL�����Q�Ƃ��������F\n");
    printf("https://www.gnu.org/licenses/old-licenses/gpl-2.0.html\n\n");
    printf("�y�A����z\n");
    printf("�{�\�t�g�E�F�A�Ɋւ��邨�₢���킹�́A�ȉ��̘A����܂ł��A�����������F\n");
    printf("Email: admin@hijikinoheya.com\n");
    printf("�܂��A�����Z�p�I�ȃT�|�[�g���K�v�ȏꍇ�����l�ɂ��A�����������B\n\n");
    printf("�y���쌠�z\n");
    printf("�{�\�t�g�E�F�A�Ɋ֘A���邷�ׂĂ̒��쌠�́ATeam Hijikinoheya�ɋA�����܂��B���Ȃ��\�t�g�E�F�A�̈ꕔ�܂��͑S�̂��g�p�A�R�s�[�A���ρA�Ĕz�z���邱�Ƃ͂ł��܂���B\n\n");
    printf("�y�ŏI�m�F�z\n");
    printf("�{�\�t�g�E�F�A���g�p���邱�ƂŁA�{���C�Z���X�_��̓��e�ɓ��ӂ������̂Ƃ݂Ȃ���܂��B���[�U�[�́A�{���C�Z���X�ɋL�ڂ��ꂽ���ׂĂ̏������\���ɗ������A���ӂ�����Ŏg�p���J�n���Ă��������B\n\n");
    printf("[1] ���ӂ���\n[2] ���ӂ��Ȃ�\n");
    int choice;
    scanf("%d", &choice);
    getchar(); // Enter�L�[����
    if (choice != 1) {
        printf("���ӂ��Ȃ��������ߏI�����܂��B\n");
        exit(0);
    }
}

void installLibraries() {
    printf("�K�v�ȃ��C�u�������C���X�g�[����...\n\n");
#ifdef _WIN32
    system("chcp 65001 > nul"); // UTF-8�ɐݒ�
#endif
    const char *libs[] = {
        "pip install PyQt5",
        "pip install PyPDF2",
        "pip install reportlab",
        "pip install pdf2image",
        "pip install Pillow"
    };
    for (int i = 0; i < sizeof(libs)/sizeof(libs[0]); i++) {
        printf("���s��: %s\n", libs[i]);
        system(libs[i]);
    }
    printf("\n���C�u�����̃C���X�g�[�����������܂����B\n");
    waitForEnter();
}

void runPythonScript() {
    printf("main/main.py �����s���܂�...\n\n");
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
    printf("���ӁFpdf2image���g�p����ɂ́A�ʓrpoppler�̃C���X�g�[�����K�v�ł��B\n");
    printf("Windows���ł̃C���X�g�[�����@�ɂ��ẮA�ȉ��̃����N���Q�Ƃ��Ă��������B\n");
    printf("https://github.com/oschwartz10612/poppler-windows/releases\n");
    printf("poppler��bin�f�B���N�g����PATH�ɒǉ����邩�A�R�[�h����poppler_path���w�肵�Ă��������B\n\n");
    waitForEnter();
}

int main() {
    showAgreement();
    int choice;
    while (1) {
        clearScreen();
        printf("===== ���j���[ =====\n");
        printf("1. �K�v�ȃ��C�u�������C���X�g�[��\n");
        printf("2. Python�X�N���v�g�����s (main/main.py)\n");
        printf("3. GitHub���|�W�g�����J��\n");
        printf("4. poppler�̃C���X�g�[���ē�������\n");
        printf("5. �I��\n");
        printf("�ԍ�����͂��Ă�������: ");
        scanf("%d", &choice);
        getchar(); // ���s�N���A

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
                printf("�I�����܂��B\n");
                return 0;
            default:
                printf("�����ȑI���ł��B\n");
                waitForEnter();
        }
    }
}
