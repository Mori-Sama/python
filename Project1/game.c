#define _CRT_SECURE_NO_WARNINGS 1
#include<stdio.h>
#include"game.h"
void init_board(char board[ROW][COL],int row, int col)
{
	for (int i = 0; i < row; i++)
	{
		for  (int j = 0;j < col; j++)
		{
			board[i][j] = ' ';
		}
	}
}

void show_board(char board[ROW][COL], int row, int col)
{
	for (int i = 0; i < row; i++)
	{
		for (int j = 0; j < col; j++)
		{
			printf(" %c ", board[i][j]);
			if (j < col - 1)
			{
				printf("|");
			}
		}
		printf("\n");
		if (i < row - 1)
		{
			for (int k = 0; k < row; k++)
			{
				printf("---");
				if (k < row - 1)
				{
					printf("|");
				}
			}
		}
		printf("\n");
	}
}
void player_move(char board[ROW][COL], int row, int col)
{
	int x,y;
	while (1)
	{
		printf("请输入坐标\n");
		scanf("%d%d", &x, &y);
		if ((x <= row && y <= col) && (x > 0 && y > 0))
		{
			if (board[x - 1][y - 1] == ' ')
			{
				board[x - 1][y - 1] = '*';
				break;
			}
			else
			{
				printf("此处存在棋子！\n");
			}
		}
		else
		{
			printf("输入错误！\n");
		}
	}
}
void player_move1(char board[ROW][COL], int row, int col)
{
	int x, y;
	while (1)
	{
		printf("请输入坐标\n");
		scanf("%d%d", &x, &y);
		if ((x <= row && y <= col) && (x > 0 && y > 0))
		{
			if (board[x - 1][y - 1] == ' ')
			{
				board[x - 1][y - 1] = '#';
				break;
			}
			else
			{
				printf("此处存在棋子！\n");
			}
		}
		else
		{
			printf("输入错误！\n");
		}
	}
}
int is_full(char board[ROW][COL], int row, int col)
{
	for (int i = 0; i < row; i++)
	{
		for (int j = 0; j < col; j++)
		{
			if (board[i][j] == ' ')
			{
				return 0;
			}
		}
	}
	return 1;
}

char judge_outcome(char board[ROW][COL], int row, int col)
{
	for (int i = 0; i < row; i++)
	{
		int count = 0;
		for (int j = 0; j < col-1; j++)
		{
			if ((board[i][j] != ' ') && (board[i][j] == board[i][j + 1]))
			{
				count++;
			}
		}
		if (count == col - 1)
		{
			return board[i][0];
		}
		count = 0;
		for (int j = 0; j < col-1; j++)
		{
			if ((board[j][i] != ' ') && (board[j][i] == board[j+1][i]))
			{
				count++;
			}
		}
		if (count == col-1)
		{
			return board[0][i];
		}
		count = 0;
		for (int j = 0; j < col-1; j++)
		{
			if ((board[j][j] != ' ') && (board[j][j] == board[j + 1][j + 1]))
			{
				count++;
			}
		}
		if (count == col-1)
		{
			return board[0][0];
		}
	}
	if (is_full(board, ROW, COL))
	{
		return 'd';
	}
	return 'c';
}

int is_win(char flag)
{
	if (flag == '*')
	{
		printf("玩家1获胜！！！\n");
		return 1;
	}
	else if (flag == '#')
	{
		printf("玩家2获胜！！！\n");
		return 1;
	}
	else if (flag == 'd')
	{
		printf("平局\n");
		return 1;
	}
	else
	{
		return 0;
	}
}