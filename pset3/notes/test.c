#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
void sort(int values[], int n);
bool search(int value, int values[], int n);

const int MAX = 65536;

int main(void)
{
    int needle = 42;
   
    // fill haystack
    int size;
    int haystack[MAX];
    for (size = 0; size < MAX; size++)
    {
        // wait for hay until EOF
        printf("\nhaystack[%i] = ", size);
        int straw = get_int();
        if (straw == INT_MAX)
        {
            break;
        }
     
        // add hay to stack
        haystack[size] = straw;
    }
    printf("\n");

    // sort the haystack
    sort(haystack, size);
    
    for(int i =0; i < size; i++)
    {
        printf("%i", haystack[i]);
    }
    if (search(needle, haystack, size))
    {
        printf("\nFound needle in haystack!\n\n");
        return 0;
    }
    else
    {
        printf("\nDidn't find needle in haystack.\n\n");
        return 1;
    }
}

void sort(int values[], int n)
{
    int count = -1;
    while(count != 0)
    {
        count = 0;
        for(int i =0; i < (n-1); i++)
        {
            if(values[i] > values[i+1])
            {
                int a= values [i];
                int b= values[i+1];
                values[i]= b;
                values[i+1]= a;
                count++;
            }
        }
    }
    return;
}



bool search(int value, int values[], int n)
{
    //test that array has at least one element
    if(n<0)
    {
        return false;
    }
    //set starting values for binary search
    int start = 0;
    int end = (n - 1);
    //search array until start and end values overlap
    while(start <= end)
    {
        //cut array in half based on starting variables
        int p = ((start + end) / 2);
        int x = values[p];
        //return true if first element is target
        if(x == value)
        {
            return true;
        }
        //cut array in half based on value of current target element
        if(x > value)
        {
            end = (p - 1);
        }
        if (x < value)
        {
            start = (p + 1);
        }
        
    }
    //return false if target is not found
    return false;
}
