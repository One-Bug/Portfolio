#include <cs50.h>
#include <stdio.h>

int heightsize();
void bricks(int h);
int main(void)
{
    int height = heightsize();
    bricks(height);
}

int heightsize()
{
    int h;
    do
    {
        h = get_int("Height: ");
    }
    while (h <= 0);
    return h;
}

void bricks(int h)
{
    for (int i = 0; i < h; i++)
    {
        for (int n = 0; n < (h - (i + 1)); n++)
        {
            printf(" ");
        }

        for (int m = 0; m <= i; m++)
        {
            printf("#");
        }
        printf("  ");
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}
