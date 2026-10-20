#!/usr/bin/env python3
"""Generate a portable, bilingual static academic website. Python 3.9+, no packages required."""
from pathlib import Path
from collections import defaultdict
from urllib.parse import urlsplit
import html
import json
import os

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
PAPERS = json.loads((ROOT / "content/publications.json").read_text())
ARCHIVE = json.loads((ROOT / "content/archive.json").read_text())
RECORDS = json.loads((ROOT / "content/profile-records.json").read_text())
DEFAULT_SITE_URL = "https://tktkymym.github.io/"


def site_base_url():
    """Return a validated absolute URL, including an optional project-site path."""
    value = os.environ.get("SITE_URL", DEFAULT_SITE_URL).strip()
    if not value or any(c.isspace() or ord(c) < 32 for c in value):
        raise ValueError("SITE_URL must be a non-empty URL without whitespace.")
    if any(c in value for c in ('\\', '<', '>', '"', "'", '?', '#')):
        raise ValueError("SITE_URL must not contain quotes, backslashes, a query, or a fragment.")
    try:
        parsed = urlsplit(value)
        parsed.port  # Validate a port if one was supplied.
    except ValueError as exc:
        raise ValueError("SITE_URL is not a valid absolute URL.") from exc
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError("SITE_URL must be an absolute http:// or https:// URL.")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("SITE_URL must not contain credentials.")
    return value.rstrip("/") + "/"


CANONICAL = site_base_url()
UPDATED = "2026.10.20"
LINKS = {
    "lab": "https://mprg.jp/",
    "about": "https://mprg.jp/about",
    "university": "https://www.chubu.ac.jp/",
    "profile": "https://research-db.chubu.ac.jp/chbhp/KgApp/k03/resid/S002210",
    "scholar": "https://scholar.google.com/citations?hl=en&user=hkguTPgAAAAJ",
    "researchmap": "https://researchmap.jp/ytakayosi",
    "dblp": "https://dblp.org/pid/64/5510.html",
    "jdla": "https://www.jdla.org/about/",
    "jdla_news": "https://www.jdla.org/news/20250730/",
    "book": "https://www.kspub.co.jp/book/detail/5133316.html",
    "tutorials": "https://mprg.jp/lecture",
}

def e(s):
    return html.escape(str(s), quote=True)

def external(url, label, cls=""):
    return '<a href="' + e(url) + '"' + (' class="' + cls + '"' if cls else '') + ' target="_blank" rel="noopener noreferrer">' + label + '</a>'

