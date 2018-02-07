#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <unistd.h>

#define DIM_MIN 3
#define DIM_MAX 9

int board[DIM_MAX][DIM_MAX];

int d;

void init(void);
void draw(void);
bool move(int tile);

int main(int argc, string argv[])
{
    if(argc != 2)
    {
        return 1;
    }
    d = atoi(argv[1]);
    init();
    draw();
}

void init(void)
{
    int c = (d * d);
    int count = c;
    for(int i = 0; i < d; i ++)
    {
        for(int j = 0; j < d; j ++)
        {
            board [i][j] = (count -1);
            count --;
        }
    }
    if(((d * d) % 2) == 0)
    {
        int x = board[d][(d - 1)];
        int y = board[d][(d - 2)];
        board[d][(d - 1)] = y;
        board[d][(d - 2)] = x;
    }
}

void draw(void)
{
    for(int i = 0; i < d; i ++)
    {
        for(int j = 0; j < d; j ++)
        {
            printf("%2i", board [i][j]);
        }
        printf("\n");
    }
}

bool move(int tile)
{
    // TODO
    int tile = get_int();
    if (tile <= d && tile != 0)
    {
        int a;
        int b;
        int x;
        int y;
        for(int i = 0; i < d; i++)
        {
            for(int j = 0; j < d; j++)
            {
                if(board[i][j] == tile)
                {
                    x=i;
                    y=j;
                }
                if(board[i][j] == 0)
                {
                    a=i;
                    b=j;
                }
            }
        }
        if(x == a)
        {
            if(y != (b+ 1) || y != (b - 1))
            {
                return false;
            }
        }
        if(y == b)
        {
            if(x != (a + 1) || x != (a - 1))
            {
                return false;
            }
        }
        else
        {
            board[x][y] = 0;
            board[a][b] = tile;
            return true;
        }
    }
    return false;
}

//need to copy array position and element value for space and tile for swap later. return false if tile not found


 // Returns true if game is won (i.e., board is in winning configuration), 
 // else false.
 
bool won(void)
{
    // TODO
    int start = 0;
    int end = (d * d);
    if(start < end)
    {
        int min = 1;
        for(int i = 0; i < d; i++)
        {
            for(int j = 0; j < d; j++)
            {
                
                if(board[i][j] > min)
                {
                    break;
                    return false;
                }
                if(board[i][j] <= min)
                {
                    start ++;
                    min = board[i][j];
                }
            }
        }
    }
    if(start == end)
    {
        return true;
    }
    return false;
    
}







int count = -1;
    while(count != 0)
    count = 0;
    for(int i = 0; i < d; i++)
    {
        for(int j = 0; j < d; j++)
        {
            if(board[i][j] > ((board[i][j]) + 1)))
            {
                count ++;
            }
        }
    }