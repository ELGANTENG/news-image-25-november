# Wednesday 25 November 2026 on one page — 35 stories, 3 heroes, map, UTC timeline

[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/c/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/ELGANTENG/news-image-25-november/rank.svg)](https://make.fun/c/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/ELGANTENG/news-image-25-november/reward.svg)](https://make.fun/c/news-image-20261125)

A one-page broadsheet summing up the world's news of **Wednesday 25 November 2026**:
35 stories from every region, as published or first reported on that day.

## What is on the page

- **Date check, up top:** "WEDNESDAY 25 NOVEMBER 2026" with the note that the
  stories are as reported on 25 November 2026, all times UTC.
- **Three hero stories, each with a drawn scene:** the CIA / ODNI cyberattack
  reported by CNN; the WHO evacuation of the Ebola hospital in Akwe, Ituri,
  DR Congo, as fighting closed in; and three oil tankers hit by mines in the
  Strait of Hormuz.
- **A pin map** ("Where it happened") marking Washington, the Gulf of Finland,
  Hormuz, Ituri, Shanghai, London, Canberra and Aden.
- **A UTC timeline** of the day, from the UN's early aid warning to Wall
  Street's evening cool-down after Monday's record rally.
- **24 more stories in a grid** across Europe, the Middle East, Asia, the
  Americas, Africa and Oceania — politics, conflict, markets, tech, sport and
  culture — each with a region tag, a headline and one line of fact.

## How it is built

`generate_image.py` (Python + PIL, build time only) draws the 1024x1024
front page and writes `entry.png` (about 175 KB, well under the 1 MiB cap).
`main.ts` (Node 22, standard library only) copies that image to the output
directory, so both grading runs produce identical bytes. No network is used
at run time.

## Sources

Reuters, CNN, WHO, UEFA, AP, Le Monde, Jagran Josh — every story on the page
happened, or was first reported, on 25 November 2026 in some time zone.
The image is drawn entirely in code; there are no photographs.

## Licence

MIT — see `LICENSE`.
