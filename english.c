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
    printf("\nPress Enter to continue...");
    getchar();
}

void showAgreement() {
    clearScreen();
    printf("PDF Master\n");
    printf("Version 3.0 Final Release\n");
    printf("🄫 By Team Hijikinoheya. All rights reserved.\n\n");
    printf("This software is a tool for basic PDF editing.\n\n");
    printf("Disclaimer:\n");
    printf("The developer is not responsible for any damage caused by using this software. Use at your own risk.\n\n");
    printf("This software is distributed under the GNU General Public License v2.0 (GPL-2.0). You may use it only if you agree to the terms below.\n\n");
    printf("[Prohibited Actions]\n");
    printf("1. Redistributing this software in a manner that violates the GPL-2.0 license.\n");
    printf("2. Using or modifying logo files (e.g., logo.png) for commercial purposes without permission.\n");
    printf("3. Redistributing the source code without making it publicly available.\n\n");
    printf("[GPL-2.0 License Summary]\n");
    printf("- You are free to use, copy, distribute, and modify this software.\n");
    printf("- Modified versions must also be distributed under the GPL-2.0 license.\n");
    printf("- You must provide the source code when distributing.\n");
    printf("- This software is provided \"as-is\" with no warranties.\n\n");
    printf("More details: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html\n\n");
    printf("[Contact]\n");
    printf("For inquiries, contact:\n");
    printf("Email: admin@hijikinoheya.com\n");
    printf("Technical support is also available via the same email.\n\n");
    printf("[Copyright Notice]\n");
    printf("All copyrights related to this software belong to Team Hijikinoheya. Unauthorized use, copying, modification, or redistribution is prohibited.\n\n");
    printf("[Final Confirmation]\n");
    printf("By using this software, you are deemed to have agreed to this license agreement.\n");
    printf("Please use it only after fully understanding and agreeing to the terms.\n\n");
    printf("[1] Agree\n[2] Disagree\n");

    int choice;
    scanf("%d", &choice);
    getchar();
    if (choice != 1) {
        printf("You did not agree. Exiting...\n");
        exit(0);
    }
}

void installLibraries() {
    printf("Installing required libraries...\n\n");
#ifdef _WIN32
    system("chcp 65001 > nul");
#endif
    const char *libs[] = {
        "pip install PyQt5",
        "pip install PyPDF2",
        "pip install reportlab",
        "pip install pdf2image",
        "pip install Pillow"
    };
    for (int i = 0; i < sizeof(libs)/sizeof(libs[0]); i++) {
        printf("Running: %s\n", libs[i]);
        system(libs[i]);
    }
    printf("\nLibrary installation complete.\n");
    waitForEnter();
}

void runPythonScript() {
    printf("Running main/main.py...\n\n");
#ifdef _WIN32
    system("chcp 65001 > nul");
#endif
    system("python main/main.py");
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
    printf("Note: To use pdf2image, Poppler needs to be installed separately.\n");
    printf("For installation on Windows, please refer to the following link:\n");
    printf("https://github.com/oschwartz10612/poppler-windows/releases\n");
    printf("Add the Poppler bin directory to PATH, or specify poppler_path in your code.\n\n");
    waitForEnter();
}

int main() {
    showAgreement();
    int choice;
    while (1) {
        clearScreen();
        printf("===== MENU =====\n");
        printf("1. Install required libraries\n");
        printf("2. Run Python script (main/main.py)\n");
        printf("3. Open GitHub repository\n");
        printf("4. Show Poppler installation info\n");
        printf("5. Exit\n");
        printf("================\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        getchar();
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
                printf("Exiting...\n");
                exit(0);
            default:
                printf("Invalid choice. Try again.\n");
                waitForEnter();
        }
    }
    return 0;
}
