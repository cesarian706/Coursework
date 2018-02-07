/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
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

/**
 * Sorts array of n values.
 */
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
