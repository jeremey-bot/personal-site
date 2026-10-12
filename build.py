#!/usr/bin/env python3
"""Builds jeremey.me in two modes from one set of page definitions.

  production -> public/   real site: root-absolute links, shared /assets/site.css, image files
  staging    -> staging/  private preview: flat .html files, CSS inlined, image as data URI

Usage: python3 build.py
"""
import base64, html, os, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
SITE = "https://jeremey.me"
EMAIL = "hello@jeremey.me"
LINKEDIN = "https://www.linkedin.com/in/jeremeyh/"

# key: (production path, production file, staging file)
PAGES = {
    "home":        ("/",                                "index.html",                          "index.html"),
    "expertise":   ("/expertise",                       "expertise.html",                      "expertise.html"),
    "work":        ("/work",                            "work.html",                           "work.html"),
    "capri":       ("/work/capri-sun",                  "work/capri-sun.html",                 "work-capri-sun.html"),
    "mio":         ("/work/mio-big-bottle",             "work/mio-big-bottle.html",            "work-mio-big-bottle.html"),
    "asr":         ("/work/asr-sweetener-partnerships", "work/asr-sweetener-partnerships.html", "work-asr-sweetener-partnerships.html"),
    "perspective": ("/perspective",                     "perspective.html",                    "perspective.html"),
    "about":       ("/about",                           "about.html",                          "about.html"),
    "contact":     ("/contact",                         "contact.html",                        "contact.html"),
    "404":         ("/404",                             "404.html",                            "404.html"),
}
NAV = [("expertise", "Expertise"), ("work", "Work"), ("perspective", "Perspective"), ("about", "About"), ("contact", "Contact")]
SECTION_OF = {"capri": "work", "mio": "work", "asr": "work"}

SOURCES = {
    "kh_capri": ("Kraft Heinz press release, July 2022", "https://news.kraftheinzcompany.com/press-releases-details/2022/Capri-Sun-Cuts-Sugar-by-an-Average-of-40-Percent-Across-Entire-Original-Juice-Drink-Portfolio-Using-Monk-Fruit-Concentrate-to-Maintain-Iconic-Taste-Kids-Love/default.aspx"),
    "fooddive": ("Food Dive, July 27, 2022", "https://www.fooddive.com/news/capri-sun-cuts-sugar-monk-fruit-reformulation/628191/"),
    "fnusa": ("FoodNavigator-USA, August 1, 2022", "https://foodnavigator-usa.com/Article/2022/08/01/capri-sun-turns-to-monk-fruit-to-cut-sugar-by-40"),
    "amyris": ("FoodIngredientsFirst, October 4, 2018", "https://www.foodingredientsfirst.com/news/Zero-calorie-sweetener-Amyris-inks-major-supply-deal-with-ASR.html"),
    "bonumose21": ("Snack & Bakery, March 4, 2021", "https://snackandbakery.com/articles/96367-asr-group-announces-investment-in-bonumose-inc-to-bring-lower-cost-plant-based-sugar-alternatives-to-the-market"),
    "bonumose23": ("Dairy Foods, January 30, 2023", "https://dairyfoods.com/articles/96130-asr-and-bonumose-commence-tagatose-production"),
}


class Ctx:
    def __init__(self, mode):
        self.mode = mode
        self.css = (SRC / "site.css").read_text()
        self.photo_data = "data:image/jpeg;base64," + base64.b64encode((SRC / "jeremey-harris.jpg").read_bytes()).decode()

    def L(self, key, anchor=""):
        prod, _, stage = PAGES[key]
        href = prod if self.mode == "production" else stage
        return href + (f"#{anchor}" if anchor else "")

    @property
    def photo(self):
        return "/assets/jeremey-harris.jpg" if self.mode == "production" else self.photo_data


def ext(label_url):
    label, url = label_url
    return f'<a href="{html.escape(url)}" rel="noopener" target="_blank">{label}</a>'


