#include "helpers.h"

void colorize(int height, int width, RGBTRIPLE image[height][width])
{
    // Change all black pixels to a color of your choosing
    for (int i = 0; i < height; i++)  // For each row
    {
        for (int j = 0; j < width; j++)  // For each column
        {
            if (image[i][j].rgbtBlue == 0 && image[i][j].rgbtGreen == 0 && image[i][j].rgbtRed == 0) // Check if a pixel is black
            {
                image[i][j].rgbtBlue = 90; // Change it to another colour
                image[i][j].rgbtGreen = 50;
                image[i][j].rgbtRed = 10;
            }
        }
    }
}

