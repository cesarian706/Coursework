#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

int main(int argc, string argv[])
{
     if(argc > 2 || argc <2)
    {
        //check user if input invalid
        printf("Enter one keyword!\n");
        return 1;
    }
    string p = get_string();
    string k = argv[1];
    //loop for iteration of cipher key. integrate into caesar code main loop body
    int j = 0; for(int i = 0; i < strlen(p); i++)
        {
            if(isalpha(p[i]))
            {
                if(isupper(k[j]))
                {
                    char x = k[j] - 
                }
            }
            
            
            //adjust key variable to int if upper
            if(isupper(k[j])
            {
                int c = (k[j] - 65);
            }
            //adjust key variable to int if lower
            if(islower(k[j])
            {
                int c = (k[j] - 97);
            }
            else
            {
                printf("%c", p[i]);
            }
            if(l == strlen(argv[1]))
            l == 0;
        }
}
