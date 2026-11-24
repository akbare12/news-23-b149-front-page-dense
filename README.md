# THE WORLD TODAY — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b149-front-page-dense/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b149-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image summing up 23 November 2026's world news: the AI rout that hit Asia
(Kospi −3.3%), the UN chief's call to regulate AI before it's too late, and the
US lead over China at a record low — plus 28 more stories, a number strip, a
world map with numbered pins, and a DATE CHECK box that keeps out stories from
other days.

## How it is built

- `draw.py` draws `entry.png` (1024×1024, PIL).
- `main.py` is stdlib-only: it validates the PNG header with `struct` and
  copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`.
