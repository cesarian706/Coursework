#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>


int main(void)
{   // get input from user
    string s = get_string();
    // capitalize first initial
    printf("%c", toupper (s[0]));
    // iterate loop for length of string
    for (int i = 0; i < strlen(s); i++)
    {
        // test for whitespace
        if (isspace(s[i]))
        {
        //print character following space
        printf("%c", toupper (s[i+1]));
        }
    }
    printf("\n");
    
}