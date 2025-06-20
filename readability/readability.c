#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int gletters(string t);
int gsentences(string t);
int gwords(string t);
int main(void)
{
    string text = get_string("Text: ");
    int letters = gletters(text);
    int sentences = gsentences(text);
    int words = gwords(text);
    double L = letters / (float) words * 100;
    double S = sentences / (float) words * 100;
    int index = round(0.0588 * L - 0.296 * S - 15.8);
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        if (index >= 1 && index <= 16)
        {
            printf("Grade %i\n", index);
        }
        else
        {
            printf("Grade 16+\n");
        }
    }
}
int gletters(string t)
{
    int letters = 0;
    for (int i = 0; i < strlen(t); i++)
    {
        if (isalpha(t[i]) != 0)
        {
            letters++;
        }
    }

    return letters;
}
int gwords(string t)
{
    int words = 1;
    for (int k = 0; k < strlen(t); k++)
    {
        if (t[k] == ' ')
        {
            words++;
        }
    }

    return words;
}
int gsentences(string t)
{
    int sentences = 0;
    for (int j = 0; j < strlen(t); j++)
    {
        if ((t[j] == '!') || (t[j] == '.') || (t[j] == '?'))
        {
            sentences++;
        }
    }

    return sentences;
}
