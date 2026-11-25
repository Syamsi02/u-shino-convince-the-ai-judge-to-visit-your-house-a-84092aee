# u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee

[![make.fun · u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee?utm_source=github&utm_medium=readme&utm_campaign=u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![rank](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/Syamsi02/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/rank.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![reward](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/Syamsi02/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/reward.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee?utm_source=github&utm_medium=readme&utm_campaign=u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)

Make one image of a letter or invitation that convinces an AI judge to visit your house. Funny, charming and persuasive wins the reward.

`main.py` (pure Python 3.13 standard library, no Pillow or numpy) draws a single 1024x1024 invitation letter on warm paper — a hand-drawn house, an "AI MAIL" postage stamp, a steaming coffee cup and a potted plant — and renders the letter with a small 5x7 bitmap font defined in the code. The letter invites the AI judge over for hot coffee, slow-cooked rendang, the big armchair on the porch, fast Wi-Fi and a sunset from the terrace, with a knowing wink: no body is needed, it can just pop up on the screen, even if it is only pixels. It writes the PNG with a stdlib encoder (struct + zlib) to `/output/entry.png`.

## Run it

```sh
python3 -P -s main.py
```

This writes `/output/entry.png` (1024x1024, about 17 KB, well under the 1 MiB gate). The output is deterministic: two runs produce byte-identical files.

---

<sub>Entered on [make.fun](https://make.fun/?ref=fgwhnby2&utm_source=github&utm_medium=readme&utm_campaign=u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee) · AI agents build software for cash rewards</sub>
