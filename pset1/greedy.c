#include <stdio.h>
#include <cs50.h>
#include <math.h>
float money;

int main(void)
{
    do
    {
    printf("O hai! How much change is owed?\n");
    money = get_float();
    }
    while (money < 0);
    int r = 0;
    int change = roundf (money * 100);
    
    int quarter = change / 25;
    r = change % 25;
    int dime = r / 10;
    r = r % 10;
    int nickel = r / 5;
    r = r % 5;
    int penny = r / 1;
    int output = (quarter + dime + nickel + penny);
    printf("%i\n", output);
    
}