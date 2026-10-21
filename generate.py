import re, html, pathlib
src = pathlib.Path.home().joinpath("Developer/Meal Snap/files/Meal Snap/iOS/MealSnap/Features/Legal/LegalView.swift").read_text()
EMAIL = "weletpojulu@gmail.com"
UPDATED = "September 19, 2026"

def block(name):
    m = re.search(r'static let %s: \[\(String, String\)\] = \[(.*?)\n    \]' % name, src, re.S)
    return re.findall(r'\("([^"]+)", """\n(.*?)\n"""\)', m.group(1), re.S)
def intro(name):
    return re.search(r'static let %s = """\n(.*?)\n"""' % name, src, re.S).group(1)

def inline(t):
    t = html.escape(t, quote=False)
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
def render(body):
    out, items = [], []
    def flush():
        nonlocal items
        if items: out.append("<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"); items = []
    for para in body.split("\n\n"):
        lines = para.split("\n")
        for ln in lines:
            if ln.startswith("• "): items.append(inline(ln[2:]))
            else:
                flush(); out.append(f"<p>{inline(ln)}</p>")
        flush()
    return "\n".join(out)

CSS = """:root{--ink:#1c2420;--muted:#5b6660;--brand:#2d6a4f;--tint:#e8f1ec;--bg:#f7faf8;--card:#fff;--line:#dbe5df}
@media(prefers-color-scheme:dark){:root{--ink:#e8efeb;--muted:#9aa8a1;--brand:#74c69d;--tint:#1e2e26;--bg:#121815;--card:#1a221e;--line:#2b3731}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
main{max-width:720px;margin:0 auto;padding:32px 16px 64px}
nav{display:flex;gap:16px;flex-wrap:wrap;margin-bottom:28px;font-size:15px}nav a{color:var(--brand);text-decoration:none;font-weight:600}nav a:hover{text-decoration:underline}
h1{font-size:34px;line-height:1.15;margin:0 0 12px}
.date{display:inline-block;background:var(--tint);color:var(--brand);font-size:13px;font-weight:600;padding:5px 12px;border-radius:99px}
.lede{color:var(--muted);margin:16px 0 24px}
section{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:20px 22px;margin:14px 0}
h2{font-size:19px;margin:0 0 10px}h2 span{color:var(--brand)}
section p{margin:0 0 10px}section ul{margin:0 0 10px;padding-left:22px}section li{margin:4px 0}
.contact{background:var(--brand);color:#fff;border-radius:16px;padding:20px 22px;margin-top:20px}.contact h2{color:#fff}.contact a{color:#fff;font-weight:700}
footer{margin-top:32px;color:var(--muted);font-size:13px}"""

NAV = '<nav><a href="index.html">Privacy Policy</a><a href="terms.html">Terms of Use</a><a href="support.html">Support</a></nav>'
def page(fname, title, lede, secs, numbered=True, date=True):
    body = "".join(
        f'<section><h2>{f"<span>{i+1}.</span> " if numbered else ""}{html.escape(h)}</h2>{render(b)}</section>'
        for i, (h, b) in enumerate(secs))
    d = f'<span class="date">Last updated {UPDATED}</span>' if date else ""
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Meal Snap - {title}</title>
<meta name="description" content="Meal Snap {title}">
<style>{CSS}</style></head><body><main>{NAV}
<h1>{title}</h1>{d}<p class="lede">{html.escape(lede)}</p>
{body}
<div class="contact"><h2>Questions?</h2><p>Contact us any time.</p><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
<footer>&copy; 2026 Welet Pojulu. Meal Snap is provided by Welet Pojulu.</footer>
</main></body></html>"""
    pathlib.Path(fname).write_text(doc)

page("index.html", "Privacy Policy", intro("privacyIntro"), block("privacySections"))
page("terms.html", "Terms of Use", intro("termsIntro"), block("termsSections"))
support = [
 ("Contact us", f"Email **{EMAIL}** and we will get back to you as soon as we can. Please include your device model and iOS version if you are reporting a problem."),
 ("Manage or cancel your subscription", "Open your iPhone's Settings, tap your name, then Subscriptions, and choose Meal Snap Pro. Refund requests are handled by Apple at reportaproblem.apple.com."),
 ("Delete your account and data", "In the app, go to Profile > Delete account. Your personal data, including photos, is deleted within 30 days."),
 ("Disconnect Apple Health", "Open the Health app, tap your profile picture, then Apps, and choose Meal Snap to change or remove access."),
]
page("support.html", "Support", "Help with Meal Snap, your account, and your subscription.", support, numbered=False, date=False)
