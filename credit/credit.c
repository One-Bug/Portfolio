#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

int valid(long c);
void valid2(long c, int d);
void type(long c, int d);
int main(void)
{
    long card = get_long("Number: ");
    int digits = valid(card);
    valid2(card, digits);
    type(card, digits);
}

int valid(long c)
{
    int digits = 0;
    while (c != 0)
    {
        c /= 10;
        digits++;
    }
    if (digits < 13)
    {
        printf("INVALID\n");
        exit(0);
    }
    return digits;
}

void valid2(long c, int d)
{
    int val = 0;
    for (int i = 0; i < d / 2; i++)
    {
        long temp = (c / pow(10, 1 + 2 * i));
        temp = temp % 10;
        temp = temp * 2;
        if (temp >= 10)
        {
            val = val + (temp % 10) + (temp / 10 % 10);
        }
        else
        {
            val = val + temp;
        }
    }
    if (d % 2 == 1)
    {
        for (int i = 0; i < (d / 2) + 1; i++)
        {
            long temp = (c / pow(10, 2 * i));
            temp = temp % 10;
            val = val + temp;
        }
    }
    else
    {
        for (int i = 0; i < (d / 2); i++)
        {
            long temp = (c / pow(10, 2 * i));
            temp = temp % 10;
            val = val + temp;
        }
    }

    if (val % 10 != 0)
    {
        printf("INVALID\n");
        exit(0);
    }
}

void type(long c, int d)
{
    int val1 = 0;
    int val2 = 0;
    if (d == 15)
    {
        val1 = c / pow(10, 14);
        val2 = c / pow(10, 13);
        val2 = val2 % 10;
        if (val1 == 3 && (val2 == 4 || val2 == 7))
        {
            printf("AMEX\n");
        }
        else
        {
            printf("INVALID\n");
            exit(0);
        }
    }
    if (d == 13)
    {
        val1 = c / pow(10, 12);
        if (val1 == 4)
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
            exit(0);
        }
    }
    if (d == 16)
    {
        val1 = c / pow(10, 15);
        val2 = c / pow(10, 14);
        val2 = val2 % 10;
        if (val1 == 4)
        {
            printf("VISA\n");
        }
        else
        {
            if (val1 == 5 && (val2 == 1 || val2 == 2 || val2 == 3 || val2 == 4 || val2 == 5))
            {
                printf("MASTERCARD\n");
            }
            else
            {
                printf("INVALID\n");
                exit(0);
            }
        }
    }
}
