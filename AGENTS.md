# Working agreement — The Scribble

This is the canonical repository policy for people and coding agents. Nested `AGENTS.md`
files may add instructions for their directory, but may not weaken this file. When rules
conflict, the closest file controls ordinary implementation detail and this root file controls
security, governance, and authority.

## Project and commands

The Scribble is a handheld, distraction-free voice-to-text capture device built around the Elecrow CrowPanel ESP32-S3 2.13" E-Paper display, an INMP441 I2S digital microphone, a 1027 coin haptic motor, and a 500mAh LiPo battery. This repository contains the mechanical CAD (OpenSCAD/STL), ESP32-S3 firmware, and local Windows USB-C sync tools.

- Install: `python -m pip install -r requirements.txt` (optional tools)
- Run Web Viewer: Open `case_model_viewer.html` in a web browser
- Build STL: Run `node scripts/generate_stl.js` or `openscad -o output/the_scribble.stl hardware/the_scribble_v5_step.scad`
- Test / CI: `bash scripts/ci/project-checks.sh`


## Autonomy and scope

Once the owner approves the outcome, make ordinary implementation decisions and execute them.
For meaningful work, plan once: name the files likely to change, what is out of scope, and the
evidence that will prove completion. Use `SPEC.md` for substantial work; skip that ceremony for
trivial changes.

Stop for a decision that materially changes product scope, cost, privacy/security boundaries,
credentials, production/shared infrastructure, a major architecture or dependency, destructive
or hard-to-reverse state, or these rules and the limits of your authority.

One branch carries one cohesive, shippable deliverable. Include its tests and necessary docs;
defer unrelated cleanup.

## Git and pull requests

1. Branch before changing files; never commit or push directly to the protected default branch.
2. Use Conventional Commits with an imperative subject of at most 72 characters. Keep logical
   commits reviewable and explain why in the body when it is not obvious.
3. Run the smallest relevant checks while working and the complete relevant suite before review.
4. Push completed work to the authoritative remote and any configured mirrors without force.
5. Obtain independent review for normal and high-risk work. A deterministically prose-only change
   is exempt, and so is any repository that sets `review.requireIndependentReview` to `false` in
   `governance-profile.json` — an explicit owner choice for solo or AI-authored work with no
   second human available; the reusable template defaults this to `true`. Review must cover the
   exact code state submitted.
6. Open a pull request with the outcome, test evidence, migration notes, and limitations. Never
   merge red. Never bypass required checks.
7. A change to a governance/control file is a proposal only. An agent may author and submit it,
   but only the human owner may ratify or merge it.

No remote means commit locally and report what could not be pushed or reviewed remotely.

## Engineering rules

Build the smallest complete solution: prefer no change, an existing capability, the platform or
standard library, an installed dependency, then small new code. Add a dependency only with a
one-line reason. Do not trade away correctness, security, accessibility, maintainability, or
explicit requirements for a smaller diff.

- Never put secrets in code, config, history, logs, prompts, test fixtures, or commit messages.
- Never hand-edit generated lockfiles; change the manifest and regenerate them.
- Do not disable or route around hooks, scanners, CI, reviews, or hosting protections.
- Do not rewrite shared history, force-push protected branches, or use administrative bypasses.
- Do not add raw audio playback or uncompressed WAV recording back into scope (design relies on direct Markdown notes).
- Enclosure design must maintain 0.00 mm button overhang on the top edge.
- Acoustic port on the rear shell must align with the INMP441 bottom port and seat a sealing foam gasket ring.

## Review and evidence

Stabilize the branch before independent review. The implementer cannot count a self-review as
independent. Any behavior-changing change after review invalidates it; deterministically
classified prose-only follow-ups may remain exempt. Record the reviewer, verdict, and exact state
reviewed using the repository's configured attestation method.

Completion requires evidence: the command and result, test output, or another observable proof.
Update `WORKLOG.md` only when work materially advances or leaves context another session needs;
do not add filler or make a commit solely for the log.

## Control boundaries

- `AGENTS.md` guides behavior; it is not a security boundary.
- Lefthook and `scripts/hooks/` provide local enforcement for every tool and manual commit.
- `.github/workflows/` and the hosting policy provide independent remote enforcement.
- Agent adapters may add convenience or defense in depth, but do not define core authority.
- If a required control fails or its result cannot be determined safely, stop and report it.

Details, recovery procedures, the control matrix, and platform notes live in `REPO_RULES.md` and
`docs/`. Governance generation: `.governance-version`.