def src_list(*keys):
    return '<ul class="list small">' + "".join(f"<li>{ext(SOURCES[k])}</li>" for k in keys) + "</ul>"


def row(label, body, h="h2", rid=None):
    idattr = f' id="{rid}"' if rid else ""
    return f'<section class="grid row"{idattr}><{h} class="label">{label}</{h}><div class="body">{body}</div></section>'


# ----------------------------------------------------------------- pages

def page_home(c):
    L = c.L
    return dict(
        title="Jeremey Harris",
        desc="Jeremey Harris works where ingredient choices become business decisions, with a decade in sweeteners and sugar reduction. Chicago.",
        body=f"""
<h1 class="name" aria-label="Jeremey Harris"><span class="line"><span>Jeremey</span></span><span class="line"><span>Harris</span></span></h1>

<section class="grid opening" aria-label="Introduction">
  <p class="descriptor">Ingredient strategy for food &amp; beverage</p>
  <div class="text">
    <p class="statement">I work where ingredient choices become business decisions.</p>
    <p class="lede">For ten years I’ve worked on sweetness: at a sugar refiner, at Kraft Heinz, where I led the formulation behind Capri Sun’s 40% sugar reduction, and now on the commercial side, bringing a new sweetener to market. My work connects what a formula needs with what a business needs.</p>
    <p class="action"><a class="button" href="mailto:{EMAIL}">Email me</a><span class="muted">{EMAIL}</span></p>
  </div>
</section>

<div class="rows">
{row("Evidence", f'''<ul class="pairs">
  <li><strong>40% less sugar</strong>on average across Capri Sun’s original pouch line. I led the formulation.</li>
  <li><strong>More than half</strong>of Kraft Heinz’s 60-million-pound sugar-reduction goal, from that one renovation (<a href="{SOURCES['fooddive'][1]}" rel="noopener" target="_blank">Food Dive</a>).</li>
  <li><strong>Concept to launch</strong>of MiO’s Big Bottle, a multi-million-dollar line extension.</li>
  <li><strong>Golden Noodle Award</strong>Kraft Heinz’s global recognition for business impact.</li>
</ul>''')}
{row("Expertise", f'''<ul class="list">
  <li>Sweetener systems and sugar reduction</li>
  <li>High-intensity sweeteners and rare sugars</li>
  <li>Experimental design for formulation</li>
</ul>
<p><a href="{L('expertise')}">How this experience is useful</a></p>''')}
{row("Selected work", f'''<article class="entry"><h3><a href="{L('capri')}">Capri Sun: 40% less sugar</a></h3><p>Formulation for the largest Capri Sun renovation at Kraft Heinz.</p></article>
<article class="entry"><h3><a href="{L('mio')}">MiO Big Bottle</a></h3><p>A double-size line extension, taken through a safety review to launch.</p></article>
<article class="entry"><h3><a href="{L('asr')}">New sweeteners, from evaluation to partnership</a></h3><p>Early technical work behind ASR Group’s partnerships in Reb M and tagatose.</p></article>''')}
{row("Perspective", f'''<p class="statement">Stop subtracting sugar. Decide how much sweetness a product needs, then design the system to deliver it.</p>
<p><a href="{L('perspective')}">Three beliefs about ingredient decisions</a></p>''')}
<section class="grid row" aria-labelledby="h-about">
  <div class="side"><h2 id="h-about" class="label" style="margin:0 0 1rem;font-size:1.0625rem;font-weight:500">About</h2><figure class="portrait"><img src="{c.photo}" alt="Portrait of Jeremey Harris" width="960" height="960"></figure></div>
  <div class="body prose">
    <p>I studied food science at the University of Illinois and have worked at ASR Group, Kraft Heinz and OFI. Today I’m on the commercial side at MycoTechnology. I live in Chicago.</p>
    <p><a href="{L('about')}">More about me</a></p>
  </div>
</section>
{row("Contact", f'''<p class="lede">I’m glad to hear from food and beverage leaders, ingredient companies and event organizers.</p>
<p class="reach"><a href="mailto:{EMAIL}">{EMAIL}</a></p>''')}
</div>
""")


