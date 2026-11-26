#!/usr/bin/env python3
"""Generates the README's animated SVG panels (light + dark) into assets/ and assets/dark/.
Run: python3 assets/build.py   (edit the CONTENT section, re-run, commit the SVGs).
Animations are pure CSS inside the SVG (GitHub renders them) and respect prefers-reduced-motion."""
import os
import textwrap
from xml.sax.saxutils import escape

W, M = 900, 28
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
THEMES = {
    "light": dict(fg="#1f2328", dim="#59636e", line="#d1d9e0", acc="#4f46e5", card="#f6f8fa", acc2="#0969da"),
    "dark": dict(fg="#e6edf3", dim="#9198a1", line="#30363d", acc="#22d3ee", card="#151b23", acc2="#79c0ff"),
}

# ---------------- CONTENT ----------------
NAME = "HUSNAIN ALI"
ROLES = [  # header cycles through these
    "Principal Software Engineer",
    "Senior iOS Engineer & Mobile Architect",
    "Platform Engineer · DevSecOps",
    "AWS DevOps Pro · Claude Certified Architect",
]
FOCUS = "ci/cd · kubernetes · devsecops · swift · aws · azure"
TICKS = ["IOS & SWIFT", "CLOUD & DEVOPS", "PLATFORM ENGINEERING"]

WHOAMI = [
    "Principal software engineer with 9+ years building scalable systems,",
    "working where mobile engineering meets cloud and DevOps.",
    "Clean, modular, testable architecture and automated, secure delivery.",
]
WHOAMI_ROWS = [
    ("MOBILE", "30+ native & hybrid apps across FinTech, Healthcare, Aviation and AR/VR. 4.5+ App Store ratings."),
    ("DEVOPS", "CI/CD, Infrastructure as Code and cloud-native architecture on AWS and Azure."),
    ("ARCH", "MVVM-C, Clean, VIPER and TDD. Scaled to 100K+ users at under 2% crash rate."),
    ("SECURITY", "PCI-DSS and HIPAA compliant infrastructure with shift-left scanning."),
    ("NOW", "Going deeper on Kubernetes and Platform Engineering. Writing on Medium."),
]

IMPACT = [
    ("90%", "Faster releases", "end-to-end CI/CD"),
    ("35%", "Lower infra cost", "serverless migration"),
    ("60%", "Faster provisioning", "infrastructure as code"),
    ("3x", "Deploy frequency", "via GitOps"),
    ("40%", "Less downtime", "proactive observability"),
    ("11", "Microservices", "from one monolith"),
    ("100K+", "Users served", "under 2% crash rate"),
    ("96%", "Stability gain", "Obj-C to Swift"),
]

PROJECT_GROUPS = [
    ("CLOUD & DEVOPS", [
        ("MongoDB on Kubernetes", "Auto-scaling, highly available production database architecture on EKS.", "EKS · MongoDB · Helm"),
        ("Siemens CIAM", "Enterprise customer identity and access management platform.", "EKS · Keycloak"),
        ("EC2 to Serverless", "Lambda and Fargate modernization that cut infrastructure costs by 35%.", "AWS · Lambda · Fargate"),
        ("StayX Microservices", "Decomposed a monolith into 11 scalable microservices.", "AWS · Docker"),
        ("Elasticsearch Cluster", "High-availability search and log infrastructure.", "EKS · Elasticsearch"),
        ("Blue/Green Pipeline", "Zero-downtime CI/CD with instant rollback.", "Jenkins · CI/CD"),
        ("Terraform Automation", "Multi-environment infrastructure provisioning.", "Terraform · Terragrunt"),
        ("LLM Platform", "Scalable LLM API deployment for enterprise apps.", "AWS Bedrock · Python"),
        ("PCI-DSS Compliance", "Secure, audit-ready compliant cloud architecture.", "AWS · Security"),
    ]),
    ("MOBILE", [
        ("FinPay", "FinTech payments app.", "Swift · iOS"),
        ("Healthcare Suite", "MediCare+, HealthTrack 360 and PharmaLink: booking, e-commerce and supply chain.", "Swift · iOS"),
        ("Volocopter Pilot", "Aviation and mobility platform.", "Swift · iOS"),
        ("RENOLIT AXS", "AR-based surface measurement tool for iPad.", "ARKit · iPad"),
        ("KSC App / KSC TV", "Live sports app and live-stream video platform.", "iOS · tvOS"),
        ("Stay Safe / TE to Go", "Workplace safety and supplier collaboration apps.", "Flutter · Dart"),
        ("Jonple · Want It · Mathlete", "Fitness, marketplace and education apps.", "React Native · iOS"),
    ]),
]

