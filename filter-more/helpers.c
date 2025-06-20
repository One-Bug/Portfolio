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
    int avgR, avgG, avgB;
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
                    if (i + k >= 0 && i + k < height && j + l >= 0 && j + l < width)
                    {
                        avgR = avgR + image[i + k][j + l].rgbtRed;
                        avgG = avgG + image[i + k][j + l].rgbtGreen;
                        avgB = avgB + image[i + k][j + l].rgbtBlue;
                        amount++;
                    }
                }
            }
            cp[i][j].rgbtRed = round(avgR / amount);
            cp[i][j].rgbtGreen = round(avgG / amount);
            cp[i][j].rgbtBlue = round(avgB / amount);
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

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    int GxR, GxG, GxB, GyR, GyG, GyB;
    int gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            GxR = 0;
            GxG = 0;
            GxB = 0;
            GyR = 0;
            GyG = 0;
            GyB = 0;
            for (int k = -1; k < 2; k++)
            {
                for (int l = -1; l < 2; l++)
                {
                    if (i + k >= 0 && i + k < height && j + l >= 0 && j + l < width)
                    {
                        GxR += (image[i + k][j + l].rgbtRed * gx[k + 1][l + 1]);
                        GyR += (image[i + k][j + l].rgbtRed * gy[k + 1][l + 1]);
                        GxG += (image[i + k][j + l].rgbtGreen * gx[k + 1][l + 1]);
                        GyG += (image[i + k][j + l].rgbtGreen * gy[k + 1][l + 1]);
                        GxB += (image[i + k][j + l].rgbtBlue * gx[k + 1][l + 1]);
                        GyB += (image[i + k][j + l].rgbtBlue * gy[k + 1][l + 1]);
                    }
                    else
                    {
                        continue;
                    }
                }
            }
            int tcolor;

            tcolor = round(sqrt(pow(GxR, 2) + pow(GyR, 2)));
            temp[i][j].rgbtRed = tcolor;
            if (tcolor > 255)
            {
                temp[i][j].rgbtRed = 255;
            }
            tcolor = round(sqrt(pow(GxG, 2) + pow(GyG, 2)));
            temp[i][j].rgbtGreen = tcolor;
            if (tcolor > 255)
            {
                temp[i][j].rgbtGreen = 255;
            }
            tcolor = round(sqrt(pow(GxB, 2) + pow(GyB, 2)));
            temp[i][j].rgbtBlue = tcolor;
            if (tcolor > 255)
            {
                temp[i][j].rgbtBlue = 255;
            }
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
        }
    }
    return;
}
