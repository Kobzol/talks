#include <memory>
#include <immintrin.h>

#define SIZE 64 * 1024 * 1024

int main()
{
    auto data = std::make_unique<size_t[]>(SIZE);

    for (int j = 0; j < 100; j++)
    {
#pragma omp parallel for
        for (size_t i = 0; i < SIZE; i++)
        {
            data[i] = i;
//            _mm_stream_si64((long long int*) data.get() + i, i);
        }
    }

    return 0;
}
