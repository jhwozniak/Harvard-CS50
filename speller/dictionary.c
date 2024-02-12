// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <stdio.h>
#include <cs50.h>
#include <stdint.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Main pointer to the nodes within the hash table
node *ptr = NULL;

// Tracker of words read from dictionary
int words_tracker;

// Initializing load flag
bool if_loaded = false;

// Global storage for hash code
unsigned int hash_code;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Initializing storage for hash code
    hash_code = hash(word);

    // Reset pointer to the 1st node
    ptr = table[hash_code];

    // Traversing down the linked list looking for the word, if not found then misspelled
    while(ptr != NULL)
    {
        // Check if found
        if (strcasecmp(word, ptr->word) == 0)
        {
            return true;
        }

        // If not, move to the next node
        else
        {
            ptr = ptr->next;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Sums ASCII values of a word and returns remainder after division by N
    int sum = 0;
    for(int j = 0; word[j] != '\0'; j++)
    {
        sum += tolower(word[j]);
    }

    return sum % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Opens dictionary file
    FILE *dct = fopen(dictionary, "r");
    if (dct == NULL)
    {
        printf("Could not open\n");
        return false;
        if_loaded = false;
    }

    // Buffer to temporaily store word from dictionary
    char buffer[LENGTH + 1];

    // Initializing storage for hash code
    hash_code = 0;

    // Initializing words tracker
    words_tracker = 0;

    // Getting rid of garbage values in hash table
    table[N - 1] = NULL;

    // Reads each string from the file and copies to temporary buffer until the end of file
    while (fscanf(dct, "%s", buffer) != EOF)
    {
        // Creates new node
        ptr = malloc(sizeof(node));
        if (ptr == NULL)
        {
            if_loaded = false;
            return false;
        }

        // Copies string from buffer into node
        strcpy(ptr->word, buffer);

        // Set next node adress to NULL
        ptr->next = NULL;

        // Hashing the copied word
        hash_code = hash(buffer);

        // Prepends the node to the hash table
        ptr->next = table[hash_code];
        table[hash_code] = ptr;

        // Keep track of words copied into hash table
        words_tracker++;
    }
    if_loaded = true;
    fclose(dct);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    if(if_loaded != true)
    {
        return 0;
    }
    else
    {
        return words_tracker;
    }
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Set a temporary pointer
    node *tmp = NULL;

    // For every branch of the hash table
    for (int k = 0; k < N; k++)
    {
        // Reset main pointer to the 1st node
        ptr = table[k];

        // Traverse down the linked list
        while (ptr != NULL)
        {
            // Point temporary pointer where the main pointer points
            tmp = ptr;

            // Move ptr to the next node
            ptr = ptr->next;

            // Free memory for current node
            free(tmp);
        }
    }
    return true;
}
