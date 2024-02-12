// Calculates readibility level of input text

#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text); // Declaring function which counts all letters in text input
int count_words(string text); // Declaring function which counts all words in text
int count_sentences(string text); // Declaring function which counts all sentences in text

int main(void)
{
    string text = get_string("Text: "); // Prompts user for text input
    int letters = count_letters(text); // Counts all letters in text
    int words = count_words(text); // Counts all words in text
    int sentences = count_sentences(text); // Counts all sentences in text
    float f_letters = (float)letters; // Typecasting int variable into float
    float f_words = (float)words; // Typecasting int variable into float
    float f_sentences = (float)sentences; // Typecasting int variable into float
    float L = f_letters / f_words * 100; // Calculating L
    float S = f_sentences / f_words * 100; // Calculating S
    int grade = round(0.0588 * L - 0.296 * S - 15.8); // Calculating and rounding grade
    if (grade < 1)  // Condition if grade result is below Grade 1
    {
        printf("Before Grade 1\n");
    }
    else if (grade >= 16)  // Condition if grade result is above or equal to Grade 16
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade); // Printing calculated Grade level
    }
}

int count_letters(string text) // Defining function which counts all letters in text
{
    int letters = 0; // Initializing variable counting letters
    for (int i = 0, n = strlen(text); i < n; i++) // Starting a loop, checking below conditions until end of characters in text
    {
        if (islower(text[i])) // If lowercase, increase letters count by one
        {
            letters += 1;
        }
        else if (isupper(text[i])) // If uppercase, increase letters count by one
        {
            letters += 1;
        }
    }
    return letters;
}

int count_words(string text) // Defining function which counts words in text
{
    int words = 1; // Initializing variable counting words, starting from one to account for last word in sentence
    for (int i = 0, n = strlen(text); i < n; i++) // Starting a loop, checking below conditions until end of characters in text
    {
        if (isspace(text[i])) // If whitecase then increase count
        {
            words += 1;
        }
    }
    return words;
}

int count_sentences(string text) // Defining function which counts sentences in text
{
    int sentences = 0; // // Initializing variable counting sentences
    for (int i = 0, n = strlen(text); i < n; i++) // Starting a loop, checking below conditions until end of characters in text
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?') // If period, exclamation or question mark then increase count
        {
            sentences += 1;
        }
    }
    return sentences;
}




