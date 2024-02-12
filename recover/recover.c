// Recover files from forensic image

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <cs50.h>

#define BLOCK_SIZE 512  // Defining FAT block size
typedef uint8_t BYTE;  // Defining new data type

int main(int argc, char *argv[])
{
    // Check for invalid usage
    if (argc != 2)
    {
        printf("Usage: ./recover filename\n");
        return 1;
    }

    // Open the forensic image file
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Could not open a file");
        return 2;
    }

    // Declaring buffer array to store data read from the file
    BYTE buffer[BLOCK_SIZE];

    // Declaring a buffer to store name of JPG file
    char filename[8];

    // Initializing JPG files counter
    int file_counter = 0;

    // Setting a pointer to JPG file
    FILE *img = NULL;

    // Iterating over 512B blocks of data
    while (fread(buffer, 1, BLOCK_SIZE, file) == BLOCK_SIZE)
    {
        // If JPG signature found
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // If first JPG
            if (img == NULL)
            {
                // Print filename
                sprintf(filename, "%03i.jpg", file_counter);

                // Open JPG file & assign a pointer to it
                img = fopen(filename, "w");

                // Write to JPG file
                fwrite(buffer, 1, BLOCK_SIZE, img);

            }

            // If next JPG found
            else
            {
                // Close current file
                fclose(img);

                // Update counter
                file_counter++;

                // Print next JPG's filename to memory buffer
                sprintf(filename, "%03i.jpg", file_counter);

                // Open a new JPG file & assign operator to it
                img = fopen(filename, "w");

                // Write to JPG file
                fwrite(buffer, 1, BLOCK_SIZE, img);
            }
        }

        // If already found JPG
        else
        {
            if (img != NULL)
            {
                // Keep writing to this file
                fwrite(buffer, 1, BLOCK_SIZE, img);
            }
        }
    }

    // Close the remaining files
    fclose(file);
    fclose(img);
    file_counter++;

    return 0;
}