def icon(kind):
    common = 'class="diagram" viewBox="0 0 250 125" xmlns="http://www.w3.org/2000/svg" fill="none" aria-hidden="true"'
    if kind == "vision":
        shape = '''<path d="M7 107h236M25 19h25M25 19v22M225 19h-25M225 19v22" stroke="#bbcede"/>
        <path d="M66 107V68c0-9 8-16 17-16s17 7 17 16v39M157 107V73c0-9 8-16 17-16s17 7 17 16v34" fill="#dceaf4"/>
        <circle cx="83" cy="39" r="13" fill="#a9c3d8"/><circle cx="174" cy="43" r="13" fill="#a9c3d8"/>
        <path d="M48 23h70v88H48zM143 26h62v85h-62z" stroke="#326b93" stroke-width="1.5"/>
        <path d="M78 35h10M83 30v10M169 40h10M174 35v10" stroke="#326b93"/>
        <rect x="48" y="11" width="42" height="12" fill="#326b93"/><rect x="143" y="14" width="42" height="12" fill="#326b93"/>
        <text x="53" y="20" fill="white" font-size="7" font-family="sans-serif">HUMAN</text><text x="148" y="23" fill="white" font-size="7" font-family="sans-serif">HUMAN</text>'''
    elif kind == "driving":
        shape = '''<path d="M30 116 95 10h61l65 106" fill="#e3edf5" stroke="#bfd2e1"/>
        <path d="m105 10-35 105M146 10l35 105" stroke="white" stroke-width="2"/>
        <path d="M124 12v13m0 10v19m0 12v28m0 13v10" stroke="white" stroke-width="2"/>
        <rect x="130" y="64" width="25" height="37" rx="5" fill="#326b93"/><rect x="134" y="70" width="17" height="10" rx="2" fill="#accde5"/>
        <rect x="91" y="28" width="17" height="26" rx="3" fill="#9fb7c9"/>
        <path d="M116 96c-7-18-3-39 13-59M164 96c6-18 2-39-13-59" stroke="#326b93" stroke-dasharray="3 4"/>
        <path d="M8 105h25V77H8zM14 73h12M211 78h25v28h-25zM218 68h12" stroke="#9bb4c8"/>
        <circle cx="205" cy="36" r="10" fill="#d2e4f2"/><path d="M205 46v17" stroke="#95b1c9"/>
        <path d="M142 48v-9m0 0-4 5m4-5 4 5" stroke="#326b93" stroke-width="1.5"/>'''
    elif kind == "education":
        shape = '''<path d="M12 108h226M12 108V20M12 20h0" stroke="#bbcede"/>
        <path d="M22 92 62 70 102 78 142 44 182 52 228 24" stroke="#326b93" stroke-width="2.5" stroke-linejoin="round"/>
        <g fill="#dceaf4" stroke="#a7c3d8"><rect x="34" y="82" width="16" height="26"/><rect x="74" y="64" width="16" height="44"/><rect x="114" y="70" width="16" height="38"/><rect x="154" y="46" width="16" height="62"/><rect x="194" y="38" width="16" height="70"/></g>
        <g fill="#326b93"><circle cx="62" cy="70" r="5"/><circle cx="102" cy="78" r="5"/><circle cx="142" cy="44" r="5"/><circle cx="182" cy="52" r="5"/><circle cx="228" cy="24" r="5"/></g>'''
    elif kind == "learning":
        edges = ""
        for a in (28, 62, 96):
            for b in (15, 46, 77, 108):
                edges += f'<path d="M42 {a} 110 {b}" stroke="#c4d7e5" stroke-dasharray="2 3"/>'
        for a in (15, 46, 77, 108):
            for b in (28, 62, 96):
                edges += f'<path d="M110 {a} 183 {b}" stroke="#c4d7e5"/>'
        shape = edges + '''<path d="M42 28 110 46 183 28M42 62 110 77 183 62M42 96 110 77 183 96" stroke="#326b93" stroke-width="2"/>
        <g fill="#f5f8fb" stroke="#95b1c9"><circle cx="42" cy="28" r="6"/><circle cx="42" cy="62" r="6"/><circle cx="42" cy="96" r="6"/><circle cx="110" cy="15" r="6"/><circle cx="110" cy="108" r="6"/><circle cx="183" cy="28" r="6"/><circle cx="183" cy="62" r="6"/><circle cx="183" cy="96" r="6"/></g>
        <g fill="#326b93"><circle cx="110" cy="46" r="7"/><circle cx="110" cy="77" r="7"/></g>
        <path d="M206 26h22M206 34h14M206 60h22M206 68h17M206 94h22M206 102h10" stroke="#9bb4c8"/>'''
    else:
        shape = '''<g stroke="#acc8dd"><path d="M24 95 47 54 93 79 133 31 171 61 217 29M47 54 78 17 133 31M93 79 125 106 171 61 216 100"/><path d="M24 95 93 79M47 54 133 31M93 79 171 61M171 61 217 29"/></g>
        <g fill="#dcebf6" stroke="#a7c3d8"><circle cx="24" cy="95" r="12"/><circle cx="47" cy="54" r="18"/><circle cx="78" cy="17" r="9"/><circle cx="93" cy="79" r="15"/><circle cx="133" cy="31" r="19"/><circle cx="125" cy="106" r="8"/><circle cx="171" cy="61" r="16"/><circle cx="217" cy="29" r="10"/><circle cx="216" cy="100" r="13"/></g>
        <g fill="#326b93"><circle cx="47" cy="54" r="6"/><circle cx="133" cy="31" r="6"/><circle cx="93" cy="79" r="5"/><circle cx="171" cy="61" r="5"/></g>
        <path d="M109 22h7M111 18v8M43 79h8M47 75v8M185 96h8M189 92v8" stroke="#95b8d2"/>'''
    return "<svg " + common + ">" + shape + "</svg>"

