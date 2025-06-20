#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int temp =
                round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtBlue = image[i][j].rgbtGreen = image[i][j].rgbtRed = temp;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int temp1 = round((0.189 * image[i][j].rgbtBlue) + (0.769 * image[i][j].rgbtGreen) +
                              (0.393 * image[i][j].rgbtRed));
            if (temp1 > 255)
                temp1 = 255;
            int temp2 = round((0.168 * image[i][j].rgbtBlue) + (0.686 * image[i][j].rgbtGreen) +
                              (0.349 * image[i][j].rgbtRed));
            if (temp2 > 255)
                temp2 = 255;
            int temp3 = round((0.131 * image[i][j].rgbtBlue) + (0.534 * image[i][j].rgbtGreen) +
                              (0.272 * image[i][j].rgbtRed));
            if (temp3 > 255)
                temp3 = 255;
            image[i][j].rgbtRed = temp1;
            image[i][j].rgbtGreen = temp2;
            image[i][j].rgbtBlue = temp3;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE temp = image[i][width - j - 1];
            image[i][width - j - 1] = image[i][j];
            image[i][j] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    int avgR,avgG,avgB;
    float amount;
    RGBTRIPLE cp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            avgR = 0;
            avgG = 0;
            avgB = 0;
            amount = 0;
            for (int k = -1; k < 2; k++)
            {
                for (int l = -1; l < 2; l++)
                {
                    if(i+k>=0 && i+k<height && j+l>=0 && j+l<width)
                    {
                        avgR = avgR + image[i+k][j+l].rgbtRed;
                        avgG = avgG + image[i+k][j+l].rgbtGreen;
                        avgB = avgB + image[i+k][j+l].rgbtBlue;
                        amount++;
                    }
                }
            }
            cp[i][j].rgbtRed = round(avgR/amount);
            cp[i][j].rgbtGreen = round(avgG/amount);
            cp[i][j].rgbtBlue = round(avgB/amount);
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = cp[i][j].rgbtRed;
            image[i][j].rgbtGreen = cp[i][j].rgbtGreen;
            image[i][j].rgbtBlue = cp[i][j].rgbtBlue;
        }
    }
    return;
}
