# GitHub repository topics — 104 public repositories

The blue pills shown under **sustainablefarming** are GitHub **repository topics**, not issue labels or Markdown badges.

This directory proposes topic sets for each of the 104 public repositories from the 20 October 2026 account inventory. All names are unique lower-case topic slugs. **Review the proposed topics before applying:** some were inferred from repository names and have not been validated against full source trees. Do not mistake provisional topic labels for implemented features.

## How to apply

1. On a computer with Python 3 and [GitHub CLI](https://cli.github.com/), run `gh auth login` using the account that owns these repositories. Grant the necessary repository administration/metadata permissions for editing topics.
2. Clone or download the `1stsimplifycode` profile repository.
3. Review and edit `docs/repository-topics/proposed-topics.json`.
4. Preview one repository: `python docs/repository-topics/apply_topics.py --repo CamSketch`.
5. Apply one: `python docs/repository-topics/apply_topics.py --repo CamSketch --apply`.
6. Preview all: `python docs/repository-topics/apply_topics.py`.
7. Apply all after approval: `python docs/repository-topics/apply_topics.py --apply`.

**Safety:** No file deletion or privacy change. Default is dry-run. The script reads existing topics, merges additions without removing existing ones, and refuses over-20-topic updates. Public repositories only. GitHub topic changes need repository permissions that the ChatGPT GitHub connection does not expose.

The list is intentionally repository-specific. Avoid adding unsupported technology claims, marketing tags, or misleading badges. Topics remain in GitHub's **About → Topics** UI, not only in the README.