def header(lang, archive=False):
    is_en = lang == "en"
    home = "index_e.html" if is_en else "index.html"
    ja = "publications.html" if archive else "index.html"
    en = "publications_e.html" if archive else "index_e.html"
    navs = [("research", "Research" if is_en else "研究"), ("publications", "Publications" if is_en else "論文"),
            ("profile", "Profile" if is_en else "略歴"), ("activities", "Activities" if is_en else "教育・活動"),
            ("contact", "Contact")]
    nav_html = "".join('<a href="' + (home if archive else "") + "#" + key + '">' + value + "</a>" for key, value in navs)
    language = '<a href="' + ja + '" lang="ja" hreflang="ja">JA</a><span aria-hidden="true">/</span><span aria-current="page">EN</span>' if is_en else '<span aria-current="page">JA</span><span aria-hidden="true">/</span><a href="' + en + '" lang="en" hreflang="en">EN</a>'
    return f'''<a class="skip" href="#main">{"Skip to content" if is_en else "本文へ移動"}</a>
    <header class="site-header"><div class="container header-inner">
    <a class="brand" href="{home}" aria-label="Takayoshi Yamashita — Home"><span class="brand-mark">MPRG</span><span class="brand-name">TAKAYOSHI<br>YAMASHITA</span></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav">{"Menu" if is_en else "メニュー"} ☰</button>
    <nav class="site-nav" id="site-nav" aria-label="{"Main navigation" if is_en else "メインメニュー"}">{nav_html}<div class="language" aria-label="Language">{language}</div></nav>
    </div></header>'''

def footer(lang):
    is_en = lang == "en"
    return f'''<footer class="site-footer"><div class="container footer-inner"><p>© 2026 Takayoshi Yamashita. Chubu University.</p><div>
    {external(LINKS["lab"], "MPRG ↗")}{external(LINKS["university"], "Chubu University ↗" if is_en else "中部大学 ↗")}
    <span>{"Updated" if is_en else "更新"} {UPDATED}</span></div></div></footer><script src="assets/site.js" defer></script>'''

def document(lang, body, archive=False):
    is_en = lang == "en"
    filename = ("publications_e.html" if is_en else "publications.html") if archive else ("index_e.html" if is_en else "index.html")
    title = ("Publications | " if archive else "") + ("Takayoshi Yamashita | Chubu University, MPRG" if is_en else ("研究業績 | " if archive else "") + "山下隆義 | 中部大学 MPRG")
    if not is_en and archive:
        title = "研究業績 | 山下隆義 | 中部大学 MPRG"
    description = ("Takayoshi Yamashita, Professor at Chubu University. Computer vision, autonomous driving, efficient and explainable learning, and AI for biology."
                   if is_en else "中部大学 工学部情報工学科 教授、山下隆義の個人ページ。画像認識、自動運転、機械学習の効率化と説明可能性、生命科学の研究・論文・教育活動を紹介します。")
    schema = {"@context": "https://schema.org", "@type": "Person", "name": "Takayoshi Yamashita", "alternateName": "山下隆義",
              "jobTitle": "Professor", "url": CANONICAL,
              "affiliation": {"@type": "Organization", "name": "Chubu University"},
              "sameAs": [LINKS["profile"], LINKS["scholar"], LINKS["researchmap"], LINKS["dblp"]]}
    return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(description)}"><meta name="theme-color" content="#f5f8fb">
