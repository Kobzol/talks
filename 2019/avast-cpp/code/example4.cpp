#include <iostream>
#include <vector>
#include <immintrin.h>

#define SIZE 4 * 1024 * 1024

using Type = float;

int main(int argc, char** argv)
{
    Type F = static_cast<Type>(std::stof(argv[1]));

    std::vector<Type> data(SIZE, 1);

    _mm_setcsr(_mm_getcsr() | 0x8040);

    for (int r = 0; r < 100; r++)
    {
        for (int i = 0; i < SIZE; i++)
        {
            data[i] *= F;
        }
    }

    return 0;
}
