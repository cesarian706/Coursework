#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint8_t  BYTE;
int i = 0;

int main(int argc, char *argv[])
{
    //check validity of source file
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover infile\n");
        return 1;
    }
    // remember filename
    char *infile = argv[1];
    // open input file 
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }
    //set array for output file names
    char filename[8];
    sprintf(filename, "%03i.jpg",i);
    FILE *outptr = fopen(filename, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", filename);
        return 3;
    }
    //set array for temporary storage from infile
    BYTE buffer[512];
    //loop while buffer array is 512 bytes
    while(fread(&buffer, 512, 1, inptr) == 1)
    {
        //check first four bytes for file header signature
        if(buffer[0] == 0xff &&
        buffer[1] == 0xd8 &&
        buffer[2] == 0xff &&
        (buffer[3] & 0xe0) == 0xe0)
        {
            //close current file, open new file, increment filename
            fclose(outptr);
            sprintf(filename, "%03i.jpg",i);
            fopen(filename, "w");
            i ++;
            //write current fread to new file
            fwrite(&buffer, 1, 512, outptr);
        }
        //write to file until new header is found
        else
        {
            fwrite(&buffer, 512, 1, outptr);
        }
    }
    //close remaining files
    fclose(outptr);
    fclose(inptr);
    // success
    return 0;
}
