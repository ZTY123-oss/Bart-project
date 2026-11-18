# Bart project
#include <iostream>
#include <cstdlib>
#include <ctime>
#include <windows.h>
#include <conio.h>

using namespace std;

// 烟花效果
void firework() {
    system("cls");
    cout << "\n\n";
    
    // 烟花爆炸效果
    for (int i = 0; i < 3; i++) {
        // 烟花上升
        for (int j = 0; j < 10; j++) {
            system("cls");
            cout << "\n\n";
            for (int k = 0; k < 10 - j; k++) cout << " ";
            cout << "  ↑" << endl;
            Sleep(50);
        }
        
        // 烟花爆炸
        system("cls");
        cout << "\n\n";
        cout << "        *   *   *" << endl;
        cout << "      *  ✨ ✨ ✨  *" << endl;
        cout << "    *  ✨ 恭喜答对！ ✨  *" << endl;
        cout << "      *  ✨ ✨ ✨  *" << endl;
        cout << "        *   *   *" << endl;
        
        // 改变颜色
        HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
        SetConsoleTextAttribute(hConsole, i * 4 + 12);
        Sleep(300);
        SetConsoleTextAttribute(hConsole, 7); // 恢复默认颜色
    }
    
    cout << "\n\n";
}

int main() {
    srand(time(0));
    int number = rand() % 100 + 1; // 生成1-100的随机数
    int guess;
    int attempts = 0;
    
    cout << "=================================" << endl;
    cout << "      欢迎来到猜数字游戏！" << endl;
    cout << "=================================" << endl;
    cout << "我已经想好了一个1-100之间的数字" << endl;
    cout << "看看你能几次猜中！" << endl;
    cout << "=================================\n" << endl;
    
    while (true) {
        cout << "请输入你的猜测：";
        cin >> guess;
        attempts++;
        
        if (guess > number) {
            cout << "太大了！再试一次。\n" << endl;
        } else if (guess < number) {
            cout << "太小了！再试一次。\n" << endl;
        } else {
            cout << "\n🎉 恭喜你！答对了！" << endl;
            cout << "你用了 " << attempts << " 次猜中！" << endl;
            
            // 播放烟花
            firework();
            
            cout << "\n还想再玩一次吗？(y/n): ";
            char playAgain;
            cin >> playAgain;
            
            if (playAgain == 'y' || playAgain == 'Y') {
                number = rand() % 100 + 1;
                attempts = 0;
                system("cls");
                cout << "新的一局开始！\n" << endl;
            } else {
                cout << "\n谢谢游玩！再见！" << endl;
                break;
            }
        }
    }
    
    return 0;
}