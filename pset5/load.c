typedef struct node
{
    bool is_word;
    struct node *children[27]
}
node;

node* root;
node* trav;
int wordcount;




//load
FILE* fp = fopen(dictionary, "r");
if (fp == NULL)
{
    return false;
}

node* root = malloc(sizeof(node));
trav = root;

int c = tolower(fgetc(fp)) - 'a'
if(c == '\'')
{
    c = 26;
}

while(c != EOF)
{
    while(isspace(c) == false)
    {
        if(c == '\'')
        {
            c = 26;
        }
        if(trav->children[c] == NULL)
        {
            trav->children[c] = malloc(sizeof(node));
            trav = trav->children[c];
        }
        else
        {
            trav = trav->children[c];
        }
        c = tolower(fgetc(fp)) - 'a';
        
    }
    trav->is_word = true;
    trav = root;
    wordcount++;
    c = tolower(fgetc(fp)) - 'a';
}
fclose(fp);
return true;

//unload
void clean(node* trav)
for(int i = 0; i < 27; i++)
{
    if(trav->children[i] != NULL)
    {
        trav = trav->children[i];
        clean(trav);
    }
    else
    {
        for(i = 0; i < 27; i++)
        {
            free(trav->children[i]);
        }
        
    }
}
free(trav);
return true;


bool unload(void)
{
    // TODO
    node *trav = root;
    if(wordcount > 0)
    {
        for(int i = 0; i < 27; i++)
        {
            if(trav->children[i] != NULL)
            {
                trav = trav->children[i];
                unload();
            }
        }
        free(trav);
        return true;
    }
    else
    {
        return false;
    }
}


//check

int c;
for(int i = 0; i < strlen(word); i++)
{
    c = tolower(fgetc(word[i])) - 'a'
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
trav = root;