<link rel="canonical" href="{e(CANONICAL + filename)}"><link rel="alternate" hreflang="ja" href="{e(CANONICAL + ("publications.html" if archive else "index.html"))}"><link rel="alternate" hreflang="en" href="{e(CANONICAL + ("publications_e.html" if archive else "index_e.html"))}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:type" content="profile"><meta property="og:url" content="{e(CANONICAL + filename)}">
<meta property="og:image" content="{e(CANONICAL + "assets/portrait.jpeg")}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/style.css"><link rel="stylesheet" href="assets/awards.css"><link rel="stylesheet" href="assets/publications.css">
<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head><body>
{header(lang, archive)}{body}{footer(lang)}</body></html>'''

def section_title(num, label, title):
    return f'<div><p class="section-kicker"><span>{num}</span> {label}</p><h2>{title}</h2></div>'

def filter_bar(lang):
    labels = {"all": "All" if lang == "en" else "すべて", "vision": "Vision" if lang == "en" else "画像認識",
              "driving": "Driving" if lang == "en" else "自動運転", "learning": "Learning" if lang == "en" else "機械学習",
              "biology": "Biology" if lang == "en" else "生命科学",
              "education": "Learning Analytics" if lang == "en" else "ラーニングアナリティクス"}
    return '<div class="filter-bar" role="group" aria-label="' + ("Research field" if lang == "en" else "論文の研究分野") + '">' + "".join(
        f'<button class="filter-chip" type="button" data-filter="{k}" aria-pressed="{"true" if k=="all" else "false"}">{v}</button>' for k,v in labels.items()) + '</div>'

def render_paper(p, lang, archive=False):
    venue = p.get("venue_short", p["venue"])
    citation = '<p class="citation-details">' + e(p["venue"]) + '</p>' if venue != p["venue"] else ""
    authors = ", ".join("<strong>" + e(a) + "</strong>" if "".join(a.split()) in {"TakayoshiYamashita", "山下隆義"} else e(a) for a in p["authors"])
    links = external(p["url"], "Paper ↗")
    if p.get("project"):
        links += external(p["project"], "Project ↗")
    if p.get("code"):
        links += external(p["code"], "Code ↗")
    summary = p.get("summary_en" if lang == "en" else "summary_ja", "")
    summary_html = '<p class="paper-summary">' + e(summary) + '</p>' if summary else ""
    award = '<p class="paper-award">' + e(p["award"]) + '</p>' if p.get("award") else ""
    paper_type = p.get("type", "conference")
    type_names = {"journal": ("雑誌論文", "Journal article"), "conference": ("国際会議", "Conference paper"), "workshop": ("ワークショップ", "Workshop paper"), "domestic": ("国内学会", "Domestic conference"), "meeting": ("研究会", "Technical meeting")}
    type_label = type_names[paper_type][1 if lang == "en" else 0]
    heading = "h4" if archive else "h3"
    return f'''<article class="paper" id="{e(p["id"])}" data-category="{e(p["category"])}" data-year="{p["year"]}" data-type="{e(paper_type)}">
    <div class="paper-venue">{e(venue)}<span class="year">{p["year"]}</span><span class="paper-type">{type_label}</span></div>
    <div class="paper-body">{award}<{heading}>{external(p["url"],e(p["title"]))}</{heading}><p class="authors">{authors}</p>{citation}
    {summary_html}</div><div class="paper-links">{links}</div></article>'''

def main_page(lang):
    en = lang == "en"
    pub_file = "publications_e.html" if en else "publications.html"
    home_title = "Takayoshi<br>Yamashita" if en else "山下 隆義"
    roman = "山下 隆義" if en else "Takayoshi Yamashita"
    affiliation = "Professor, Department of Computer Science<br><small>College of Engineering, Chubu University</small>" if en else "中部大学 工学部 情報工学科 教授<br><small>Machine Perception and Robotics Group（MPRG）</small>"
    description = ("I study computer vision and machine learning at MPRG, Chubu University. From autonomous driving to single-cell biology, my research connects learning algorithms with the challenges of the real world."
                   if en else "画像認識と機械学習を通じて、人と世界を理解するAIを研究しています。自動運転から生命科学まで、実世界の課題と学習アルゴリズムをつなぎます。")
    research = [
        ("education", "教育支援・ラーニングアナリティクス", "Learning analytics", "学習ログや振り返りの分析から、学習状況の把握・成績予測・早期の支援につなげます。教育データを活かして、学び手と教員を支える技術に取り組みます。", "Analyzing learning logs and student reflections to understand learning progress, predict performance, and support learners early.", "Learning analytics · Educational data mining"),
        ("driving", "自動運転・環境理解", "Autonomous driving", "道路シーンの認識とリスク評価、3次元シーンの再構成。安全な自動運転を支える知覚・評価技術に取り組みます。", "Road-scene perception, risk assessment, and 3D reconstruction for safer autonomous systems and realistic simulation.", "Scene understanding · 3D reconstruction"),
        ("learning", "機械学習の効率化・適応", "Efficient & adaptive learning", "モデルの軽量化と継続学習。限られた計算資源を生かし、変化するデータから学び続ける仕組みを探究します。", "Model compression and continual learning: using limited computing resources effectively and learning from changing data.", "Model compression · Continual learning"),
        ("biology", "生命科学・遺伝子発現", "AI for biology", "単一細胞の遺伝子発現から細胞の状態を学習。Mouse-Geneformerを通じ、細胞種分類とin silico摂動解析に取り組みます。", "Learning from single-cell gene expression. Mouse-Geneformer supports cell-type classification, in silico perturbation analysis, and cross-species research.", "Single-cell analysis · Geneformer"),
    ]
    cards = ""
    for i,(key,ja_title,en_title,ja_text,en_text,keywords) in enumerate(research,1):
        cards += f'''<article class="research-card" id="field-{key}">{icon(key)}<span class="number">0{i}</span><h3>{en_title if en else ja_title}</h3>
        <p>{en_text if en else ja_text}</p><div class="keywords">{keywords}</div><a href="{pub_file}?category={key}">{"Explore papers" if en else "関連論文を見る"} <span aria-hidden="true">↗</span></a></article>'''
    milestones = [
        ("2021.04 —", "中部大学 教授", "工学部 情報工学科", "Professor, Chubu University", "Department of Computer Science"),
        ("2017.04", "中部大学 准教授", "工学部 情報工学科", "Associate Professor, Chubu University", "Department of Computer Science"),
        ("2014.04", "中部大学 講師", "同年、MPRGの活動を開始", "Lecturer, Chubu University", "MPRG launched in the same year"),
        ("2011.03", "博士（工学）", "中部大学大学院 工学研究科", "Ph.D. in Engineering", "Chubu University"),
        ("2002 — 2014", "オムロン株式会社", "画像認識技術の研究開発", "OMRON Corporation", "Research and development in computer vision"),
        ("2002.03", "奈良先端科学技術大学院大学 修了", "博士前期課程", "Master's degree, NAIST", "Master’s program"),
    ]
    timeline = "".join(f'<li><time>{time}</time><div><strong>{et if en else jt}</strong><p>{ed if en else jd}</p></div></li>' for time,jt,jd,et,ed in milestones)
    career_records = "".join("<li>" + e(x) + "</li>" for x in RECORDS["career"])
    awards_records = "".join("<li>" + e(x) + "</li>" for x in reversed(RECORDS["awards"]))
    awards = [
        ("2020", "電子情報通信学会 論文賞", "IEICE Best Paper Award"),
        ("2019 · 2020", "MIRU 長尾賞", "MIRU Nagao Award"),
        ("2019", "MIRU フロンティア賞", "MIRU Frontier Award"),
        ("2013", "IEICE ISS 論文賞・PRMU 研究奨励賞", "IEICE ISS Best Paper & PRMU Research Encouragement Awards"),
        ("2009", "SSII 高木賞", "SSII Takagi Award"),
    ]
    award_highlight = f'''<article class="award-highlight">
    <time datetime="2026-08-20">2026.08.20</time>
    <h4>ICPR 2026<br>Best Industry Related Paper Award</h4>
    <p class="award-paper-label">{"Award-winning paper" if en else "受賞論文"}</p>
    <p class="award-paper">{external("https://link.springer.com/chapter/10.1007/978-3-032-31666-0_10","Few-shot Adaptive Open-set Object Detection with Personalized Scene Generation ↗")}</p>
    <p class="authors">Yuzuru Nakamura, Yasunori Ishii, <strong>Takayoshi Yamashita</strong></p>
    </article>'''
    award_grid = award_highlight + "".join(f'<p class="award"><time>{year}</time>{et if en else jt}</p>' for year,jt,et in awards)
    intro = ("My work spans computer vision and machine learning, with applications in autonomous driving and life sciences. I joined Chubu University in 2014 after working at OMRON and became a professor in 2021."
             if en else "専門はコンピュータビジョンと機械学習。オムロンでの研究開発を経て2014年に中部大学へ着任し、2021年より教授を務めています。基礎的な手法の研究と、実世界への応用に取り組んでいます。")
    education_title = "Sharing the foundations of AI" if en else "AIの基礎から実践まで、学びをつなぐ"
    education_text = ("I teach image processing, computer vision, and artificial intelligence. Through lectures, tutorials, and writing, I help students and practitioners understand and apply deep learning."
                      if en else "画像情報処理、コンピュータビジョン、AIの基礎・実践を担当。講義、チュートリアル、書籍を通じて、深層学習の仕組みと活用を伝えています。")
    community_text = ("Board Director of the Japan Deep Learning Association (JDLA) since July 2025. I contribute to AI education and the connection between research and practice."
                      if en else "2025年7月より日本ディープラーニング協会（JDLA）理事。AI人材の育成と、研究成果の社会への普及に取り組んでいます。")
    contact_text = ("For research collaboration, graduate study, or speaking invitations, please contact me by email."
                    if en else "共同研究、大学院への進学、講演などのご相談は、メールでお気軽にお問い合わせください。")
    featured = sorted((p for p in PAPERS if p.get("featured")), key=lambda p: p["featured"])
    full_papers = "".join(render_paper(p,lang) for p in featured)
    return f'''<main id="main">
    <section class="hero"><div class="container"><div class="hero-grid"><div>
      <p class="eyebrow">CHUBU UNIVERSITY / MPRG</p><h1>{home_title}</h1><p class="roman">{roman}</p><p class="affiliation">{affiliation}</p>
      <p class="hero-description">{description}</p><div class="hero-actions"><a class="button" href="#research">{"Explore research" if en else "研究について"} <span aria-hidden="true">→</span></a><a class="text-link" href="{pub_file}">{"Publications" if en else "研究業績を見る"} <span aria-hidden="true">↗</span></a></div>
      <div class="external-links">{external(LINKS["scholar"],"Google Scholar ↗")}{external(LINKS["researchmap"],"researchmap ↗")}{external(LINKS["lab"],"MPRG ↗")}</div>
    </div><figure class="portrait-wrap"><img src="assets/portrait.jpeg" width="600" height="600" alt="{"Takayoshi Yamashita at his laboratory" if en else "研究室での山下隆義"}" fetchpriority="high"><figcaption><span>MACHINE PERCEPTION &amp; ROBOTICS GROUP</span><span>CHUBU UNIV.</span></figcaption></figure></div>
    <div class="hero-foot"><div class="topics"><span>COMPUTER VISION</span><span>MACHINE LEARNING</span><span>AI FOR SCIENCE</span></div><p>KASUGAI, AICHI, JAPAN</p></div></div></section>
    <section class="section" id="research"><div class="container"><div class="section-heading">{section_title("01","RESEARCH","Research interests" if en else "研究領域")}<p>{"From visual recognition to learning systems.<br>Connecting fundamental research with real-world problems." if en else "認識の仕組みを深め、現実の課題へ。<br>基礎研究と応用研究の両面から取り組みます。"}</p></div><div class="research-grid">{cards}</div></div></section>
    <section class="section papers-section" id="publications"><div class="container"><div class="section-heading">{section_title("02","SELECTED PUBLICATIONS","Selected publications" if en else "主な論文・研究成果")}<a class="text-link" href="{pub_file}">{f"Browse all {len(PAPERS)} papers" if en else f"論文一覧・検索（{len(PAPERS)}件）"} <span aria-hidden="true">↗</span></a></div>
    {filter_bar(lang)}<div class="paper-list">{full_papers}</div><p class="empty-state" id="no-papers" role="status" hidden>{"No papers in this field." if en else "この分野の論文はありません。"}</p>
    <div class="paper-footer"><p>{f"{len(featured)} selected papers. Browse the full list for publications by year, type, and research field." if en else f"主な論文{len(featured)}件を紹介しています。論文一覧では、発表年・種別・研究分野で絞り込めます。"}</p><a class="text-link" href="{pub_file}">{f"All {len(PAPERS)} papers" if en else f"すべての論文を見る（{len(PAPERS)}件）"} ↗</a></div></div></section>
    <section class="section profile-section" id="profile"><div class="container"><div class="profile-layout"><div class="profile-intro">
    {section_title("03","PROFILE","Background" if en else "略歴・プロフィール")}<p class="serif-quote">From industry<br>to academia.</p><p>{intro}</p>
    <div class="profile-links">{external(LINKS["profile"],"University profile ↗" if en else "大学教員情報 ↗","text-link")}{external(LINKS["researchmap"],"researchmap ↗","text-link")}</div></div>
    <div><ol class="timeline">{timeline}</ol><details class="record-details"><summary>{"Full academic record (Japanese)" if en else "学歴・職歴の詳細"}</summary><ul>{career_records}</ul></details></div></div>
    <div class="awards-row" id="awards"><h3>{"Selected awards" if en else "主な受賞"}</h3><div class="award-grid">{award_grid}</div><details class="record-details awards-details"><summary>{"Full awards record (Japanese)" if en else "受賞歴の詳細"}</summary><ul>{awards_records}</ul></details></div>
    </div></section>
    <section class="section" id="activities"><div class="container"><div class="section-heading">{section_title("04","EDUCATION & ACTIVITIES","Education & activities" if en else "教育・社会活動")}<p>{"Making AI research accessible to students, engineers, and society." if en else "研究で得た知識を、学生・技術者・社会へ。"}</p></div>
    <div class="activities-layout"><div><article class="activity"><p class="label">EDUCATION</p><h3>{education_title}</h3><p>{education_text}</p>{external(LINKS["about"]+"#professor","Teaching at MPRG ↗" if en else "MPRGの教育・研究活動 ↗","text-link")}</article>
    <article class="activity"><p class="label">COMMUNITY</p><h3>{"Japan Deep Learning Association" if en else "日本ディープラーニング協会（JDLA）"}</h3><p>{community_text}</p>{external(LINKS["jdla_news"],"Board appointment ↗" if en else "理事就任のお知らせ ↗","text-link")}</article></div>
    <aside class="book"><a href="{LINKS["book"]}" target="_blank" rel="noopener noreferrer"><img src="assets/book-cover.jpg" width="349" height="500" loading="lazy" alt="イラストで学ぶ ディープラーニング 改訂第2版 書影"></a><div><p class="label">SELECTED BOOK</p><h3>イラストで学ぶ<br>ディープラーニング<br><small>{"2nd edition" if en else "改訂第2版"}</small></h3><p class="book-meta">{"Takayoshi Yamashita · Kodansha<br>2018 · In Japanese" if en else "山下隆義 著 ／ 講談社<br>2018年11月刊"}</p>{external(LINKS["book"],"Publisher ↗" if en else "書籍について ↗","text-link")}</div></aside></div>
    </div></section>
    <section class="section contact-section" id="contact"><div class="container contact-grid"><div>{section_title("05","GET IN TOUCH","Let's connect." if en else "お問い合わせ")}<p class="contact-intro">{contact_text}</p>
    <div class="email-row"><a class="email" href="mailto:takayoshi@isc.chubu.ac.jp">takayoshi@isc.chubu.ac.jp</a><button class="copy-email" type="button">{"Copy" if en else "コピー"}</button></div><p class="copy-status" id="copy-status" role="status"></p></div>
    <div class="contact-info"><p><strong>{"Chubu University" if en else "中部大学 工学部 情報工学科"}</strong>{"Department of Computer Science<br>Machine Perception and Robotics Group" if en else "Machine Perception and Robotics Group（MPRG）"}</p><p>{"1200 Matsumoto-cho, Kasugai, Aichi<br>487-0027, Japan" if en else "〒487-0027 愛知県春日井市松本町1200"}<br>{"Tel. +81-568-51-9670 (ext. 4410)" if en else "電話：0568-51-9670（内線4410）"}</p>{external(LINKS["about"]+"#access","Access to MPRG ↗" if en else "MPRGへのアクセス ↗")}</div></div></section>
    </main>'''

def archive_page(lang):
    en = lang == "en"
    category_names = {"学術論文":"Journal articles","国際会議":"International conferences","国内発表":"Domestic conferences","研究会発表":"Technical meetings","解説論文":"Review articles","チュートリアル/講演":"Tutorials & talks","書籍":"Books","特許":"Patents"}
    groups = defaultdict(list)
    for item in ARCHIVE:
        groups[item["category"]].append(item["text"])
    archive_html = ""
    for category, items in groups.items():
        rows = "".join('<li class="legacy-entry">' + e(x) + "</li>" for x in items)
        label = category_names[category] if en else category
        archive_html += f'<details class="legacy-group"><summary>{label}<small class="group-count">{len(items)}{" records" if en else "件"}</small></summary><ol class="legacy-list">{rows}</ol></details>'
    sorted_papers = sorted(PAPERS,key=lambda p:-p["year"])
    years = sorted({p["year"] for p in PAPERS}, reverse=True)
    paper_html = ""
    for year in years:
        year_papers = [p for p in sorted_papers if p["year"] == year]
        rows = "".join(render_paper(p,lang,True) for p in year_papers)
        paper_html += f'<section class="publication-year" data-year="{year}" aria-labelledby="pub-year-{year}"><div class="year-heading"><h3 id="pub-year-{year}">{year}</h3><p><span class="year-count">{len(year_papers)}</span>{" papers" if en else "件"}</p></div><div class="paper-list">{rows}</div></section>'
    year_options = '<option value="all">' + ("All years" if en else "すべての年") + '</option>' + "".join(f'<option value="{year}">{year}</option>' for year in years)
    type_options = [("all", "すべての種別", "All types"), ("journal", "雑誌論文・解説", "Journal & review articles"), ("conference", "国際会議", "Conference papers"), ("workshop", "ワークショップ", "Workshop papers"), ("domestic", "国内学会", "Domestic conferences"), ("meeting", "研究会", "Technical meetings")]
    types_html = "".join(f'<option value="{key}">{english if en else japanese}</option>' for key,japanese,english in type_options)
    stats = type_options[1:]
    stats_html = "".join(f'<div><strong>{sum(p.get("type")==key for p in PAPERS)}</strong><span>{english if en else japanese}</span></div>' for key,japanese,english in stats)
    description = ("Journal and review articles, international conference papers, workshop papers, and domestic conference and technical-meeting presentations from 2020–2026. Earlier publications, presentations, books, and patents are collected in the historical record below."
                   if en else "2020〜2026年の雑誌論文・解説・国際会議・ワークショップ・国内学会・研究会の業績を掲載しています。2019年以前の論文・国内発表・書籍・特許は、下部の「過去の業績」にまとめています。")
    return f'''<main id="main"><section class="container archive-hero"><p class="eyebrow">TAKAYOSHI YAMASHITA / RESEARCH</p><h1>{"Publications & archive" if en else "研究業績"}</h1><p>{description}</p><div class="publication-stats"><div class="stat-total"><strong>{len(PAPERS)}</strong><span>{"Papers" if en else "掲載論文"}</span></div>{stats_html}</div><div class="archive-external">{external(LINKS["scholar"],"Google Scholar ↗")}{external(LINKS["dblp"],"DBLP ↗")}{external(LINKS["profile"],"University profile ↗" if en else "大学教員情報 ↗")}</div></section>
    <div class="search-panel"><div class="container"><div class="search-box"><label for="publication-search">{"Search" if en else "業績検索"}</label><input type="search" id="publication-search" placeholder="{"Title, author, venue, or year" if en else "論文名・著者・会議名・年で検索"}" autocomplete="off"><button type="button" id="reset-search">{"Reset" if en else "リセット"}</button></div><p id="search-status" class="search-status" role="status">{f"{len(PAPERS)} papers · {len(ARCHIVE)} historical records" if en else f"論文 {len(PAPERS)}件 ・ 過去の業績 {len(ARCHIVE)}件"}</p></div></div>
    <div class="container archive-main"><noscript><p class="no-js-note">{"All records are available below. Enable JavaScript to search and filter." if en else "すべての業績は下に掲載しています。検索・絞り込みにはJavaScriptを有効にしてください。"}</p></noscript><h2>{"Papers by year" if en else "論文一覧"}</h2><p class="subheading">{"Browse papers by year, publication type, and research field. Titles link to the published papers." if en else "発表年・論文種別・研究分野で絞り込めます。各タイトルから論文ページへ移動できます。"}</p>
    <div class="publication-controls"><div class="select-field"><label for="publication-year">{"Year" if en else "発表年"}</label><select id="publication-year">{year_options}</select></div><div class="select-field"><label for="publication-type">{"Publication type" if en else "論文種別"}</label><select id="publication-type">{types_html}</select></div></div>
    {filter_bar(lang)}<div class="publication-years">{paper_html}</div><p class="empty-state" id="no-papers" role="status" hidden>{"No papers match these filters. Try another year, type, field, or search term." if en else "条件に一致する論文はありません。発表年・種別・研究分野・検索語を変更してください。"}</p>
    <section class="legacy-area" id="historical-record"><h2>{"Historical record" if en else "過去の業績"}</h2><p class="subheading">{f"{len(ARCHIVE)} records inherited from the previous website, in their original publication languages. Keyword search applies to these records; the year, type, and field filters apply to the paper list above. Some papers appear in both lists." if en else f"旧ページの{len(ARCHIVE)}件を区分別に掲載しています。上部の検索欄でキーワード検索ができます（発表年・種別・分野の絞り込みは上の論文一覧が対象です）。一部の論文は両方の一覧に含まれます。"}</p>{archive_html}</section>
    <div class="archive-back"><a class="text-link" href="{"index_e.html" if en else "index.html"}">← {"Back to profile" if en else "プロフィールに戻る"}</a></div></div></main>'''

if __name__ == "__main__":
    DIST.mkdir(exist_ok=True)
    for lang in ("ja","en"):
        filename = "index_e.html" if lang == "en" else "index.html"
        (DIST / filename).write_text(document(lang,main_page(lang)),encoding="utf-8")
        filename = "publications_e.html" if lang == "en" else "publications.html"
        (DIST / filename).write_text(document(lang,archive_page(lang),True),encoding="utf-8")
    print(f"Built 4 pages; {len(PAPERS)} papers ({sum(bool(p.get('featured')) for p in PAPERS)} featured); {len(ARCHIVE)} archived records; {len(RECORDS['career'])} career records; {len(RECORDS['awards'])} awards.")
