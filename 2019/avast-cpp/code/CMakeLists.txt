cmake_minimum_required(VERSION 2.8)
project(avast)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread -fopenmp")

include(ExternalProject)

set(BENCHMARK_ROOT ${CMAKE_CURRENT_BINARY_DIR}/benchmark)

# download Google benchmark
ExternalProject_Add(gbenchmark
        PREFIX ${BENCHMARK_ROOT}
        GIT_REPOSITORY https://github.com/google/benchmark
        GIT_TAG master
        CMAKE_ARGS -DBENCHMARK_ENABLE_GTEST_TESTS=OFF -DCMAKE_BUILD_TYPE=Release
        INSTALL_COMMAND ""
        UPDATE_COMMAND ""
)
include_directories(${BENCHMARK_ROOT}/src/gbenchmark/include)
link_directories(${BENCHMARK_ROOT}/src/gbenchmark-build/src)

link_libraries(benchmark)

add_executable(example1 example1.cpp)
add_dependencies(example1 gbenchmark)

add_executable(example2 example2.cpp)
add_dependencies(example2 gbenchmark)

add_executable(example3 example3.cpp)
add_executable(example4 example4.cpp)
add_executable(example5 example5.cpp)
