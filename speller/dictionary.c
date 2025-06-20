// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Represents a node in a hash table

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

typedef struct node
{
    char word;
    struct node *path[N];
    bool end;
} node;

// Hash table
node *tries;
int size_counter = 0;

node *make(char word)
{
    node *n = (node *) calloc(1, sizeof(node));
    for (int i = 0; i < N; i++)
        n->path[i] = NULL;
    n->end = false;
    n->word = word;
    return n;
}

bool freeW(node *n)
{
    for (int i = 0; i < N; i++)
    {
        if (n->path[i] != NULL)
        {
            freeW(n->path[i]);
        }
        else
        {
            continue;
        }
    }
    free(n);
    return true;
}

node *insert(node *r, char *word)
{
    node *temp = r;

    for (int i = 0; word[i] != '\0'; i++)
    {
        int idx = tolower(word[i]) - 'a';
        if (temp->path[idx] == NULL)
        {
            temp->path[idx] = make(word[i]);
        }
        else
        {
        }
        temp = temp->path[idx];
    }
    temp->end = true;
    size_counter++;
    return r;
}

int search(node *r, const char *word)
{
    node *temp = r;
    for (int i = 0; word[i] != '\0'; i++)
    {
        int p = tolower(word[i]) - 'a';
        if (temp->path[p] == NULL)
            return 0;
        temp = temp->path[p];
    }
    if (temp != NULL && temp->end == true)
        return 1;
    return 0;
}

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    if (search(tries, word) == 0)
    {
        return false;
    }
    else
    {
        return true;
    }
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    char word[LENGTH + 1];
    node *trie = make('\0');
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }
    while (fscanf(file, "%s", word) != EOF)
    {
        tries = insert(trie, word);
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return size_counter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO

    if (freeW(tries))
    {
        return true;
    }
    else
    {
        return false;
    }
}
