#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#define UCONTROL 65
#define LCONTROL 97
//accept user input at command line
int main(int argc, string argv[])
{
    //check input viability
    if(argc > 2 || argc <2)
    {
        //check user if input invalid
        printf("Enter non-negative integer!\n");
        return 1;
    }
    //convert command line string input to int value
    int k = atoi(argv[1]);
    //prompt user for string input
    printf("plaintext:  ");
    string p = get_string();
    printf("ciphertext: ");
    
    //iterate for string length
    for (int i = 0; i < strlen(p); i++)
    {
        //if so, check for letter case, print case preserved letter with cipher shift
        if(isalpha (p[i]))
        {
                if(isupper (p[i]))
                {
                    printf("%c", (((p[i] - UCONTROL) + k) % 26) + UCONTROL);
                }
                if(islower (p[i]))
                {
                    printf("%c", (((p[i] - LCONTROL) + k) % 26) + LCONTROL);
                }
        }
        else
        {
             printf("%c", p[i]);
        }
    }
    printf("\n");
    return 0;
}