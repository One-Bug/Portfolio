#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int points[] = {1, 3, 3, 2,  1, 4, 2, 4, 1, 8, 5, 1, 3,
                1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
void score(string p1, string p2);
int main(void)
{
    string player1 = get_string("Player 1: ");
    string player2 = get_string("Player 2: ");
    score(player1, player2);
}

void score(string p1, string p2)
{
    int score1 = 0;
    int score2 = 0;
    for (int i = 0; i < strlen(p1); i++)
    {
        if (isupper(p1[i]))
        {
            score1 += points[p1[i] - 'A'];
        }
        else
        {
            if (islower(p1[i]))
            {
                score1 += points[p1[i] - 'a'];
            }
        }
    }
    for (int i = 0; i < strlen(p2); i++)
    {
        if (isupper(p2[i]))
        {
            score2 += points[p2[i] - 'A'];
        }
        else
        {
            if (islower(p2[i]))
            {
                score2 += points[p2[i] - 'a'];
            }
        }
    }

    if (score1 > score2)
    {
        printf("Player 1 Wins!\n");
    }
    else
    {
        if (score2 > score1)
        {
            printf("Player 2 Wins!\n");
        }
        else
        {
            if (score1 == score2)
            {
                printf("Tie!\n");
            }
        }
    }
}