STACK = [
    ("LANGUAGES", "Swift · Objective-C · Python · Bash · Node.js · Dart"),
    ("MOBILE", "SwiftUI · UIKit · Combine · RxSwift · React Native · Flutter · ARKit · CoreML"),
    ("CLOUD", "AWS · Azure · Lambda · Fargate · EKS · S3 · RDS · DynamoDB · Bedrock · SageMaker"),
    ("PLATFORM", "Kubernetes · Docker · Helm · Terraform · Terragrunt · Pulumi · ArgoCD · FluxCD"),
    ("CI/CD", "Jenkins · GitHub Actions · GitLab CI · Xcode Cloud · Fastlane"),
    ("SECURITY", "Vault · Keycloak · SonarQube · Trivy · Gitleaks · OWASP · PCI-DSS · HIPAA"),
    ("DATA & OBS", "PostgreSQL · MongoDB · MySQL · Realm · Firebase · Prometheus · Grafana · Datadog"),
]

CERTS = [
    ("2026", "Claude Certified Architect, Foundations", "Anthropic"),
    ("2025", "AWS Certified DevOps Engineer, Professional", "Amazon Web Services"),
    ("2024", "DevOps with AWS · Composable SwiftUI Architecture Using Redux", "LinkedIn Learning"),
    ("2023", "Software Architecture: From Developer to Architect", "LinkedIn Learning"),
    ("2022", "Scalable App Development & Modular Architecture", "Udemy"),
    ("2017", "Certified iOS Mobile Developer", "eVenture Solutions"),
]

FOOTER = "Bridging mobile experiences with cloud-native infrastructure, one pipeline at a time."
# -----------------------------------------

CSS = """
.rise{opacity:0;animation:rise .8s cubic-bezier(.2,.7,.2,1) forwards}
.draw{stroke-dasharray:1;stroke-dashoffset:1;animation:draw 1.4s cubic-bezier(.6,0,.2,1) forwards}
.grow{transform-box:fill-box;transform-origin:left center;transform:scaleX(0);animation:grow 1.2s cubic-bezier(.2,.7,.2,1) forwards}
.rot{opacity:0;animation:rot 16s infinite backwards}
.blink{animation:blink 1.1s steps(1) infinite}
.pulse{animation:pulse 2.4s ease-in-out infinite}
.ring{transform-box:fill-box;transform-origin:center;animation:ring 2.4s ease-out infinite}
@keyframes rise{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
@keyframes draw{to{stroke-dashoffset:0}}
@keyframes grow{to{transform:scaleX(1)}}
@keyframes rot{0%{opacity:0;transform:translateY(8px)}4%,21%{opacity:1;transform:translateY(0)}25%,100%{opacity:0;transform:translateY(-8px)}}
@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}
@keyframes ring{0%{transform:scale(.5);opacity:.8}80%,100%{transform:scale(2.6);opacity:0}}
@media (prefers-reduced-motion:reduce){
 *{animation:none!important}
 .rise,.rot.first{opacity:1}.draw{stroke-dashoffset:0}.grow{transform:none}.ring{opacity:0}.rot:not(.first){display:none}
}
"""


def t(x, y, s, size=13, fill="fg", weight=400, ls=0, anchor="start", fam=MONO, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<text{c} x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{{{fill}}}" '
            f'letter-spacing="{ls}" text-anchor="{anchor}" font-family="{fam}">{escape(s)}</text>')


def line(y, x1=M, x2=W - M, color="line", delay=0.0, sw=1, vertical=False):
    if vertical:
        return (f'<line class="draw" pathLength="1" x1="{x1}" y1="{y}" x2="{x1}" y2="{x2}" stroke="{{{color}}}" '
                f'stroke-width="{sw}" style="animation-delay:{delay}s"/>')
    return (f'<line class="draw" pathLength="1" x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{{{color}}}" '
            f'stroke-width="{sw}" style="animation-delay:{delay}s"/>')


def rise(delay, *parts):
    return f'<g class="rise" style="animation-delay:{delay:.2f}s">' + "".join(parts) + "</g>"


