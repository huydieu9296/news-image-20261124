# The World in One Day — 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/huydieu9296/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/huydieu9296/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A newspaper front page that sums up Tuesday 24 November 2026 in a
single image. Six verified stories from the day — Nvidia reinstating
Jensen Huang as CEO and its shares jumping 31% after Trump
intervened, Russian strikes killing at least 14 in Ukraine's Kyiv
region as Zelenskyy calls for four-way talks, the Indonesian
candy-factory fire toll rising to 24 with about 30 still missing,
Oregon and Virginia suing Musk's firms over nonconsensual sexualised
images made with the Grok chatbot, Rep. Jimmy Gomez resigning after
the Ethics panel found evidence of sexual misconduct, and storms and
airline glitches threatening messy Thanksgiving travel — laid out as
a classic broadsheet: navy masthead, red rule, and six story blocks
with a coloured side bar, a hand-drawn icon, a kicker, a headline
and a two-line deck.

## The six stories

1. **Tech · USA — Huang is back, Nvidia soars 31%.** Nvidia
   reinstates Jensen Huang as CEO after Trump intervenes; shares
   jump a third, Nasdaq rallies 6.5%, nearly $1 trillion added in a
   day. Sources: Reuters, CNN, SCMP (24 Nov).
2. **War · Ukraine — Kyiv strikes kill 14; Zelensky seeks talks.**
   Russian strikes hit a Kyiv-region flat block and a store;
   Zelenskyy calls for four-way talks as soon as possible and urges
   the US to release paid-for Patriot missiles. Sources: Associated
   Press / AFP, Al Jazeera, The Guardian (24 Nov).
3. **Disaster · Indonesia — Factory fire toll rises to 24.** A
   candy-factory fire near Jakarta kills 24; about 30 still missing
   as rescuers search the unstable wreckage. Sources: Reuters, AFP
   (24 Nov).
4. **Tech · AI — States sue Musk firms over Grok images.** Oregon
   and Virginia sue over nonconsensual sexualised images of real
   people made with the Grok chatbot. Sources: Associated Press,
   WCBE (24 Nov).
5. **Politics · USA — Congressman Gomez to quit over ethics probe.**
   Rep. Jimmy Gomez resigns effective 1 December after the Ethics
   panel finds evidence of sexual misconduct. Sources: Associated
   Press (24 Nov).
6. **Weather · USA — Storms threaten messy Thanksgiving travel.**
   Storms and airline glitches threaten holiday travel as millions
   head home for Thanksgiving. Sources: Associated Press (24 Nov).

## Run

```sh
python3 draw_news.py   # builds entry.png (1024x1024, under 1 MiB)
python3 main.py        # validates entry.png and copies it to $MAKEFUN_OUTPUT_DIR
```

`main.py` uses only the Python standard library. It checks the PNG
magic bytes, the 1 MiB size limit and the 1024x1024 dimensions,
copies the file byte for byte, then reads the copy back to confirm
it is identical. `MAKEFUN_OUTPUT_DIR` defaults to `/output`.

The picture is fully deterministic: fixed layout, fixed DejaVu
fonts, no randomness, no timestamps and no network access. Two runs
of `main.py` write byte-identical files.
