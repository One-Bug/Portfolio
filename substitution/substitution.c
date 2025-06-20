#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (isalpha(argv[1][i]) == false)
        {
            printf("Key must only contain aplhabetic characters.\n");
            return 1;
        }
        for (int j = i + 1; j < strlen(argv[1]) + 1; j++)
        {
            if (toupper(argv[1][i]) == toupper(argv[1][j]))
            {
                printf("Key must not contain repeated characters.\n");
                return 1;
            }
        }
    }
    string plaintext = get_string("plaintext: ");
    printf("ciphertext: ");
    for (int i = 0; i < strlen(plaintext); i++)
    {
        if (plaintext[i] >= 'A' && plaintext[i] <= 'Z')
        {
            printf("%c", toupper(argv[1][plaintext[i] - 65]));
        }
        if (plaintext[i] >= 'a' && plaintext[i] <= 'z')
        {
            printf("%c", tolower(argv[1][plaintext[i] - 97]));
        }
        else
        {
            if (isalpha(plaintext[i]) == false)
            {
                printf("%c", plaintext[i]);
            }
        }
    }
    printf("\n");
}
