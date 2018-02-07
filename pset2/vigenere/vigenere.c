#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
//set constant for alphabet shift in ascii
#define UCONTROL 65
#define LCONTROL 97
//accept user input at command line
int main(int argc, string argv[])
{
    string k = argv[1];
    //check input viability
    if(argc > 2 || argc <2)
    {
        //check user if input invalid
        printf("Enter one keyword, no numbers!\n");
        return 1;
    }
    for(int c=0; c<strlen(k);c++)
    {
        if(isdigit(k[c]))
        {
            printf("Enter one keyword, no numbers!\n");
            return 1;
        }
    }
    //prompt user for message to encode
    printf("plaintext:  ");
    string p = get_string();
    
    printf("ciphertext: ");
    //iterate for string length
    int j = 0; for (int i = 0; i < strlen(p); i++)
    {
        //check if char is letter
        if(isalpha (p[i]))
        {
            //change character of key to cipher shift
            char x = (toupper (k[j]) - UCONTROL);if(isupper (p[i]))
            {
                printf("%c", (((p[i] - UCONTROL) + x) % 26) + UCONTROL);
                j++;
            }
            if(islower (p[i]))
            {
                printf("%c", (((p[i] - LCONTROL) + x) % 26) + LCONTROL);
                j++;
            }
            // reset key if shorter than message
            if (j == strlen(k))
            {
                j = 0;
            }
        }
        //if char not letter, print original input
        else
        {
             printf("%c", p[i]);
        }
    }
    printf("\n");
    return 0;
}