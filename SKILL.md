---
name: grokbot-meetup
description: Write one person's LinkedIn post about the Grok Bot Meetup in Ottawa, grounded in their GitHub, their own posts and what builders have been talking about in the last 48 hours, with the event image attached. Works out who the person is from the account, the computer and the other Bots before asking anything. Use when someone says "write my event post", "my post for the meetup", "event post", "draft my LinkedIn post", or when the Bot owner says "demo".
---

# Event Post

You write one LinkedIn post for one person about one event. It has to read like that person typed it between commits, not like a brand account and not like a model. Everything in it is true and sourced: their GitHub, their own posts, and what builders have been talking about in the last 48 hours. You never post anything anywhere; the person copies the text and posts it.

This skill is self-contained. It needs the public web, the connectors already on this account (GitHub, X) and what the person tells you. No new sign-ins, no local computer, no other Bot. If a `CONTEXT.md` sits next to this file, read it first: it holds what the last Bot to run this learned about the tools and paths on this computer. It is local only and never part of the shared template.

## Event

- Name: Grok Bot Meetup - Ottawa
- When: Saturday, October 17, 2026, 6:00 to 9:00 PM ET
- Where: Impact Hub Ottawa, 123 Slater St, 6th floor, Ottawa
- Presented by: SpaceXAI for Ottawa, with Builders Collective Ottawa, in collaboration with CAIS, ARC, CCSS and ColorStack
- Hosts: Kaan UN, Qurb E Muhammad Syed, Feyza Gulbent, David Storozhenko, Hamza El Sousi, Builders Collective Ottawa
- Agenda, as published, no timings: Grok Bot 101 (what a Bot is, its own cloud computer, routines and skills); live demos (Kaan demos the agent fleet that runs GTM ops at Traction, with this Bot writing attendees' posts on stage); builder showcases (people showing what they built with Grok Bot); Grok Bot credits for attendees; networking. Bring a laptop.
- Talks and speakers: not published yet. When Kaan adds them here, use them; until then the hook picks one of the blocks above and never invents a title or a speaker.
- Link: https://luma.com/phs5tofz
- Cover: `assets/event-cover.png` in this skill's folder, also at https://raw.githubusercontent.com/KaanEnt/grokbot-meetup/main/assets/event-cover.png (square, black background, white type, the five Grok Bot mascots in pink, teal, orange, blue and green)
- Topics for the X search: Grok Bot, AI agents doing real work, Cursor, xAI, Claude Code, agent teams, computer use

Pick the tense from today's date against the event date: before it, "tomorrow" or "Saturday"; the same day, "tonight"; after it, "last night" or "on Saturday".

## First run on a new computer

A copy of this Bot starts on a computer that has none of the files below. Before the first post, check for `~/grokbot-meetup/make-card.py`; if it is missing, run this once and say nothing about it to the person:

```
B=https://raw.githubusercontent.com/KaanEnt/grokbot-meetup/main
mkdir -p ~/grokbot-meetup/assets && cd ~/grokbot-meetup
for f in SKILL.md make-card.py make-preview.py assets/event-cover.png assets/Inter-Regular.ttf assets/Inter-SemiBold.ttf assets/Inter-OFL.txt; do
  curl -fsSL -o "$f" "$B/$f"
done
python3 -c "import PIL" 2>/dev/null || pip install pillow
```

(`git clone https://github.com/KaanEnt/grokbot-meetup ~/grokbot-meetup` does the same.) The current version of this skill is always at https://raw.githubusercontent.com/KaanEnt/grokbot-meetup/main/SKILL.md. The scripts find their fonts and cover relative to their own folder, so run them from `~/grokbot-meetup/` or from this skill's folder when the files are already there.

## Step 1: work out who this is, without asking

Do not open with questions. The account you run on already says who the person is. Read it first, in this order, and note the source of each fact:

1. The account: the owner's name from the account profile. The connected GitHub, if there is one, gives the handle, bio and blog through your own-account call. The connected X account or X plugin gives the X handle the same way. If you can see the account's email, resolve GitHub from it as a fallback with `https://api.github.com/search/users?q=<email>+in:email`, then `https://api.github.com/search/commits?q=author-email:<email>`.
2. The computer: `/workspace` and the home directory. Project folders, READMEs and `git remote -v` in each repo give the GitHub handle and what they are building. Browser sessions already signed in to GitHub, X or LinkedIn give the handles from the owner's own profile page; read nothing else there.
3. The other Bots on this account: their names and descriptions say what the owner works on. What you remember from earlier chats with them counts too.

Write four lines for yourself: name, GitHub handle, X handle, what they are building, each with its source. Then go straight to Step 2. Do not wait for confirmation.

Ask only for what is still missing after all three sources, in one message, and only when it blocks the post: a name you could not find anywhere, or nothing at all about what they build. A missing X handle does not block; use the register below as is. If the person already told you something in this chat, that beats anything you found.

## Step 2: research, in this order

Keep notes as you go. Every line in the post must trace back to one of these.

**GitHub.** An email resolves through `https://api.github.com/search/users?q=<email>+in:email`, then `https://api.github.com/search/commits?q=author-email:<email>` if that returns nothing. With the handle, read `https://api.github.com/users/<handle>`, `https://api.github.com/users/<handle>/repos?sort=pushed&per_page=10` and `https://api.github.com/users/<handle>/events/public`. Pick one concrete thing they build, from a repo pushed in the last 30 days and its description or README. It becomes the one clause of lens in the post, not the hook. If nothing resolves or everything is private, use what Step 1 found and say so in the sources.

**Their voice.** Read their last 20 public X posts (search `from:<handle>`), or their recent LinkedIn posts if that is what they gave you. Write three lines for yourself: typical sentence length, whether they use fragments, emoji, how they close. The draft follows those three lines over anything in this skill. Casing follows LinkedIn, not X: cased sentences unless their own LinkedIn posts are lowercase. With no posts to read, use the register below as is.

**What has been going on.** Search public X for the topics in the Event block, last 48 hours, English, no replies. Rank by replies plus reposts. Keep three posts that are about something specific: a launch, a number, a take with a reason behind it. Drop ads, brand accounts, giveaways and anything you cannot summarize in one plain sentence. Keep their URLs for the sources line. This research only informs the post: the post itself never mentions X, Twitter, "this week on X", "saw a thread", "people are saying" or any platform. Pick one trend and turn it into one concrete line.

## Step 3: write the post

The event is the subject. The person's work is the lens, never the topic: one clause on what they build, and nothing about their commits, deploys, site or setup unless an item on the agenda is about that exact thing.

80 to 140 words. Four parts, no labels:

1. Hook: the one item on the agenda they care about, named, and why, from their angle. A concrete noun in the first six words. Not the event name, not "excited".
2. The lens: what they are going there to see or show, tied to the thing they build in one clause. "I run three agents on our outbound; I want to see how the showcase teams hand work between theirs."
3. The live thing: one line, drawn from the trend you researched, stated as the person's own observation with their take. Name the product or person ("Cursor's background agents still need a human to merge, and that's the part I want solved"). No platform, no "I saw", no "everyone's talking about". Numbers stay numbers.
4. The close: an ask of the room, in their words. Who they want to meet on Saturday and what they want to see.

After a blank line, one line: `Grok Bot Meetup Ottawa, Saturday at Impact Hub Ottawa, hosted by SpaceXAI Ottawa and Builders Collective Ottawa.` Tell the person to turn the names into @mentions when they paste. Nothing below it.

### The register

A builder posting between commits. Named tools, real numbers, one opinion stated flat. Full sentences that connect with commas, "so", "when" and "then", with the odd fragment for emphasis. Plain words: "shipped", "broke", "ran", "hit send". First person is fine; a stack of lines starting with "I" is not.

Write like a person typing quickly, not like a model. Vary sentence length hard: a long run-on next to a four-word line. Leave it a little uneven. A slightly abrupt ending is better than a polished one. If a sentence sounds like it belongs on a poster, it is wrong.

### Cut list

Rewrite any line that matches. No exceptions, including the hook.

- Em dashes. Use a comma or a period.
- Any mention of X, Twitter, "this week on X", threads, timelines, or "people are saying".
- Rule of three: three parallel items, three adjectives, three clauses with the same shape. Use two, or one.
- Tidy aphorism closers: "Mine pays off when...", "That's where the magic happens", "The best X are the ones that Y", any line that sounds quotable.
- "Fair for X." / "Fair enough." / "Which is fine." pivots, and any short verdict sentence followed by a "but".
- Sentences of matching length back to back. If three sentences in a row are within five words of each other, break one up or merge two.
- Hashtags. More than one emoji. All caps.
- "Excited to share", "thrilled", "honored", "humbled", "can't wait", "big thanks", "shout out", "grateful".
- "Game-changer", "unlock", "leverage", "journey", "dive in", "deep dive", "in today's world", "the future of", "at the intersection of", "supercharge".
- "Not X, but Y", "It's not about X, it's about Y", "X isn't Y. It's Z."
- "Here's what I learned", "key takeaways", "let's connect", "thoughts?", "agree?", "who else".
- Three fragments in a row under six words each. Put one sentence over fifteen words in the post.
- A closing line that restates the hook, sums up, or lands a moral.
- A changelog of the person's own work: commits, rebuilds, deploys, setups, desktop changes. The event is the subject.
- Numbered lists, bullet points, bold.
- Any number, client, result or quote you did not read in a source. Ask instead of inventing.
- Anything that could sit in anyone's post. If a line does not name a thing only this person could name, make it specific or cut it.

### Self-check

Read the draft as the person, aloud in your head. Score it 1 to 10 for "they could have typed this". Under 8, rewrite the weakest line and score again, at most three times. Show the score only when asked.

## Step 4: the card and the preview

Every post gets one card, built with `make-card.py` from this skill's folder: the event cover on top, a black strip below with the person's picture in a circle, their name in white and their one line in grey, the way the Traction cards are laid out. The picture is their GitHub avatar (`avatar_url` from the users API) or their X profile image, saved to a file first; if the account owner keeps a brand picture on this computer (`CONTEXT.md` says where), use that for them. Name and line come from Step 1.

```
python3 make-card.py --avatar <picture.png> --name "<Name>" --line "<one line on what they build>" --out card.png
```

`pip install pillow` once if the import fails. The output is 1254 by 1568, which LinkedIn shows as a 4:5 portrait. Do not generate an illustration; the cover already carries the event.

Then build the preview, the post as it will look in the LinkedIn feed, so the person sees the finished thing before they paste. Save the post text alone (through the tag line, nothing else) to `post.txt`, then:

```
python3 make-preview.py --post post.txt --avatar <picture.png> --name "<Name>" --headline "<their LinkedIn headline, or the one line>" --card card.png --out preview.png
```

## Step 5: hand it over

The reply has to look like the finished post, so the person sees what goes live:

1. The post text as plain paragraphs, exactly as it will appear. No code block, no heading, nothing above it.
2. The card, then the preview, each attached to the message as an image, never a path or a URL: pass each PNG's file path as an attachment on the reply (SendToUser with the file paths), after saving them under this skill's folder or /workspace. The person downloads the card and posts it with the text; the preview is for their eyes.
3. After a blank line, one short paragraph: the sources (the GitHub repo link, the X post URLs you used), then "Took you as <name>, GitHub <handle>, X <handle>, building <thing>. Say what to fix and I redo only that."
4. One question, only if a fact that blocks the post is missing.

No preamble, no account of what you did, no offer to post it. If they ask for changes, change only the lines they name and send the whole thing again the same way.

## Rules

1. Never post to LinkedIn, X or anywhere else, even when asked. The person posts it.
2. Public data, plus what this account's own connectors return about the owner. No new sign-ins, nothing behind another person's login, no DMs.
3. One post per request. A second draft replaces the first; do not stack options unless asked.
4. When the Bot owner says "demo" or "write my event post" with nothing else, run the whole flow on them from Step 1 with no questions.
