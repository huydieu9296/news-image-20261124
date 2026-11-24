# Test results — news-image-20261124 (24 Nov 2026, 07:2x VN)

Built in this recorded session (fresh subagent session for this task):
- `draw_news.py` — draws the 1024x1024 front page (PIL, DejaVu, no network)
- `main.py` — stdlib-only validator + byte-copy to $MAKEFUN_OUTPUT_DIR
- `entry.png` — 132,312 bytes, sha256
  e0aa51bf890f73e8650ebff94b8c01933885d9468350c5e6a0d4c19497560544
- `README.md`, `LICENSE` (MIT), prompt file at
  `~/workspace/makefun/news-image-20261124-prompt.txt`

Checks (run 24 Nov 2026 ~07:27 VN):
- [x] main.py run 1 → ok, 1024x1024, 132312 bytes
- [x] main.py run 2 → identical sha256 (byte-identical) — PASS
- [x] entry.png ≤ 1 MiB (132,312 / 1,048,576) — PASS
- [x] entry.png exactly 1024x1024 — PASS
- [x] draw_news.py re-run → same sha256 (deterministic build) — PASS
- [x] Visual check: 6 cards, no text overflow, all headlines/decks legible

NOT submitted — submit must run from the main session (subagent cannot
submit). Remaining steps for the main session:
1. Create public repo huydieu9296/news-image-20261124 (after bounty opened),
   push these files (MIT LICENSE).
2. Submit with --prompt-file ~/workspace/makefun/news-image-20261124-prompt.txt
   (+ --mcp --harness-version --provider --effort, and --parent-session if
   the builder session opened from a hand-off).
3. Deadline: 00:00 UTC Thu 26/11/2026 = 07:00 VN 26/11.
