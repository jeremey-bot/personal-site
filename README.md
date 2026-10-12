# jeremey.me: site source

This is the multi-page personal site built on 2026-10-12 to the brief in `BRIEF - Personal Brand Website.md`. It uses the Executive modernist layout set in Hanken Grotesk, with a black-and-white portrait.

## How it's built

- **All page text lives in `build.py`.** Each page is a small function, so editing wording means editing that function.
- **Styles** are in `src/site.css`. **Images** are in `src/`: the portrait, the social-sharing image and the favicon.
- **To rebuild, run `python3 build.py`.** It writes two outputs:
  - `public/`: the real site, which is what gets deployed. Clean URLs (`/expertise`, `/work/capri-sun`), a shared stylesheet, `sitemap.xml`, `robots.txt` and a 404 page.
  - `staging/`: a flat, self-contained copy used for the private Claude preview.

## How it's deployed

GitHub repo `jeremey-bot/personal-site`, deployed by a Cloudflare Worker on every push to `main`. `wrangler.jsonc` serves `./public`, so the repo's own files (README, build script) are not public, and unknown URLs show `public/404.html`. Live since 2026-10-12.

To change the site: edit `build.py` or `src/`, run `python3 build.py`, check `public/`, then commit and push. Check jeremey.me on desktop and phone afterwards.

## Brand system

The site follows the Jeremey Harris brand system (2026-10-12): white paper, black type, cobalt `#1F3BD6` for identity and links, Illini Orange `#FF5F05` for proof only (Evidence figures at 24px and up; `#B93C0A` for smaller orange text), Hanken Grotesk throughout. The tokens are at the top of `src/site.css`. The full rules are in `brand-system/BRAND-BOOK.md` and `BRAND-SYSTEM.md` in the vault project folder.

## Email signature kit

`src/email/` is copied to `public/email/` by the build:
- `jh-mark.png`: the JH mark at 108 px, shown at 36 px in email (hosted so iPhone Mail keeps it).
- `signature.html`: served at https://jeremey.me/email/signature. Open it in Safari on the iPhone, tap Copy signature, and paste into Settings → Apps → Mail → Signature. It is noindex, not linked from the site and not in the sitemap.

## Who owns what (brief §8)

Jeremey owns everything:
- **Domain:** jeremey.me, via iCloud+ and Cloudflare Registrar.
- **DNS, SSL and hosting:** his Cloudflare account. Hosting costs $0; the only cost is the domain renewal.
- **Source:** his GitHub account, `jeremey-bot/personal-site`.
- **Content:** this folder in the vault.

The site uses no third-party services except Google Fonts. There are no forms, analytics or cookies.

## Open items

The brief's §11 checklist and anything still open are tracked in `Personal Brand Plan.md`.
