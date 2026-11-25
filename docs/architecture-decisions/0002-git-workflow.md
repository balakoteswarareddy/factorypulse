# ADR-0002: Git Workflow

**Date:** 2026-11-24  
**Status:** Accepted

## Decision

I chose trunk-based development because it works well with CI automation and is simpler to manage than GitFlow, which involves multiple long-lived branches.

Since I am the only contributor, maintaining multiple long-lived branches would add unnecessary complexity.

## Branch protection

I configured branch protection on main to prevent accidental direct pushes and make pull requests mandatory. This will also allow me to enforce automated CI checks before merging changes.

## Merge strategy

I chose squash merging to maintain a clean commit history on main without including every intermediate development commit.

## Pull request approvals

I configured zero mandatory approvals because I am currently the only contributor and cannot approve my own pull requests.

## Trade-offs

Squash merging does not preserve individual feature branch commits in the main branch history.

There is currently no independent code review. If more contributors join the project, I will introduce mandatory human approvals.