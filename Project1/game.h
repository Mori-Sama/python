
#define ROW 3
#define COL 3
void init_board(char board[ROW][COL],int row, int col);
void show_board(char board[ROW][COL], int row, int col);
void player_move(char board[ROW][COL], int row, int col);
char judge_outcome(char board[ROW][COL], int row, int col);
void player_move1(char board[ROW][COL], int row, int col);
int is_win(char flag);