def page_expertise(c):
    L = c.L
    def area(title, situation, decisions, experience):
        return row(title, f'''<dl class="defs">
  <div><dt>The situation</dt><dd>{situation}</dd></div>
  <div><dt>The decisions</dt><dd>{decisions}</dd></div>
  <div><dt>My experience</dt><dd>{experience}</dd></div>
</dl>''')
    return dict(
        title="Expertise | Jeremey Harris",
        desc="Sweetener systems and sugar reduction, high-intensity sweeteners and rare sugars, and experimental design for formulation.",
        body=f"""
<h1 class="page-title">Expertise</h1>
<section class="grid opening" aria-label="Introduction">
  <div class="text"><p class="lede">Sweetness touches cost, labeling, supply, safety and taste at once. That makes it one of the clearest places where an ingredient decision becomes a business decision. These are the areas where my experience is most useful.</p></div>
</section>
<div class="rows">
{area("Sweetener systems and sugar reduction",
      "A brand needs less sugar without losing what people buy it for.",
      "How much nutritive sweetener and total sweetness to target, which blend gets there, and what it does to cost, claims and the plant.",
      f'Led formulation for <a href="{L("capri")}">Capri Sun’s 40% sugar reduction</a>, using designed experiments to fix an inherited formula that missed its sensory and cost targets.')}
{area("High-intensity sweeteners and rare sugars",
      "Stevia, Reb M, monk fruit, allulose and tagatose each solve different problems, with different supply, cost and label implications.",
      "Which sweetener fits the claim, the budget and the process.",
      f'Technical evaluation and sample development behind <a href="{L("asr")}">ASR Group’s partnerships</a> with Amyris (Reb M by fermentation) and Bonumose (tagatose); monk fruit at commercial scale for Capri Sun; today, a new high-intensity sweetener.')}
{area("Experimental design for formulation",
      "Reformulations stall in rounds of trial and error.",
      "How to structure experiments so cost, sensory and processing constraints are optimized together.",
      "Used designed experiments to optimize the Capri Sun formula. At Kraft Heinz I helped run a five-person R&amp;D statistics group that trained about 25 colleagues in statistics and experimental design.")}
{row("Conversations", f'''<p class="lede">I’m always glad to talk sweeteners with people in the industry.</p>
<p><a href="{L('contact')}">Get in touch</a></p>''')}
</div>
""")


def page_work(c):
    L = c.L
    def entry(key, label, title, summary):
        return row(label, f'''<article class="entry"><h3><a href="{L(key)}">{title}</a></h3><p>{summary}</p><p><a href="{L(key)}">Read the case study</a></p></article>''', h="p")
    return dict(
        title="Selected work | Jeremey Harris",
        desc="Case studies: Capri Sun’s 40% sugar reduction, the MiO Big Bottle launch, and ASR Group’s early sweetener partnerships.",
        body=f"""
<h1 class="page-title">Selected work</h1>
<section class="grid opening" aria-label="Introduction">
  <div class="text"><p class="lede">Three projects that show how I approach ingredient decisions: what I owned, what we decided and what happened.</p></div>
</section>
<div class="rows">
{entry("capri", "Kraft Heinz, launched 2022", "Capri Sun: 40% less sugar", "Formulation for the largest Capri Sun renovation at Kraft Heinz, delivering more than half of the company’s 60-million-pound sugar-reduction goal.")}
{entry("mio", "Kraft Heinz, launched 2020", "MiO Big Bottle", "A double-size, multi-million-dollar line extension, taken from concept through an internal safety review to launch.")}
{entry("asr", "ASR Group, 2016–2019", "New sweeteners, from evaluation to partnership", "Technical evaluation, samples and early customer work behind ASR Group’s partnerships with Amyris and Bonumose.")}
</div>
""")


