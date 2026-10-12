# jeremey.me: site source

This is the multi-page personal site built on 2026-10-12 to the brief in `BRIEF - Personal Brand Website.md`. It uses the Executive modernist layout set in Hanken Grotesk, with a black-and-white portrait.

## How it's built

- **All page text lives in `build.py`.** Each page is a small function, so editing wording means editing that function.
- **Styles** are in `src/site.css`. **Images** are in `src/`: the portrait, the social-sharing image and the favicon.
- **To rebuild, run `python3 build.py`.** It writes two outputs:
  - `public/`: the real site, which is what gets deployed. Clean URLs (`/expertise`, `/work/capri-sun`), a shared stylesheet, `sitemap.xml`, `robots.txt` and a 404 page.
  - `staging/`: a flat, self-contained copy used for the private Claude preview.

## How it's deployed

The site goes live through the existing setup: GitHub repo `jeremey-bot/personal-site`, deployed by a Cloudflare Worker on every push.

To launch:
1. Copy `public/`, `wrangler.jsonc`, `build.py`, `src/` and this README into the repo root.
2. Remove the old root `index.html`.
3. Push. `wrangler.jsonc` now serves `./public`, so the repo's own files (README, build script) are no longer public. Unknown URLs show `public/404.html`.
4. Check jeremey.me and www.jeremey.me on desktop and phone. The www redirect rule stays as it is.

## Who owns what (brief §8)

Jeremey owns everything:
- **Domain:** jeremey.me, via iCloud+ and Cloudflare Registrar.
- **DNS, SSL and hosting:** his Cloudflare account. Hosting costs $0; the only cost is the domain renewal.
- **Source:** his GitHub account, `jeremey-bot/personal-site`.
- **Content:** this folder in the vault.

The site uses no third-party services except Google Fonts. There are no forms, analytics or cookies.

## Before launch

Run the brief's §11 checklist. The open items are tracked in `Personal Brand Plan.md`.
