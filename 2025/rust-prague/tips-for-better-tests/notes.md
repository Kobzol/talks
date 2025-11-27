# Intro
- whoami

## Tests
- tests, do you love tests? I love tests
    - green test result satisfaction
    - flaky tests joke
    - love/hate relationship
- why are tests annoying?
  - stress => red test means a problem
  - changing/maintaining tests is annoying
  - understanding tests is annoying

- make tests visual with (nano-)DSLs
  - easier to understand
  - blessable
- tests as data
  - blessable tests

- test behavior, not implementation
  - sometimes, implementation *is* behavior

- why split tests based on categories
  - how often a test breaks, how flaky it is, how fast it is
  - compare testing pyramids

- snapshot tests for everything
    - image tests 
    - easy to upgrade, blessable
      - code review to test the blessed changes
    - visual understanding
- code changes should not require test changes
- integration tests
    - database
    - HTTP mocking
    - don't mock dependencies, makes code too complicated
- ultimate solution: TigerBeetle

- VecDeque, IntelliJ Rust, hyperqueue, bors, rustc
    - bors SQL parser tests, migration test
    - bors: pragmatic, didn't test it as a binary
- ideally, no tests are the best => compile-time tests => type system
- use test markers, asynchronous tests, control concurrency
    - error propagation in asynchronous tests!
    - loom, tokio <something>, OS system used by TigerBeetle
- don't use mocks too much
    - show tests from Jersy's Kelvin PR
    - this entire test suite must be purged

- proptest, fuzzing
- test coverage => wtf
- throw away unit tests
- unit testing => for code with no dependencies
- no rocket science rule (bors/merge queue)
  - Rust Log Analyzer

- write blog post
