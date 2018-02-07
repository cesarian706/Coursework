#include <stdio.h>
#include <cs50.h>

int height;
int space;
int count;
int hash;
int main(void)
{
    do
    {
        printf("Height: ");
        height = get_int();
    }
    while ((height < 0) || (height > 23));
    for (count = 0; count < height; count++)
    {
        for (space = ((height - 1) - count); space > 0; space--)
        {
            printf(" ");
        }
        for (hash = 0; hash < (count + 2); hash++)
        {
            printf("#");
        }
        printf("\n");
    }
}