// Encrypts text using Caesar's code method

#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

bool check_key(string s);

int main(int argc, string argv[])
{
    // Making sure program was run with just one command line argument
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;  // If not a single command line argument, early exit
    }

    // Making sure every character in argv[1] is a digit
    bool goodkey = check_key(argv[1]);
    if (goodkey == false)
    {
        printf("Usage: ./caesar key\n");
        return 1; // If any of the command line argument is not a digit, exit early
    }

    // Converting argv[1] from a `string` to an `int`
    int key = atoi(argv[1]);

    // Prompt user for plaintext
    string plaintext = get_string("plaintext:  ");
    printf("ciphertext: ");
    for (int i = 0; i < strlen(plaintext); i++) // For every character of plaintext
    {
        if (islower(plaintext[i])) // For every lowercase letter
        {
            printf("%c", (plaintext[i] - 97 + key) % 26 + 97); // Rotate letter using key parameter
        }
        else if (isupper(plaintext[i]))  // For every uppercase letter
        {
            printf("%c", (plaintext[i] - 65 + key) % 26 + 65); // Rotate letter using key parameter
        }
        else
        {
            printf("%c", plaintext[i]);  // If not a letter, print the same character
        }
    }
    printf("\n");
}

bool check_key(string s) // Defining a function which checks whether the key is composed only of digits
{
    for (int i = 0; i < strlen(s); i++)
    {
        if (isdigit(s[i]) == 0)
        {
            return false;
        }
    }
    return true;
}

