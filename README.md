# grokbot-meetup

A shareable Grok Bot skill that writes one person's LinkedIn post about the Grok Bot Meetup in Ottawa (Saturday, October 17, 2026, Impact Hub Ottawa), plus a branded card image and a LinkedIn-feed preview.

## Files

- `SKILL.md`: the skill. Drop it into a Grok Bot's skills/workflows folder.
- `luma-event.py`: reads the public Luma event page (no sign-in, stdlib only) and prints clean JSON: name, times, venue, description, hosts with their links, cover URL. `python3 luma-event.py https://luma.com/phs5tofz`
- `make-card.py`: builds the 1254x1568 post card (event cover + avatar, name, one line).
- `make-preview.py`: renders the post as it would look in the LinkedIn feed.
- `assets/`: `event-cover.png`, Inter Regular/SemiBold fonts and their license (`Inter-OFL.txt`, SIL Open Font License 1.1).

## Quick start

```
git clone https://github.com/KaanEnt/grokbot-meetup ~/grokbot-meetup
cd ~/grokbot-meetup && pip install pillow
python3 make-card.py --avatar me.png --name "Your Name" --line "What you build" --out card.png
python3 make-preview.py --post post.txt --avatar me.png --name "Your Name" --headline "Your headline" --card card.png --out preview.png
```

Scripts resolve assets relative to their own folder. The skill never posts anything; the person copies the text and posts it.

Event: https://luma.com/phs5tofz
