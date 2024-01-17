# What is governance?
- being able to make (both important and unimportant) decisions, in a distributed fashion, quickly
- be transparent and inclusive
- OSS vs company vs BDFL vs committee
- decision-making process on how to evolve something

# History
- 2006
  - Graydon Hoare created Rust
  - open-source from start
- 2009
  - Mozilla starts sponsoring it
  - Patrick Walton, Niko Matsakis
  - people from this time still working on Rust (IRC -> Zulip)
- 2010 - 2012
  - Graydon BDFL
- 2012 - 2014
  - Graydon steps down
  - core team is created
- March 2014
  - RFC process begins, inspired by Python's PEP
  - RFC #1: private fields (https://rust-lang.github.io/rfcs/0001-private-fields.html)
  - RFC #2: RFC process (https://rust-lang.github.io/rfcs/0002-rfc-process.html)
- 2015
  - RFC 1068 (https://rust-lang.github.io/rfcs/1068-rust-governance.html) introduced teams
- 2020
  - Mozilla layoffs
  - Rust Foundation plans by core team
- 2021
  - February: Rust Foundation created (Mozilla, AWS, Huawei, Google, Microsoft)
  - November: moderation team resigns
- 2022
  - May: governance update
- 2023
  - April: Trademark policy
  - Leadership council

# Governance diagram
- https://www.rust-lang.org/governance
- council
- Foundation
  - legal
  - documents
  - financials
  - trademark
- drama
- unanimous decisions
- if you want something done, do it

- Forge (https://forge.rust-lang.org/)

- https://forge.rust-lang.org/governance/council.html
- moderation (https://forge.rust-lang.org/governance/moderation.html)

# Teams
- nine top-level teams
- representatives => leadership council
- project directors
- managed by automation (https://github.com/rust-lang/team)
- bors rights (quite open, I can merge rust-lang/rust PRs)
- Zulip (https://rust-lang.zulipchat.com)

# RFC process (how do decisions happen?)
- RFCs
  - pre-RFC
  - shepherd (member of a team)
  - open comments period
  - FCP
  - voting
  - decision
  - merge/close
  - implementation
- ACP (API change proposal)
- [MCP](https://forge.rust-lang.org/compiler/mcp.html) (Major change proposal)
- Cargo FCP
- every design or implementation choice carries a trade-off and numerous costs. There is seldom a right answer.
- "no new rationale" rule
  - never introduce new arguments during decision/FCP

1. Create RFC
2. Receive feedback
3. Modify RFC
4. If no consensus, goto 2.
5. FCP
6. Merge

- consensus within the subteam
- if no consensus => leader decides, should consult with the core team

# Handling conflict/drama
- https://graydon2.dreamwidth.org/307105.html
- unresolved conflict => one party leaves
- burnout
- people who do the work get to decide (unfair?)
  - attend every city meeting to push your goal
- Graydon's suggestion: hire professionals
- transparency

# How to get something done?
- poke people
- do it!

# How to get involved?
- observe, lurk, do stuff, talk with people
- how I joined wg-compiler-performance and the infra team?

# Sources
- https://chrisholdgraf.com/blog/2018/rust_governance/index.html
- https://blog.rust-lang.org/2023/06/20/introducing-leadership-council.html
- https://users.rust-lang.org/t/why-is-there-so-much-mismanagement-in-the-rust-foundation-and-core-team/94822
- https://blog.rust-lang.org/inside-rust/2022/10/06/governance-update.html
- https://hackmd.io/@XAMPPRocky/r1HT-Z6_t
- https://blog.rust-lang.org/2023/05/29/RustConf.html
- https://www.theregister.com/2023/04/17/rust_foundation_apologizes_trademark_policy
- https://www.theregister.com/2021/11/23/rust_moderation_team_quits
- https://fasterthanli.me/articles/the-rustconf-keynote-fiasco-explained
- https://www.jntrnr.com/why-i-left-rust/
- https://fasterthanli.me/articles/rust-the-wrong-people-are-resigning
- https://www.technologyreview.com/2023/02/14/1067869/rust-worlds-fastest-growing-programming-language/
- https://brson.github.io/2022/02/09/rust-core-team-alumni
- https://graydon2.dreamwidth.org/307105.html
- https://www.youtube.com/watch?v=79PSagCD_AY
- https://rustacean-station.org/episode/042-ben-striegel/