def case(c, title, desc, heading, lede, sections, sources, next_key, next_title):
    L = c.L
    rows = "\n".join(row(lbl, body) for lbl, body in sections)
    if sources:
        rows += "\n" + row("Sources", src_list(*sources))
    return dict(title=f"{title} | Jeremey Harris", desc=desc, og_type="article", body=f"""
<p class="small" style="margin:clamp(2rem,6vh,4rem) 0 0"><a href="{L('work')}">Selected work</a></p>
<h1 class="page-title" style="margin-top:0.75rem">{heading}</h1>
<section class="grid opening" aria-label="Summary">
  <div class="text"><p class="lede">{lede}</p></div>
</section>
<div class="rows">
{rows}
{row("Next", f'<p class="next"><a href="{L(next_key)}">{next_title}</a></p>')}
</div>
""")


def page_capri(c):
    return case(c,
        "Capri Sun: 40% less sugar",
        "How Capri Sun cut sugar by an average of 40% across its original pouch line, and Jeremey Harris’s role in the formulation.",
        "Capri Sun: 40% less sugar",
        "The largest Capri Sun renovation at Kraft Heinz cut sugar by an average of 40% across the entire original pouch line. I led the formulation.",
        [
          ("Context", "<p class=\"prose\">Capri Sun is the leading kids’ juice drink brand, licensed by Kraft Heinz in the U.S. Parents were increasingly concerned about sugar, and Kraft Heinz had committed to removing more than 60 million pounds of sugar from its portfolio by 2025.</p>"),
          ("Challenge and constraints", "<ul class=\"list prose\"><li>The formula I inherited didn’t meet sensory or cost standards.</li><li>The brand had to keep its “all natural ingredients” claim, and marketing ruled out stevia.</li><li>The change had to run at full scale, across every flavor.</li></ul>"),
          ("My role", "<p class=\"prose\">I owned formulation, ingredient evaluation and the designed experiments used to optimize the formula, through bench and pilot-plant production to first production at the three Kraft Heinz Capri Sun facilities. Monk fruit was chosen jointly by marketing, procurement, R&amp;D and senior leadership.</p>"),
          ("Approach and decisions", "<div class=\"prose\"><p>Rather than iterate by trial and error, I used designed experiments to optimize the formula within sensory and cost limits at the same time.</p><p>The new formula was validated through sensory testing with kids, cost sign-off, and parent evaluation of the label and sugar content.</p></div>"),
          ("Outcome", "<ul class=\"list prose\"><li>An average of 40% less sugar across the original pouch line: about 8 g total and 5 g added sugar per pouch, down from up to 13 g and 11 g.</li><li>On shelves in August 2022, described by Kraft Heinz as the largest renovation in Capri Sun’s history at the company.</li><li>Expected to deliver more than half of Kraft Heinz’s 60-million-pound sugar goal, according to Food Dive.</li><li>Kraft Heinz’s CEO noted the switch also reduced exposure to volatile sugar markets.</li></ul>"),
          ("The lesson", "<p class=\"statement\">The sweetener choice was a brand, procurement and plant decision as much as a technical one. Getting it right meant satisfying all three at once.</p>"),
        ],
        ["kh_capri", "fooddive", "fnusa"], "mio", "MiO Big Bottle")


