Did you ever wonder what has to happen for a new version of the Rust compiler gets to Rustaceans? I’ll show you!

We will follow the journey of a single Rust commit, from its pull request, through the compiler build system, continuous integration workflows, our myriad of tests, the PGO and BOLT optimization pipeline, to packaging an archive and making a release that can then finally be downloaded by Rust users through rustup. I will also describe various pieces of tooling and bots that help us automate this process to make it as smooth as possible.

# Story
- having an idea
  - RFC
  - rfcbot
  - FCP, concerns
- implementing the change
  - rustc-dev-guide
  - git clone
    - submodules, subtrees, Josh, josh-sync
  - building the compiler
    - bootstrap
    - set of Makefiles -> Python + Rust
    - x.py
    - x setup
    - bootstrapping diagram
  - running tests
    - compiletest
    - test suites (codegen, miropt, incremental, UI, run-make, etc.)
    - tidy
- open a PR
- triagebot
  - greeting
  - assignment
  - review rotation and preferences
  - label system
  - shortcuts, review links, all comments viewer
  - CI dashboard?
  - integration with Zulip
- rustc-perf
- crater
    - cargo build (+ open source) enables crater
    - enables things like the new trait solver or the never type stabilization
    - triaging
- bors
  - merge queue
  - try builds, delegation
  - rollups
  - problems with homu
  - bors rewritten from Python to Rust, weekend project
- merge
  - r+
  - team database
  - GitHub issues
  - thanks
- CI
  - duration, cost
  - bash, Python, Rust
  - test vs dist runners
  - tiers, targets and architectures
  - complex configuration
  - Docker reuse of images with Rustup
  - PGOLTOBOLTWTFBBQ pipeline
    - rewritten from shell to Python, then to Rust
- commit -> build archive -> store on S3
- nightly build
  - beta/stable bump
- rustup
  - manifest
  - extraction into a sysroot, mapping to bootstrap components
  - concurrent download
- release
  - compression of release archives
  - bandwidth of downloaded archives
  - exponential growth
  - future: CDN, caching, mirroring, our own GitHub Action for setting up Rust?
  - every build is a release

- rfcbot (?)
- triagebot
- bors
- commit -> archive (multiple commits, PRs, rollups)
- compression of release archives
- Docker reuse with rustup
- PGOLTOBOLTWTFBQQ pipeline
- bootstrapping process
- bandwidth of downloaded archives
- CI testing
  - test vs dist runners
- bors rewritten from Python to Rust
  - homu "lockfile"
- PGO rewritten from shell to Python, then to Rust
- cargo build (+ open source) enables crater
  - crater enables things like the new trait solver
- infrastructure map (help from Ada? :) )

- https://www.youtube.com/watch?v=luBJvcGg9HQ


# Intro
- screenshot of TechMeetup 2023 Rust talk
- whoami
- governance, maintenance & development, deployment of Rust

## Governance
- what is governance
- forms of language government
  - company-backed (Kotlin/C#/TypeScript?)
  - design by committee (C/C++/Javascript)
  - BDFL (Ruby/Zig/ex-Python)
  - Open RFC process (Rust/PHP/Python - steering council)
- Rust governance history
  - Graydon BDFL
  - core team
  - RFC process, teams
  - Rust Foundation
- structure of the Project
  - people of the Rust Project
  - team structure
  - Rust Foundation (legal entity, bank account, infrastructure, domain ownership, sponsorship)
- team database
- how to change Rust?
  - small change => PR
  - large/language change => RFC
- making decisions
  - consensus
  - FCP
  - invest most time => make decisions?

- handling conflict
  - great int debate, no new rationale
    - await, not follow the results of the survey
  - trademark drama, mod team resignation, RustConf drama
  - transparency
  - CrabLang
  - code of conduct
  - people care a lot about Rust, it feels improbable
  - slide with all the dramas

- thanks.rust-lang.org

- communication
  - OSS is communication, screenshot of my GitHub profile
  - mailing lists => not inclusive (Linux)
  - IRC
  - Zulip (publicly accessible), Discord, GitHub
  - asynchronous communication, different time-zones
  - who gets to decide what gets done? Project Goals

- RFCs
  - can be submitted by anyone!

- teams
  - stats
  - team database
  - invite people early (show my invitation into wg-compiler-perf and t-infra), avoid gatekeeping
  - teams are autonomous and independent

- complex distributed system
  - asynchronous
  - no one tells people what to work on

## Maintenance
- OSS
  - screwdriver
  - curl list of things that form maintenance
- show rust-lang/rust and other repositories, issue/PR counts
- bots
  - triagebot => welcome contributors
  - bors => delegate r+

- onboarding, developing both external and internal documentation
  - The Rust Programming Language book
  - rustc-dev-guide
- contributor stats from GitHub

## Deployment
- new release every six weeks
  - release train, avoid stress
  - breaking changes
  - crater
  - edition model

## How can you contribute to your language
- GSoC
- nerd-sniping
- summarize the current state
- post an issue
- write a blog post
- send a PR (if possible)

- consider sponsoring OSS developers
  - thanks.dev
  - GitHub Sponsors

## Materials
- https://www.youtube.com/watch?v=d9_ymbFnzM4
- https://docs.google.com/presentation/d/12xeMuDvFiiSD3fdxS-Xp0Bqfa81tU9qIQtVxBQuGNkg/edit?slide=id.p#slide=id.p
- https://www.youtube.com/watch?v=EMKCp7Oel5M
- https://www.youtube.com/watch?v=IwPRu5FhfIQ
- https://www.youtube.com/watch?v=edczUK1v7nM
