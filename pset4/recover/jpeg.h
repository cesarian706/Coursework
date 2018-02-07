#include <stdint.h>
typedef uint8_t  BYTE;

typedef struct
{
    BYTE one;
    BYTE two;
    BYTE three;
    BYTE four;
} __attribute__((__packed__))
PATTERN;