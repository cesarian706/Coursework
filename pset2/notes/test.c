#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
//set constant for alphabet shift in ascii
#define UCONTROL 65
#define LCONTROL 97
//accept user input at command line
int l;
int main(int argc, string argv[])
{
    //check input viability
    if(argc > 2 || argc <2)
    {
        //check user if input invalid
        printf("Enter one keyword!\n");
        return 1;
    }
    string k = argv[1];
    if(isalpha(argv[1]))
    {
        //prompt user for string input
        printf("plaintext:  ");
        string p = get_string();
    
        printf("ciphertext: ");
        //iterate for string length
        for (int i = 0; i < strlen(p); i++)
        {//l is length of keyword
            for(l = 0; l < strlen(argv[1]); l++)
            //check if char is letter, if so: check for letter case, print case preserved letter with cipher shift
            if(isupper (p[i]))
            {
                printf("%c", (((p[i] - UCONTROL) + k[l]) % 26) + UCONTROL);
            }
            if(islower (p[i]))
            {
                printf("%c", (((p[i] - LCONTROL) + k[l]) % 26) + LCONTROL);
            }
            if(l == strlen(argv[1]))
            {
                l = 0;
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
    return 1;
}