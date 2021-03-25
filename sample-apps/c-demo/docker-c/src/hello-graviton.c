#include <stdio.h>
#include <stdlib.h>

#ifndef ARCH
#define ARCH "Undefined"
#endif

int main()
{
    printf("\n === DevDay === \n\n");
    printf("Hello, architecture from uname is %s\n", ARCH);

    switch (sizeof(void *))
    {
        case 4:
            printf("32-bit userspace\n\n");
            break;
        case 8:
            printf("64-bit userspace\n\n");
            break;
        default:
            printf("unknown userspace\n\n");
    }
    exit(0);
}