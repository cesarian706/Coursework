#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint8_t  BYTE;
int i = 0;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover infile\n");
        return 1;
    }
    // remember filenames
    char *infile = argv[1];
   
  
    // open input file 
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }
    char filename[8];
    sprintf(filename, "%03i.jpg",i);
    FILE *outptr = fopen(filename, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", filename);
        return 3;
    }
    
    
    BYTE buffer[512];
    fread(&buffer, 512, 1, inptr);
    while(buffer[0] != 0xff &&
    buffer[1] != 0xd8 &&
    buffer[2] != 0xff &&
    (buffer[3] & 0xe0) != 0xe0)
    {
        fread(&buffer, 512, 1, inptr);
    }
    
    fwrite(&buffer, 512, 1, outptr);
    while(fread(&buffer, 512, 1, inptr) == 1)
    {
        
        
        if(buffer[0] == 0xff &&
        buffer[1] == 0xd8 &&
        buffer[2] == 0xff &&
        (buffer[3] & 0xe0) == 0xe0)
        {
            fclose(outptr);
            i ++;
            sprintf(filename, "%03i.jpg",i);
            fopen(filename, "w");
            
            fwrite(&buffer, 1, 512, outptr);
        }
        else
        {
            fwrite(&buffer, 512, 1, outptr);
        }
           
    }
    fclose(outptr);
    fclose(inptr);
    // success
    return 0;
   
}
