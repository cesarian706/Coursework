/**
 * Implements a dictionary's functionality.
 */
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#include "dictionary.h"
//create data type for trie
typedef struct node
{
    bool is_word;
    struct node *children[27];
}
node;
//declare function to free allocated memory for unload()
bool cleanup(node* trav);
//global node pointer for head of trie for use in all functions
node* root;
//track number of words loaded to dictionary
int wordcount;

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    //pointer to root to navigate without changing head pointer
    node *trav = root;
    //compare string length to max
    if(strlen(word) < LENGTH+1)
    {
        int c;
        //iterate for each letter
        for(int i = 0; i < strlen(word); i++)
        {
            //convert letter to correlate to place in array
            c = tolower(word[i]) - 'a';
            //set apostrophe to last element in array
            if(word[i] == '\'')
            {
                c = 26;
            }
            //check if letter exists in dictionary, exit if it does not
            if(trav->children[c] == NULL)
            {
                return false;
            }
            //if letter exists, move pointer to next array
            trav = trav->children[c];
        }
        //confirm word exists in dictionary
        return trav->is_word;
        
    }
    else
    {
        //returns if word is too long
        return false;
    }


    
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    //open dictionary
    FILE* fp = fopen(dictionary, "r");
    //check for valid file pointer
    if (fp != NULL)
    {
        //allocate memory for head pointer
        root = calloc(1,sizeof(node));
        //pointer to navigate trie without changing head pointer
        node* trav = root;
        //gets letter from file
        int ch = fgetc(fp);
        
        //loop until end of file reached
        while(ch != EOF)
        {
            //loop until end of word
            while(isspace(ch) == false)
            {
                //convert letter to correlate to place in array
                int c = tolower(ch) - 'a';
                //set apostrophe to last element in array
                if(ch == '\'')
                {
                    c = 26;
                }
                //allocate memory if none already exists
                if(trav->children[c] == NULL)
                {
                    trav->children[c] = calloc(1,sizeof(node));
                    trav = trav->children[c];
                    
                }
                //advance pointer to next array
                else
                {
                    trav = trav->children[c];
                }
                //get next letter
                ch = fgetc(fp);
                
            }
            //mark end of word true
            trav->is_word = true;
            //reset pointer to head
            trav = root;
            //increment number of words in dictionary
            wordcount++;
            //get next letter
            ch = fgetc(fp);
        }
        //close dictionary file
        fclose(fp);
        return true;
    }
    else
    {
        return false;
    }
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    if(wordcount > 0)
    {
        return wordcount;
    }
    else
    {
        return 0;
    }
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    //pointer to root to navigate without changing head pointer
    node* trav = root;
    //pass pointer to cleanup function
    bool check = cleanup(trav);
    if(check)
    {
        return true;
    }
    else
    {
        return false;
    }
}

//free allocated memory
bool cleanup(node* trav)
{
    //check if there is something to free
    if(trav == NULL)
    {
        return true;
    }
    //iterate for every element in every level of trie
    for(int i = 0; i < 27; i++)
    {
        //check for allocated memory
        if(trav->children[i] != NULL)
        {
            //pointer to hold current position
            node* temp = trav;
            //advance original pointer to next level
            trav = trav->children[i];
            //begin function again starting at lowest level reached
            cleanup(trav);
            //after bottom of trie is reached, adjust pointer
            trav = temp;
        }
    }
    //free allocated memory at current pointer
    free(trav);
    return true;
    
}