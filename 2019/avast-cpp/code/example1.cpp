#include <random>
#include <algorithm>
#include <benchmark/benchmark.h>

using Type = int;

std::vector<Type> create_data(size_t size)
{
    std::default_random_engine rng(0);
    std::uniform_int_distribution<int> dist(1, 10);

    std::vector<Type> data(size);
    std::generate(std::begin(data), std::end(data), [&dist, &rng]() {
        return dist(rng);
    });

    return data;
}

void filter_loop(const std::vector<Type>& data, benchmark::State& state)
{
    Type sum = 0;
    for (auto _ : state)
    {
        for (auto x : data)
        {
            if (x < 6)
            {
                sum += x;
            }
        }
    }
    benchmark::DoNotOptimize(sum);
}

static void filter_nosort(benchmark::State& state)
{
    auto size = static_cast<size_t>(state.range(0));
    auto data = create_data(size);

    filter_loop(data, state);
}

static void filter_sorted(benchmark::State& state)
{
    auto size = static_cast<size_t>(state.range(0));
    auto data = create_data(size);

    std::sort(data.begin(), data.end());

    filter_loop(data, state);
}

#define BENCH(Fn) BENCHMARK(Fn)->Range(32768, 32768)
BENCH(filter_nosort);
BENCH(filter_sorted);

BENCHMARK_MAIN();
