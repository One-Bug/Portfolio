#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint8_t BYTE;
int main(int argc, char *argv[])
{
    int counter = 0;
    if (argc < 2)
    {
        printf("Usage: ./recover infile\n");
        return 1;
    }
    char *infile = argv[1];
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        printf("Could not open %s.\n", infile);
        return 1;
    }
    BYTE buffer[512];
    char filename[8];
    FILE *jpg = NULL;
    while (fread(buffer, sizeof(BYTE), 512, inptr) == 512)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            if (counter == 0)
            {
                sprintf(filename, "%03i.jpg", counter);
                counter++;
                jpg = fopen(filename, "w");
                fwrite(&buffer, sizeof(BYTE), 512, jpg);
            }
            else if (counter > 0)
            {
                fclose(jpg);
                sprintf(filename, "%03i.jpg", counter);
                counter++;
                jpg = fopen(filename, "w");
                fwrite(&buffer, sizeof(BYTE), 512, jpg);
            }
        }
        else if (counter > 0)
        {
            fwrite(&buffer, sizeof(BYTE), 512, jpg);
        }
    }

    fclose(inptr);
    fclose(jpg);
}