def chips(x, y, items, maxw, size=11.5, h=24, gap=8, delay=0.0, step=0.04):
    """Rounded pills that wrap. Returns (parts, next_y)."""
    parts, cx, d = [], x, delay
    for it in items:
        w = len(it) * size * 0.6 + 20
        if cx + w > x + maxw:
            cx, y = x, y + h + gap
        parts.append(rise(d, f'<rect x="{cx}" y="{y}" width="{w:.0f}" height="{h}" rx="{h/2}" fill="{{card}}" stroke="{{line}}"/>',
                          t(cx + w / 2, y + h / 2 + 4, it, size, "fg", 500, 0, "middle", SANS)))
        cx += w + gap
        d += step
    return parts, y + h


def section(num, label, path):
    label_w = len(label) * 12.5 + 18
    x0 = M + 60 + label_w
    x1 = W - M - len(path) * 6.8 - 14
    return [
        rise(0.0, t(M, 42, num, 36, "acc", 700)),
        rise(0.1, t(M + 62, 38, label, 12, "fg", 700, 5)),
        line(33, x0, x1, delay=0.2),
        rise(0.3, t(W - M, 38, path, 11, "dim", anchor="end")),
    ], 80


def svg(parts, h):
    body = "\n".join(parts)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}">\n'
            f'<style>{CSS}</style>\n{body}\n</svg>\n')


def header():
    y = 58
    p = [rise(0.0, t(M, y, NAME, 50, "fg", 800, 3))]
    for i, r in enumerate(ROLES):
        cls = "rot first" if i == 0 else "rot"
        p.append(f'<g class="{cls}" style="animation-delay:{i*4}s">' +
                 t(M, y + 40, r, 20, "acc", 600, 0, fam=SANS) + "</g>")
    p.append(f'<rect class="blink" x="{M}" y="{y + 59}" width="8" height="14" fill="{{acc}}"/>')
    p.append(rise(0.4, t(M + 18, y + 70, FOCUS, 12, "dim")))
    p.append(line(y + 94, delay=0.5))
    n = len(TICKS)
    for i, s in enumerate(TICKS):
        anchor = "start" if i == 0 else ("end" if i == n - 1 else "middle")
        x = M if i == 0 else (W - M if i == n - 1 else W / 2)
        p.append(rise(0.7 + i * 0.1, t(x, y + 116, s, 10, "dim", 400, 3, anchor)))
    p.append(line(y + 128, delay=0.9))
    return p, y + 146


def whoami():
    p, y = section("01", "WHOAMI", "~/01-whoami")
    d = 0.3
    for ln in WHOAMI:
        p.append(rise(d, t(M, y, ln, 16, "fg", 400, 0, fam=SANS))); y += 27; d += 0.08
    y += 10
    p.append(line(y, delay=d)); y += 14
    for k, v in WHOAMI_ROWS:
        p.append(rise(d, f'<rect x="{M}" y="{y}" width="{W - 2*M}" height="46" rx="8" fill="{{card}}"/>',
                      t(M + 18, y + 28, k, 11, "acc", 700, 2),
                      t(M + 130, y + 28, v, 14, "fg", 400, 0, fam=SANS)))
        y += 54; d += 0.08
    return p, y + 6


