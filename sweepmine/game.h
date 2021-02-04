#pragma once
// 在这里设定矩阵大小
#define ROW 9
#define COL 9
#define ROWS  ROW + 2
#define COLS  COL + 2
// 这里设定雷数量
#define MINE_COUNT 10
#include<stdio.h>
#include<time.h>
#include<stdlib.h>
void init_board(char board[ROWS][COLS], int row, int col, char a);
void create_mine(char board[ROWS][COLS], int row, int col);
void show_board(char mine[ROWS][COLS], int row, int col);
void get_player(char board[ROWS][COLS],char mine[ROWS][COLS], int row, int col);
int calculation_mine(char board[ROWS][COLS], char mine[ROWS][COLS], int row, int col);
void play(char board[ROWS][COLS], char mine[ROWS][COLS], int x, int y);
