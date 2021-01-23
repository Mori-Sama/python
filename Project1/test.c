#define _CRT_SECURE_NO_WARNINGS 1
#include<stdio.h>
#include"game.h"
void menu()
{
	printf("     1.play  0.exit     \n");

}
void game()
{
	char board[ROW][COL] = { 0 };
	// 初始化棋盘
	init_board(board,ROW,COL);
	// 打印棋盘
	show_board(board, ROW, COL);
	while (1)
	{
		char flag;
		player_move(board, ROW, COL);
		show_board(board, ROW, COL);
		if (is_win(judge_outcome(board, ROW, COL)))
		{
			break;
		}
		player_move1(board, ROW, COL);
		show_board(board, ROW, COL);
		if (is_win(judge_outcome(board, ROW, COL)))
		{
			break;
		}
	}

}
int main()
{
	int a;
	do
	{
		printf("请输入对应序号开始游戏\n");
		menu();
		scanf("%d", &a);
		switch (a)
		{
		case 1:
			game();
			break;
		case 0:
			break;
		default:
			printf("输入有误，请重新输入！");
			break;
		}
	} while (a);
	return 0;
}