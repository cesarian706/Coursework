/**
 * Copies a BMP piece by piece, just because.
 */
       
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize number infile outfile\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];
    int n = atoi(argv[1]);

    // open input file 
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 || 
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }
    // determine padding for scanlines new and old
    int padding = (4 - ((bi.biWidth * n) * sizeof(RGBTRIPLE)) % 4) % 4;
    int inpadding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    
    // copy file headers and change for n
    BITMAPFILEHEADER file;
    BITMAPINFOHEADER info;
    memcpy(&file, &bf, sizeof(BITMAPFILEHEADER));
    memcpy(&info, &bi, sizeof(BITMAPINFOHEADER));
    info.biWidth *= n;
    info.biHeight *= n;
    info.biSizeImage = (((sizeof(RGBTRIPLE) * (bi.biWidth * n)) + padding) * abs((bi.biHeight * n)));
    file.bfSize = info.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&file, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&info, sizeof(BITMAPINFOHEADER), 1, outptr);


    // iterate over infile's scanlines
    int height = abs(bi.biHeight);
    for (int i = 0; i < height; i++)
    {
        // repeat each scanline n times
        for (int d = 0; d < n; d++)
        {
            // iterate over pixels in scanline
            for (int j = 0; j < bi.biWidth; j++)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
                // copy each pixel n times
                for (int c = 0; c < n; c++)
                {
                    // write RGB triple to outfile
                fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }
            // add new padding
            for (int k = 0; k < padding; k++)
            {
                fputc(0x00, outptr);
            }
            // return pointer to begining of scanline 
            fseek(inptr, -(bi.biWidth * sizeof(RGBTRIPLE)), SEEK_CUR);
        }
        // move pointer to beginning of new line
        fseek(inptr, ((bi.biWidth * sizeof(RGBTRIPLE)) + inpadding), SEEK_CUR);

    }
    
    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
