#include <random>
#include <memory>
#include <benchmark/benchmark.h>

struct A
{
    virtual ~A() = default;
    virtual int id() const = 0;
    virtual void handle(size_t* data) const = 0;
};

struct B: public A
{
    int id() const override { return 1; }
    void handle(size_t* data) const override { *data += 1; }
};

struct C: public A
{
    int id() const override { return 2; }
    void handle(size_t* data) const override { *data += 2; }
};

std::vector<std::unique_ptr<A>> create_data(size_t size)
{
    std::default_random_engine rng(0);
    std::uniform_int_distribution<int> dist(0, 1);

    std::vector<std::unique_ptr<A>> data(size);
    std::generate(std::begin(data), std::end(data), [&dist, &rng]() -> std::unique_ptr<A> {
        if (dist(rng)) return std::make_unique<B>();
        return std::make_unique<C>();
    });

    return data;
}

void handle_loop(const std::vector<std::unique_ptr<A>> &data, benchmark::State &state)
{
    for (auto _ : state)
    {
        size_t sum = 0;
        for (auto& x : data)
        {
            x->handle(&sum);
        }
        benchmark::DoNotOptimize(sum);
    }
}

static void handle_nosort(benchmark::State& state)
{
    auto size = static_cast<size_t>(state.range(0));
    auto data = create_data(size);

    handle_loop(data, state);
}
static void handle_sorted(benchmark::State& state)
{
    auto size = static_cast<size_t>(state.range(0));
    auto data = create_data(size);

    std::sort(data.begin(), data.end(), [](const std::unique_ptr<A>& lhs, const std::unique_ptr<A>& rhs) {
        return lhs->id() < rhs->id();
    });

    handle_loop(data, state);
}

#define BENCH(Fn) BENCHMARK(Fn)->Range(2 * 1024 * 1024, 2 * 1024 * 1024)
BENCH(handle_nosort);
BENCH(handle_sorted);

BENCHMARK_MAIN();