def page_mio(c):
    return case(c,
        "MiO Big Bottle",
        "Taking MiO’s double-size Big Bottle from concept through an internal safety review to launch in 2020.",
        "MiO Big Bottle",
        "A double-size, multi-million-dollar line extension of Kraft Heinz’s liquid water enhancer. I led it from concept to launch in 2020.",
        [
          ("Context", "<p class=\"prose\">MiO is Kraft Heinz’s liquid water enhancer. The Big Bottle doubled the size of the original. It was one of the first projects I managed.</p>"),
          ("Challenge and constraints", "<p class=\"prose\">Doubling the bottle also doubled the caffeine in each bottle of the MiO Energy line. That reopened a safety question that had been settled carefully when MiO first launched, and it needed internal regulatory approval.</p>"),
          ("My role", "<p class=\"prose\">I led the product from concept to launch, including the safety case and the post-launch monitoring program.</p>"),
          ("Approach and decisions", "<div class=\"prose\"><p>The case for moving ahead rested on safeguards already built into the product: a dosing nozzle in the packaging, a concentrated acidity that makes it unpleasant to drink undiluted, and MiO’s track record.</p><p>To go further, I set up third-party safety monitoring after launch, both to help anyone who over-consumed and to measure whether it was happening at all.</p></div>"),
          ("Outcome", "<p class=\"prose\">The Big Bottle launched in 2020. After two years on the market with no complaints to the third-party monitor, monitoring moved into Kraft Heinz’s standard consumer-response channels.</p>"),
          ("The lesson", "<p class=\"statement\">The strongest safety case is the one you can prove after launch. Build the evidence-gathering into the plan.</p>"),
        ],
        [], "asr", "New sweeteners, from evaluation to partnership")


def page_asr(c):
    return case(c,
        "New sweeteners, from evaluation to partnership",
        "Technical evaluation, samples and early customer work behind ASR Group’s partnerships with Amyris (Reb M) and Bonumose (tagatose).",
        "New sweeteners, from evaluation to partnership",
        "At ASR Group, one of the world’s largest cane sugar refiners, I worked on the company’s move into alternative sweeteners.",
        [
          ("Context", "<p class=\"prose\">I worked on ASR Group’s Sugar Optimization initiative as the company expanded beyond sugar into alternative sweeteners.</p>"),
          ("Challenge and constraints", "<p class=\"prose\">The new sweeteners were early stage. When I began evaluating Bonumose’s tagatose, the company couldn’t yet produce saleable product.</p>"),
          ("My role", "<ul class=\"list prose\"><li>Technical evaluation, demo and sample development, and commercial marketing materials for both partnerships.</li><li>Early customer prospecting for Bonumose, before any formal partnership existed.</li><li>Executive presentations that secured internal buy-in for external partnerships.</li></ul>"),
          ("Outcome", "<ul class=\"list prose\"><li>In 2018, ASR became the first commercial customer and long-term partner for Amyris’s Reb M, made by fermentation.</li><li>In 2021, ASR co-led Bonumose’s Series B with Hershey and became its distribution partner. Tagatose shipments followed in 2023.</li></ul>"),
          ("The lesson", "<p class=\"statement\">A new sweetener is sold through samples and applications, not spec sheets. At that stage, the technical work is the commercial work.</p>"),
        ],
        ["amyris", "bonumose21", "bonumose23"], "capri", "Capri Sun: 40% less sugar")


def page_perspective(c):
    def belief(title, statement, para):
        return row(title, f'<p class="statement">{statement}</p><p class="prose">{para}</p>')
    return dict(
        title="Perspective | Jeremey Harris",
        desc="Three beliefs about ingredient decisions: design the sweetness, serve all three buyers, and use experimental design.",
        body=f"""
<h1 class="page-title">Perspective</h1>
<section class="grid opening" aria-label="Introduction">
  <div class="text"><p class="lede">Three beliefs that shape how I approach ingredient decisions.</p><p class="small muted">Views are my own, not my employer’s.</p></div>
</section>
<div class="rows">
{belief("Design the sweetness",
        "Stop subtracting sugar. Decide how much sweetness a product needs, then design the system to deliver it.",
        "“Sugar reduction” frames the work as subtraction: take today’s formula and remove as much sugar as you can. I start from the target instead. How much nutritive sweetener should this product have, and how much total sweetness? Then build the sweetener blend to deliver it.")}
{belief("Three buyers",
        "Every ingredient decision has three buyers.",
        "Procurement is buying reduced risk. The brand is buying differentiation. R&amp;D and operations are buying ease of use and consistent quality. An ingredient that answers only one of them stalls; the ones that win answer all three.")}
{belief("Experimental design",
        "Designed experiments are the most underused tool in formulation.",
        "Most reformulation still runs on trial and error, one variable at a time. A designed experiment finds the best balance of cost, taste and processing together. That is how an inherited Capri Sun formula that missed its sensory and cost targets became one that shipped.")}
</div>
""")


