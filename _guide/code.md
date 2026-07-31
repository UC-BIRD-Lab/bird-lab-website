---
title: Code
category: Research Workflow
order: 5
summary: Version control, coding style, documentation, and dependency management.
description: "How we use GitHub, what we expect of documentation and style, and how to keep dependencies from breaking later."
keywords: [coding, software, programming, git, version control, python, R, repository, github]
icon: "💻"
reviewed: 2026-07-05
---

<aside class="marginnote" markdown="1">
**Lab-specific software.** Additional getting-started guides for some software and tools are in the [member portal]({{ '/portal/' | relative_url }}).
</aside>

Good software practices make research reproducible, collaborative, and easier to
maintain. As the lab evolves, so will these recommendations. Tools are named as
practical suggestions, not endorsements; equivalent alternatives are fine, and any
tool that stores lab data must follow UC Davis data-security guidance.

## Github Repositories (Mandatory)

Every project with code must have its own repository in the
[UC-BIRD-Lab GitHub organization](https://github.com/UC-BIRD-Lab).
When starting, create the repository in the UC-BIRD-Lab organization
(for shared work). Repository names should be descriptive, lowercase, and use hyphens between words. Examples include:

✔ `birdlike-airfoil-optimization`

✔ `avian-pressure-sensing`

✘ `Project1`

✘ `myRepository`

Note that a project that uses Python and R code can share one repository. Refer to [graduate student start guide]({{ '/lab-guide/graduate-students/' | relative_url }}) for first-time
Git setup.

## Version Control Tips/Tricks

We recommend:

- Work on feature branches rather than directly on `main`.
- Keep `main` stable and deployable.
- Push your work regularly (at least daily).
- Make small, logical commits with descriptive messages.

A repository should tell the story of a project. Someone unfamiliar with your work
should be able to understand what changed simply by reading the commit history.

<div class="callout" markdown="1">
**Good commit messages describe a logical change, not simply that files changed.**

✔ `Add pressure calibration routine`

✔ `Fix tail force sign convention in stability analysis`

✘ `Updates`

✘ `Fixed stuff`
</div>

## Documentation

Code is read far more often than it is written.

Write comments that explain **why** something exists, not simply **what** the code is doing.

Whenever implementing new methods:
- document assumptions
- record the origin of equations
- cite relevant publications
- explain important design decisions

If a function cannot be summarized in a few sentences, consider simplifying it.

<div class="callout" markdown="1">

**Plan for publication.**

Our GitHub repositories start private. Most become public when the associated paper is published, released under an open-source license so others can reuse the work. Organize your code from the start as though another researcher will eventually explore it. Clear repository structure, meaningful commit messages, and thoughtful documentation are much easier to maintain than to reconstruct at the end of a project.
</div>

## Reusing validated code

Analysis code is usually written once per project and then rebuilt for the next one. 
This can lead to duplication of effort and introduction of minor typos or errors.
Instead, we are working to keep common functions (experimental collection, uncertainty propagation, etc.) in a documented, tested GitHub repo that we build on as a team.

Suggestions/Recommedations:
- **Paths.** Do not hardcode absolute paths such as `setwd("/Users/.../Data")` or
  `"ENTERYOURDIRECTORYHERE"`. Use paths relative to the project root (`here::here()` in R,
  `pathlib` in Python) so the code runs on any machine.
- **Constants.** Comments required for any hard-coded numbers that includes their units and source. 
- **Duplication.** Do not copy-paste blocks, instead you should use a loop or function. 
- **Scratch versus shipped.** Keep troubleshooting scripts separate from the code that produces
  published numbers. A scratch file with its real loop commented out and open questions in the
  comments is a fine notebook, but ensure that only your validated pieces make it into the paper's repo.
- **Cite sources in the code.** Put the equation number and the paper DOI next to the code that
  implements it, so that the next person doesn't have to hunt down where the equation came from.

## Style

Consistent formatting makes code easier to read and review.

For Python we recommend following
[PEP 8](https://peps.python.org/pep-0008/).

Use an automatic formatter/linter whenever possible. We recommend
[`ruff`](https://docs.astral.sh/ruff/) because it is fast, consistent, and
combines formatting, linting, and import organization into a single tool.

## Dependency management (Python)

Python projects rely on many external libraries. Rather than installing packages
globally, use a project-specific environment.

Common options include:

| Tool | Notes |
|------|------|
| **uv** | Recommended for nearly all projects. Fast, modern, and manages environments and packages together. |
| **pip + venv** | Native Python solution; reliable and widely supported. |
| **conda** | Popular in scientific computing and non-Python workflows. |
| **poetry** | Powerful dependency management, though often more complex than necessary. |
| **pdm** | Stores virtual environments within the project directory. |

Any of these approaches are acceptable, but we recommend uv for most projects.

## Resources

**Git & GitHub**

- [Git Book](https://git-scm.com/book/en/v2)
- [About Version Control](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control)
- [Install Git (macOS)](https://macpaw.com/how-to/install-git-mac)

**Tutorials**

- [15-minute Git command-line tutorial](https://youtu.be/USjZcfj8yxE)
- [Git with VS Code](https://youtu.be/HkdAHXoRtos)
- [Official VS Code Git tutorial](https://youtu.be/i_23KUAEtUM)

**Python**

- [PEP 8](https://peps.python.org/pep-0008/)
- [Ruff documentation](https://docs.astral.sh/ruff/)
- [uv documentation](https://docs.astral.sh/uv/)