def impact():
    p, y = section("02", "IMPACT", "~/02-impact")
    gap = 12
    cw = (W - 2 * M - 3 * gap) / 4
    for i, (big, lab, sub) in enumerate(IMPACT):
        cx, cy = M + (i % 4) * (cw + gap), y + (i // 4) * 124
        d = 0.3 + i * 0.07
        p.append(rise(d,
                      f'<rect x="{cx:.0f}" y="{cy}" width="{cw:.0f}" height="112" rx="10" fill="{{card}}" stroke="{{line}}"/>',
                      t(cx + 20, cy + 50, big, 38, "acc", 800),
                      t(cx + 20, cy + 76, lab, 14, "fg", 600, 0, fam=SANS),
                      t(cx + 20, cy + 95, sub, 12, "dim", 400, 0, fam=SANS)))
        p.append(f'<rect class="grow" x="{cx + 20:.0f}" y="{cy + 104}" width="{cw - 40:.0f}" height="3" rx="1.5" '
                 f'fill="{{acc}}" opacity=".55" style="animation-delay:{d + 0.4:.2f}s"/>')
    return p, y + 2 * 124


def projects():
    p, y = section("03", "PROJECTS", "~/03-projects")
    gap = 14
    cw = (W - 2 * M - gap) / 2
    ch = 132
    d = 0.3
    for gname, items in PROJECT_GROUPS:
        p.append(rise(d, f'<circle cx="{M + 4}" cy="{y - 4}" r="4" fill="{{acc}}"/>', t(M + 18, y, gname, 12, "fg", 700, 4)))
        y += 20
        for i, (name, desc, tags) in enumerate(items):
            cx, cy = M + (i % 2) * (cw + gap), y + (i // 2) * (ch + gap)
            lines = textwrap.wrap(desc, 56)[:2]
            parts = [f'<rect x="{cx:.0f}" y="{cy}" width="{cw:.0f}" height="{ch}" rx="12" fill="{{card}}" stroke="{{line}}"/>',
                     t(cx + 20, cy + 32, name, 16, "fg", 700, 0, fam=SANS)]
            for j, ln in enumerate(lines):
                parts.append(t(cx + 20, cy + 56 + j * 19, ln, 13, "dim", 400, 0, fam=SANS))
            cx2 = cx + 20
            for tg in tags.split(" · "):
                w = len(tg) * 6.8 + 18
                parts.append(f'<rect x="{cx2:.0f}" y="{cy + 94}" width="{w:.0f}" height="22" rx="11" fill="none" stroke="{{acc}}" opacity=".6"/>')
                parts.append(t(cx2 + w / 2, cy + 109, tg, 11, "acc", 600, 0, "middle", SANS))
                cx2 += w + 8
            p.append(rise(d + (i // 2) * 0.12 + (i % 2) * 0.05, *parts))
        rows = (len(items) + 1) // 2
        y += rows * (ch + gap) + 14
        d += 0.2
    return p, y - 6


def stack():
    p, y = section("04", "STACK", "~/04-stack")
    d = 0.3
    for k, v in STACK:
        items = v.split(" · ")
        cp, ny = chips(M + 130, y, items, W - 2 * M - 130, delay=d)
        p.append(rise(d, t(M, y + 16, k, 11, "dim", 700, 2)))
        p += cp
        y = ny + 18
        p.append(line(y - 8, delay=d))
        y += 8
        d += 0.1
    return p, y - 6


def certs():
    p, y = section("05", "CREDENTIALS", "~/05-certifications")
    top = y - 6
    n = len(CERTS)
    row = 62
    p.append(line(top, M + 76, top + n * row - 22, vertical=True, delay=0.3))
    for i, (yr, name, org) in enumerate(CERTS):
        cy = y + i * row
        d = 0.4 + i * 0.12
        parts = [t(M, cy + 5, yr, 14, "acc", 700),
                 f'<circle cx="{M + 76}" cy="{cy}" r="5" fill="{{acc}}"/>',
                 t(M + 100, cy + 5, name, 16, "fg", 600, 0, fam=SANS),
                 t(M + 100, cy + 25, org, 12, "dim", 400, 0, fam=SANS)]
        if i == 0:
            parts.insert(2, f'<circle class="ring" cx="{M + 76}" cy="{cy}" r="5" fill="none" stroke="{{acc}}" stroke-width="2"/>')
        p.append(rise(d, *parts))
    return p, y + n * row - 14


def bare(num, label, path):
    return section(num, label, path)


def footer():
    y = 44
    return [line(10, delay=0.0),
            rise(0.2,
                 f'<circle cx="{M + 6}" cy="{y - 4}" r="5" fill="{{acc}}" class="pulse"/>',
                 f'<circle class="ring" cx="{M + 6}" cy="{y - 4}" r="5" fill="none" stroke="{{acc}}" stroke-width="2"/>',
                 t(M + 24, y, FOOTER, 13, "dim", 400, 0, fam=SANS)),
            ], 72


PANELS = {
    "header": header, "whoami": whoami, "impact": impact, "projects": projects,
    "stack": stack, "certs": certs, "footer": footer,
    "activity": lambda: bare("06", "ACTIVITY", "~/06-activity"),
    "writing": lambda: bare("07", "WRITING", "~/07-writing"),
}

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(here, "dark"), exist_ok=True)
    for name, fn in PANELS.items():
        parts, h = fn()
        for theme, c in THEMES.items():
            out = os.path.join(here, "dark" if theme == "dark" else "", f"{name}.svg")
            s = svg(parts, h)
            for k, v in c.items():
                s = s.replace("{" + k + "}", v)
            with open(out, "w") as f:
                f.write(s)
    print("ok", len(PANELS) * 2, "svgs")