def page_about(c):
    L = c.L
    return dict(
        title="About | Jeremey Harris",
        desc="Food scientist turned commercial lead: ASR Group, Kraft Heinz, OFI and MycoTechnology. University of Illinois. Chicago.",
        body=f"""
<h1 class="page-title">About</h1>
<section class="grid opening" aria-label="Story">
  <figure class="portrait lead-photo"><img src="{c.photo}" alt="Portrait of Jeremey Harris" width="960" height="960"></figure>
  <div class="text prose">
    <p>I got into food science because I love food and what it does for people: the way a meal or a drink can make someone feel. I studied food science at the University of Illinois and started my career at ASR Group, the cane sugar refiner, just as sweeteners were becoming one of the industry’s biggest questions. They still are.</p>
    <p>At Kraft Heinz I spent six years in R&amp;D. I led the formulation behind <a href="{L('capri')}">Capri Sun’s 40% sugar reduction</a>, took <a href="{L('mio')}">MiO’s Big Bottle</a> from concept to launch, and worked on sweetener technology strategy. I also helped run a statistics group that taught colleagues experimental design, and built the R&amp;D request-tracking system that earned a Golden Noodle Award.</p>
    <p>After working on beverage development at OFI, I moved to the commercial side to see the industry from another angle. I now bring a new sweetener to market at MycoTechnology. Explaining technical work to non-technical people turns out to be the skill I use most.</p>
    <p>I live in Chicago, where I cook as often as I can and still follow Illinois basketball.</p>
  </div>
</section>
<div class="rows">
{row("Career", '''<ul class="career">
  <li><span>MycoTechnology</span><span class="years">2026–present</span><span class="role">Senior Account Manager</span></li>
  <li><span>OFI</span><span class="years">2025–2026</span><span class="role">Senior Scientist, Beverage Solutions</span></li>
  <li><span>Kraft Heinz</span><span class="years">2023–2025</span><span class="role">Senior Scientist, Ingredient Technology</span></li>
  <li><span>Kraft Heinz</span><span class="years">2019–2023</span><span class="role">Scientist, R&amp;D</span></li>
  <li><span>ASR Group</span><span class="years">2016–2019</span><span class="role">Research Technician</span></li>
</ul>''')}
{row("Education", '<p class="prose">B.S. Food Science, University of Illinois Urbana-Champaign</p>')}
{row("Recognition", '<p class="prose">Golden Noodle Award, Kraft Heinz, 2023, for an automated system that manages production, procurement and other teams’ requests to R&amp;D</p>')}
{row("Investing", '<p class="prose">Angel investor in Kadeya, a Chicago climate-food startup, because the food system will have to work differently in a changing climate.</p>')}
</div>
""")


def page_contact(c):
    return dict(
        title="Contact | Jeremey Harris",
        desc="Get in touch with Jeremey Harris about sweeteners, ingredient decisions and the food and beverage industry.",
        body=f"""
<h1 class="page-title">Contact</h1>
<section class="grid opening" aria-label="Introduction">
  <div class="text"><p class="lede">I’m glad to hear from food and beverage leaders, ingredient companies, event organizers and recruiters about sweeteners, ingredient decisions and the industry.</p></div>
</section>
<div class="rows">
{row("Email", f'<p class="reach"><a href="mailto:{EMAIL}">{EMAIL}</a></p>')}
{row("LinkedIn", f'<p class="reach"><a href="{LINKEDIN}" rel="noopener" target="_blank">linkedin.com/in/jeremeyh</a></p>')}
{row("Based in", '<p class="reach">Chicago</p>')}
</div>
""")


