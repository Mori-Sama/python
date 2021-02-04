#define _CRT_SECURE_NO_WARNINGS 1
#include"game.h"


void init_board(char board[ROWS][COLS], int row, int col, char a)
{
	for (int i = 0; i < row + 2; i++)
	{
		for (int j = 0; j < col + 2; j++)
		{
			board[i][j] = a;
		}
	}
}


void create_mine(char board[ROWS][COLS], int row, int col)
{
	int count = 0;
	do
	{
		int x = (rand() % row) + 1;
		int y = (rand() % col) + 1;
		if (board[x][y] == '0')
		{
			board[x][y] = '1';
			count++;
		}
	} while (count < MINE_COUNT);
}


void show_board(char mine[ROWS][COLS], int row, int col)
{
	for (int i = 0; i <= row; i++)
	{
		printf("%d ", i);
	}
	printf("\n");
	for (int i = 1; i <= row; i++)
	{
		printf("%d ", i);
		for (int j = 1; j <= col; j++)
		{
			printf("%c ", mine[i][j]);
		}
		printf("\n");
	}
}


void get_player(char board[ROWS][COLS], char mine[ROWS][COLS], int row, int col)
{
	while (1)
	{
		int x = 0, y = 0;
		printf("请输入坐标\n");
		scanf("%d%d", &x, &y);
		if (x > 0 && y > 0 && x <= ROW && y < COL)
		{
			if (board[x][y] == '1')
			{
				printf("死！！！\n");
				break;
			}
			else
			{
				if (mine[x][y] == '*')
				{
					play(board, mine, x, y);
					show_board(mine, ROW, COL);
				}
				else
				{
					printf("？？？\n");
				}
			}
		}
		else
		{
			printf("？？？\n");
		}
	}
}


int calculation_mine(char board[ROWS][COLS], char mine[ROWS][COLS], int x, int y)
{
	if (x > 0 && y > 0 && x <= ROW && y <= COL)
	{
		// 循环计算
		int a = 0;
		for (int i = x - 1; i <= x + 1; i++)
		{
			for (int j = y - 1; j <= y + 1; j++)
			{
				if (i == x && j == y)
				{
					continue;
				}
				else if (mine[i][j] == '*')
				{
					a += (board[i][j] - '0');
				}
				else
				{
					continue;
				}
			}
		}
		if (a != 0)
		{
			mine[x][y] = a + '0';
			return 0;
		}
		else
		{
			mine[x][y] = ' ';
			return 1;
		}
	}
	return 2;
}


void play(char board[ROWS][COLS], char mine[ROWS][COLS], int x, int y)
{
	int a = calculation_mine(board, mine, x, y);
	if (a == 1)
	{
		for (int i = x - 1; i <= x + 1; i++)
		{
			for (int j = y - 1; j <= y + 1; j++)
			{
				if (mine[i][j] == '*')
				{
					play(board, mine, i, j);
				}
			}
		}
	}
}