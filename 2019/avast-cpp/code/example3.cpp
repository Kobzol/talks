#include <thread>
#include <vector>
#include <cstring>

#define REPETITIONS 1200 * 1024 * 1024UL

void thread_fn(int tid, int64_t* data, int count)
{
    for (size_t i = 0; i < REPETITIONS; i++)
    {
        for (int c = 0; c < count; c++)
        {
            data[tid * 8 + count]++;
        }
    }
}

int main(int argc, char** argv)
{
    auto thread_count = static_cast<size_t>(std::stoi(argv[1]));

    auto data = std::make_unique<int64_t[]>(512);

    std::vector<std::thread> threads;
    for (int i = 0; i < thread_count; i++)
    {
        threads.emplace_back(thread_fn, i, data.get(), 1);
    }

    for (auto& thread : threads)
    {
        thread.join();
    }

    return 0;
}
