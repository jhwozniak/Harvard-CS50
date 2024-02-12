// Caclulates number of years requierd for population to grow to specific size

#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    // Prompt for start size
    int start_size;
    do
    {
        start_size = get_int("Start size: ");
    }
    while (start_size < 9);

    int current_size = start_size;

    // Prompt for end size
    int end_size;
    do
    {
        end_size = get_int("End size: ");
    }
    while (end_size < start_size);

    // Calculate number of years until we reach threshold
    int years = 0;
    while(current_size < end_size)
    {
        // Update years tracker
        years++;

        // Update size
        current_size = current_size + round(current_size / 3) - round(current_size / 4);
    }

    // Print number of years
    printf("Years: %i\n", years);
}
