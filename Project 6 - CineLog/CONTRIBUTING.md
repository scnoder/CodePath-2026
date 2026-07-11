# Contributing to CineLog

Thanks for contributing! Before you submit a PR, please read this guide. Maintainers will check for these conventions during review.

---

## Commit Format

CineLog uses **Conventional Commits**. Every commit message must begin with a type prefix:

| Prefix | When to use |
|--------|-------------|
| `feat:` | A new feature or endpoint |
| `fix:` | A bug fix |
| `test:` | Adding or updating tests |
| `docs:` | Documentation changes only |
| `refactor:` | Code restructuring with no behavior change |
| `chore:` | Maintenance tasks (deps, config, etc.) |

**Format:**
```
<type>: <short description in imperative mood>
```

**Good examples:**
```
feat: add director filter to film search endpoint
fix: return 404 when user not found in collection endpoint
test: add test for get_collection sort order
docs: update README with local setup instructions
refactor: extract pagination logic into shared utility
```

**Not acceptable:**
```
added watchlist
fixed a bug
more changes
WIP
```

---

## One Logical Change Per Commit

Each commit should represent one coherent unit of work. If you fixed a bug *and* added a test for it, those are two commits — not one.

If your branch history is messy, clean it up with `git rebase -i` before submitting.

---

## No Merge Commits

Do not merge `main` into your feature branch. Use `git rebase origin/main` instead. The PR branch must have a linear history with no merge commits.

---

## Naming Conventions

Service functions follow a `verb_to_noun` pattern. Compare existing functions before adding new ones:

- `add_to_collection()` ✓
- `remove_from_collection()` ✓
- `get_collection()` ✓

New functions should follow the same pattern.

---

## PR Description

Every PR must include:
- What the feature does (plain language, 2–3 sentences)
- Any design decisions made (especially around defaults or behavior choices)
- How to manually test the feature end to end

---

## Tests

If you're adding a new service function, include at least:
1. A test for the happy path
2. A test for duplicate/conflict handling
3. A test for a nonexistent ID

See `tests/test_collection.py` for the expected pattern.
