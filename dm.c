/*
 * Binary dumper.
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define Step 16

#define Red    "\033[0;31m"
#define Green  "\033[0;32m"
#define Normal "\033[00m"

static int fColor_ = 0;
static int fBinary_ = 0;

static void
color (
  char * psz,
  const char * pszColor ) {
    if (fColor_) {
        strcat(psz, pszColor);
    }
}

int
main (
  int argc,
  char * * argv ) {
  FILE * pfile;
  unsigned char ac[Step];
  unsigned char * psz;
  int iOffset;
  int nRead;
  int i;
  int nBufSize;
    nBufSize = Step * (strlen(Red) + 1) + strlen(Normal) + 1;
    psz = (unsigned char *) malloc(sizeof (unsigned char) * nBufSize);
    for (i = 1; i < argc; i ++) {
        if        (strcmp(argv[i], "-c") == 0) {
            fColor_ = 1;
        } else if (strcmp(argv[i], "-b") == 0) {
            fBinary_ = 1;
            fColor_ = 1;
        } else {
            break;
        }
    }
    if (i < argc) {
        if ((pfile = fopen(argv[i], "r")) == (void *) 0) {
            fprintf(stderr, "Error: Failed to open \"%s\"\n", argv[i]);
            exit (1);
        }
    } else {
        pfile = stdin;
    }
    for (
     iOffset = 0;
     nRead = fread(ac, sizeof (unsigned char), Step, pfile);
     iOffset += Step ) {
        memset(psz, 0, nBufSize);
        printf("%08X |", iOffset);
        for (i = 0; i < Step; i ++) {
            if (i < nRead) {
                printf(" %02X", ac[i]);
                if        (ac[i] < 0x20 || ac[i] == 0x7F) {
                    color(psz, Green);
                    psz[strlen(psz)] = '.';
                } else if (0x80 <= ac[i]) {
                    if (fBinary_) {
                        color(psz, Green);
                    } else {
                        color(psz, Red);
                    }
                    psz[strlen(psz)] = '.';
                } else {
                    color(psz, Normal);
                    psz[strlen(psz)] = ac[i];
                }
            } else {
                printf("   ");
            }
        }
        color(psz, Normal);
        printf(" | %s\n", psz);
    }
    if (pfile != stdin) {
        fclose(pfile);
    }
    free((void *) psz);
    return (0);
}
