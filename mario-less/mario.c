#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    do
    {
        // Prompting user for height
        n = get_int("Height: ");
    }
    while ( n < 1 || n > 8);

    // For each row
    for (int i = 0; i < n; i++)
    {
        // First inside loop, checking condition to print empty space
        for (int j = 0; j < n - i - 1; j++)
        {
            printf(" ");
        }

        // Second inside loop, checking condition to print hash
        for (int j = 0; i >= j; j++)
        {
            printf("#");
        }

        //Move to next row
        printf("\n");
    }

}