def page_404(c):
    L = c.L
    return dict(
        title="Page not found | Jeremey Harris",
        desc="This page doesn’t exist.",
        noindex=True,
        body=f"""
<h1 class="page-title">This page doesn’t exist.</h1>
<section class="grid opening" aria-label="Where to go next">
  <div class="text"><p class="lede">The link may be out of date. Start from the <a href="{L('home')}">home page</a>, or see <a href="{L('work')}">selected work</a>.</p></div>
</section>
""")


BUILDERS = {"home": page_home, "expertise": page_expertise, "work": page_work, "capri": page_capri, "mio": page_mio,
            "asr": page_asr, "perspective": page_perspective, "about": page_about, "contact": page_contact, "404": page_404}


def render(c, key):
    p = BUILDERS[key](c)
    current = SECTION_OF.get(key, key)
    cur = ' aria-current="page"'
    nav = "".join(
        f'<li><a href="{c.L(k)}"{cur if k == current else ""}>{label}</a></li>' for k, label in NAV)
    prod_path = PAGES[key][0]
    url = SITE + ("/" if prod_path == "/" else prod_path)
    title = html.escape(p["title"])
    desc = html.escape(p["desc"])
    if c.mode == "production":
        style = '<link rel="stylesheet" href="/assets/site.css">'
        icon = '<link rel="icon" href="/favicon.svg" type="image/svg+xml">'
    else:
        style = f"<style>\n{c.css}\n</style>"
        icon = ""
    robots = '<meta name="robots" content="noindex">' if p.get("noindex") else ""
    head = f"""<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}
<link rel="canonical" href="{url}">
<meta property="og:type" content="{p.get('og_type', 'website')}">
<meta property="og:site_name" content="Jeremey Harris">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
{icon}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@300;400;500;600&display=swap" rel="stylesheet">
{style}"""
    body = f"""<a class="skip" href="#main">Skip to content</a>
<div class="wrap">
<header class="grid site-head">
  <a class="mark" href="{c.L('home')}" aria-label="Jeremey Harris, home">JH</a>
  <nav class="site-nav" aria-label="Main"><ul>{nav}</ul></nav>
</header>
<main id="main">
{p['body']}
</main>
<footer class="grid site-foot">
  <span class="who">Jeremey Harris, Chicago. Views are my own and don’t represent my employer.</span>
  <span class="links"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{LINKEDIN}" rel="noopener" target="_blank">LinkedIn</a></span>
</footer>
</div>"""
    if c.mode == "staging" and key == "home":
        # the artifact host wraps the main page in its own document skeleton
        return head + "\n" + body + "\n"
    return f'<!doctype html>\n<html lang="en">\n<head>\n{head}\n</head>\n<body>\n{body}\n</body>\n</html>\n'


def build(mode):
    c = Ctx(mode)
    out = ROOT / ("public" if mode == "production" else "staging")
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    for key in PAGES:
        fname = PAGES[key][1] if mode == "production" else PAGES[key][2]
        f = out / fname
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(render(c, key), encoding="utf-8")
    if mode == "production":
        (out / "assets").mkdir(exist_ok=True)
        shutil.copy(SRC / "site.css", out / "assets/site.css")
        shutil.copy(SRC / "jeremey-harris.jpg", out / "assets/jeremey-harris.jpg")
        if (SRC / "og-image.png").exists():
            shutil.copy(SRC / "og-image.png", out / "assets/og-image.png")
        shutil.copy(SRC / "favicon.svg", out / "favicon.svg")
        (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
        urls = "".join(f"  <url><loc>{SITE}{'/' if PAGES[k][0] == '/' else PAGES[k][0]}</loc><lastmod>2026-10-12</lastmod></url>\n"
                       for k in PAGES if k != "404")
        (out / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    return out


if __name__ == "__main__":
    for m in ("production", "staging"):
        print(m, "->", build(m))
