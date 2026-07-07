---
title: Code
category: Research Workflow
order: 5
summary: Version control, coding style, documentation, and dependency management.
keywords: [coding, software, programming, git, version control, python, R, repository, github]
icon: "💻"
reviewed: 2026-07-05
---

<aside class="marginnote" markdown="1">
**Lab-specific software.** Getting-started guides for **FlightStream** (our CFD tool) and our **reinforcement-learning stack** are in the [member portal]({{ '/portal/' | relative_url }}).
</aside>

Good software practices make research reproducible, collaborative, and easier to
maintain. As the lab evolves, so will these recommendations.

## Version control

Every project should have its own repository in the
[UC-BIRD-Lab GitHub organization](https://github.com/UC-BIRD-Lab).

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

**Starting a project.** Create the repository in the UC-BIRD-Lab organization
(for shared work), name it per the conventions below, set permissions, and clone
it from your IDE (PyCharm: *Get from VCS*; RStudio: *File → New Project → Version
Control → Git*). A Python and an R project can share one repository. First-time
Git setup (installing Git and setting your username and email) is in the
[graduate student start guide]({{ '/lab-guide/graduate-students/' | relative_url }}).

## Repository organization

Each repository should correspond to a single research project. Repository names should be descriptive, lowercase, and use hyphens between words. Examples include:

✔ `birdlike-airfoil-optimization`

✔ `avian-pressure-sensing`

✘ `Project1`

✘ `myRepository`

## Documentation

Code is read far more often than it is written.

Write comments that explain **why** something exists, not simply **what** the code
is doing.

Whenever implementing new methods:

- document assumptions
- record the origin of equations
- cite relevant publications
- explain important design decisions

If a function cannot be summarized in a few sentences, consider simplifying it.

<div class="callout" markdown="1">

**Plan for publication.**

Repositories start private. Most become public when the associated paper is published, released under an open-source license so others can reuse the work. Organize your code from the start as though another researcher will eventually explore it. Clear repository structure, meaningful commit messages, and thoughtful documentation are much easier to maintain than to reconstruct at the end of a project.
</div>

## Style

Consistent formatting makes code easier to read and review.

For Python we recommend following
[PEP 8](https://peps.python.org/pep-0008/).

Use an automatic formatter/linter whenever possible. We recommend
[`ruff`](https://docs.astral.sh/ruff/) because it is fast, consistent, and
combines formatting, linting, and import organization into a single tool.

## Dependency management (Python)

<div class="callout" markdown="1">
**Recommendation:** use [`uv`](https://docs.astral.sh/uv/) for new Python projects.
</div>

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

Any of these approaches are acceptable, but we recommend **uv** for most projects.

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
