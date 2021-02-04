#define _CRT_SECURE_NO_WARNINGS 1
#include"game.h"
void game()
{
	srand((unsigned int)time(NULL));
	char board[ROWS][COLS] = { '0' };
	char mine[ROWS][COLS] = { '0' };
	// 初始化棋盘
	init_board(board, ROW, COL, '0');
	init_board(mine, ROW, COL, '*');
	// 生成随机位置地雷
	create_mine(board, ROW, COL);
	show_board(board, ROW, COL);
	// 打印棋盘
	show_board(mine, ROW, COL);
	// 玩家输入
	get_player(board, mine, ROW, COL);

}


void menu()
{
	printf("     1.play     \n");
	printf("     0.exit     \n");
}

void test()
{
	int a;
	do
	{
		menu();
		scanf("%d", &a);
		switch (a)
		{
		case 1:
			game();
			break;
		case 0:
			printf("退出游戏\n");
			break;
		default:
			printf("？？？\n");
			break;
		}
	} while (a);
}

int main()
{
	test();

	return 0;
}