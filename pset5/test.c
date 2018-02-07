/**
 * Implements a dictionary's functionality.
 */
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#include "dictionary.h"
typedef struct node
{
    bool is_word;
    struct node *children[27];
}
node;
void cleanup(node* trav);

node* root;


int wordcount;

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    // TODO
    node *trav = root;
    if(strlen(word) < LENGTH)
    {
        int c;
        for(int i = 0; i < strlen(word); i++)
        {
            c = tolower(word[i]) - 'a';
            if(c == '\'')
            {
                c = 26;
            }
            if(trav->children[c] == NULL)
            {
                return false;
            }
            trav = trav->children[c];
        }
        return trav->is_word;
        
    }
    else
    {
        return false;
    }


    
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    // TODO
    FILE* fp = fopen(dictionary, "r");
    if (fp != NULL)
    {
        root = calloc(1,sizeof(node));
        node* trav = root;
        
        int ch = fgetc(fp);
        

        while(ch != EOF)
        {
            while(isspace(ch) == false)
            {
                int c = tolower(ch) - 'a';
                if(ch == '\'')
                {
                    c = 26;
                }
                if(trav->children[c] == NULL)
                {
                    trav->children[c] = calloc(1,sizeof(node));
                    trav = trav->children[c];
                    
                }
                else
                {
                    trav = trav->children[c];
                }
                ch = fgetc(fp);
                
            }
            trav->is_word = true;
            trav = root;
            wordcount++;
            ch = fgetc(fp);
        }
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
    // TODO
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
    //root is global pointer to trie
    node* trav = root;
    cleanup(trav);
    
    if(root == NULL)
    {
        free(root);
        return true;
    }
    else
    {
        return false;
    }
}


void cleanup(node* trav)
{
    if(trav == NULL)
    {
        free(trav);
    }
    for(int i = 0; i < 27; i++)
    {
        if(trav->children[i] != NULL)
        {
            node* temp = trav;
            trav = trav->children[i];
            cleanup(trav);
            trav = temp;
        }
    }
    free(trav);
    
    
}