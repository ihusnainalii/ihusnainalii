#!/usr/bin/env python3
"""Generates the README's terminal-style SVG panels (light + dark) into assets/ and assets/dark/.
Run: python3 assets/build.py   (edit the CONTENT section, re-run, commit the SVGs)."""
import os
from xml.sax.saxutils import escape

W, M = 900, 28
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
THEMES = {
    "light": dict(fg="#1f2328", dim="#656d76", line="#d0d7de", acc="#4f46e5"),
    "dark": dict(fg="#e6edf3", dim="#8b949e", line="#30363d", acc="#22d3ee"),
}

# ---------------- CONTENT ----------------
NAME = "HUSNAIN ALI"
ROLE = "Principal DevOps Engineer — Platform & iOS Architect."
FOCUS = "focus  ·  ci/cd  ·  kubernetes  ·  devsecops  ·  swift  ·  aws"
OPEN = "bridging mobile + cloud  ·  8+ years  ·  30+ apps shipped"
TICKS = ["IOS & SWIFT", "CLOUD & DEVOPS", "PLATFORM ENGINEERING"]

WHOAMI = [
    "principal software engineer with 8+ years building scalable systems.",
    "working where mobile engineering meets cloud and devops.",
    "clean, modular, testable architecture. automated, secure delivery.",
]
WHOAMI_ROWS = [
    ("MOBILE", "30+ native & hybrid apps · FinTech · Healthcare · Aviation · AR/VR · 4.5+ ★"),
    ("DEVOPS", "CI/CD · Infrastructure as Code · cloud-native on AWS"),
    ("ARCH", "MVVM-C · Clean · VIPER · TDD · 100K+ users at <2% crash rate"),
    ("SECURITY", "PCI-DSS · HIPAA · SonarQube · Trivy · Gitleaks · OWASP"),
    ("NOW", "Kubernetes & Platform Engineering · writing on Medium"),
]

IMPACT = [
    ("90%", "faster releases", "end-to-end CI/CD"),
    ("35%", "lower infra cost", "serverless migration"),
    ("60%", "faster provisioning", "infrastructure as code"),
    ("3x", "deploy frequency", "GitOps"),
    ("40%", "less downtime", "proactive observability"),
    ("11", "microservices", "from one monolith"),
    ("100K+", "users", "<2% crash rate"),
    ("96%", "stability gain", "Obj-C to Swift"),
]

PROJECTS = [
    ("MONGODB ON KUBERNETES", "Auto-scaling, highly available production database architecture on EKS.", "KUBERNETES · EKS · MONGODB · HELM"),
    ("SIEMENS CIAM", "Enterprise customer identity & access management platform.", "EKS · KEYCLOAK · KUBERNETES"),
    ("EC2 TO SERVERLESS", "Lambda/Fargate modernization that cut infrastructure costs by 35%.", "AWS · LAMBDA · FARGATE"),
    ("STAYX MICROSERVICES", "Decomposed a monolith into 11 scalable microservices.", "AWS · MICROSERVICES · DOCKER"),
    ("ELASTICSEARCH CLUSTER", "High-availability search and log infrastructure.", "EKS · ELASTICSEARCH · OBSERVABILITY"),
    ("BLUE/GREEN PIPELINE", "Zero-downtime CI/CD with instant rollback.", "JENKINS · BLUE/GREEN · CI/CD"),
    ("TERRAFORM AUTOMATION", "Multi-environment infrastructure provisioning.", "TERRAFORM · TERRAGRUNT · IAC"),
    ("LLM PLATFORM", "Scalable LLM API deployment for enterprise apps.", "AWS BEDROCK · PYTHON · API"),
    ("PCI-DSS COMPLIANCE", "Secure, audit-ready compliant cloud architecture.", "AWS · SECURITY · COMPLIANCE"),
    ("FINPAY", "FinTech payments app.", "SWIFT · IOS · PAYMENTS"),
    ("HEALTHCARE SUITE", "MediCare+, HealthTrack 360 and PharmaLink: booking, e-commerce, supply chain.", "SWIFT · IOS · HEALTHCARE"),
    ("VOLOCOPTER PILOT", "Aviation and mobility platform.", "SWIFT · IOS · AVIATION"),
    ("RENOLIT AXS", "AR-based surface measurement tool for iPad.", "ARKIT · SWIFT · IPAD"),
    ("KSC APP / KSC TV", "Live sports app and live-stream video platform.", "SWIFT · IOS · TVOS · STREAMING"),
    ("STAY SAFE / TE TO GO", "Workplace safety and supplier collaboration apps.", "FLUTTER · DART"),
    ("JONPLE · WANT IT · MATHLETE", "Fitness, buy-and-sell marketplace and education/gamification apps.", "REACT NATIVE · SWIFT · IOS"),
]

STACK = [
    ("LANGUAGES", "Swift · Objective-C · Python · Bash · Node.js · Dart"),
    ("MOBILE", "SwiftUI · UIKit · Combine · RxSwift · React Native · Flutter · ARKit · CoreML"),
    ("CLOUD", "AWS · Lambda · Fargate · EKS · S3 · RDS · DynamoDB · Bedrock · SageMaker"),
    ("PLATFORM", "Kubernetes · Docker · Helm · Terraform · Terragrunt · Pulumi · ArgoCD · FluxCD"),
    ("CI/CD", "Jenkins · GitHub Actions · GitLab CI · Xcode Cloud · Fastlane"),
    ("SECURITY", "Vault · Keycloak · SonarQube · Trivy · Gitleaks · OWASP · PCI-DSS · HIPAA"),
    ("DATA & OBS", "PostgreSQL · MongoDB · MySQL · Realm · Firebase · Prometheus · Grafana · Datadog"),
]

CERTS = [
    ("2026", "Claude Certified Architect — Foundations", "Anthropic"),
    ("2025", "AWS Certified DevOps Engineer — Professional", "Amazon Web Services"),
    ("2024", "DevOps with AWS · Composable SwiftUI Architecture Using Redux", "LinkedIn Learning"),
    ("2023", "Software Architecture: From Developer to Architect", "LinkedIn Learning"),
    ("2022", "Scalable App Development & Modular Architecture", "Udemy"),
    ("2017", "Certified iOS Mobile Developer", "eVenture Solutions"),
]

FOOTER = "bridging mobile experiences with cloud-native infrastructure — one pipeline at a time."
# -----------------------------------------


def t(x, y, s, size=13, fill="fg", weight=400, ls=0, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{{{fill}}}" '
            f'letter-spacing="{ls}" text-anchor="{anchor}">{escape(s)}</text>')


def rule(y, color="line", x1=M, x2=W - M, sw=1):
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{{{color}}}" stroke-width="{sw}"/>'


def section(num, label, path):
    """Big number + spaced label + rule + path. Returns (svg parts, next y)."""
    label_w = len(label) * 13 + 26
    x0 = M + 52 + label_w
    return [
        t(M, 40, num, 34, "fg", 700),
        t(M + 56, 38, label, 12, "fg", 700, 5),
        rule(33, x1=x0, x2=W - M - len(path) * 7.4 - 12),
        t(W - M, 38, path, 11, "dim", anchor="end"),
    ], 74


def svg(parts, h):
    body = "\n".join(parts)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" '
            f'font-family="{FONT}">\n{body}\n</svg>\n')


def header():
    p, y = [], 52
    p += [t(M, y, NAME, 46, "fg", 800, 3)]
    p += [t(M, y + 32, ROLE, 15, "fg")]
    p += [t(M, y + 62, FOCUS, 11, "dim"), t(M, y + 80, OPEN, 11, "dim")]
    p += [rule(y + 100)]
    n = len(TICKS)
    for i, s in enumerate(TICKS):
        anchor = "start" if i == 0 else ("end" if i == n - 1 else "middle")
        x = M if i == 0 else (W - M if i == n - 1 else W / 2)
        p += [t(x, y + 120, s, 10, "dim", 400, 3, anchor)]
    p += [rule(y + 132)]
    return p, y + 150


def whoami():
    p, y = section("01", "WHOAMI", "~/01-whoami")
    for line in WHOAMI:
        p.append(t(M, y, line, 13)); y += 22
    y += 6
    p.append(rule(y)); y += 24
    for k, v in WHOAMI_ROWS:
        p += [t(M, y, k, 10, "dim", 400, 2), t(M + 110, y, v, 12)]; y += 26
    return p, y + 4


def impact():
    p, y = section("02", "IMPACT", "~/02-impact")
    cw = (W - 2 * M) / 4
    for i, (big, lab, sub) in enumerate(IMPACT):
        cx, cy = M + (i % 4) * cw, y + (i // 4) * 104
        p += [
            f'<rect x="{cx + 4}" y="{cy}" width="{cw - 8}" height="94" fill="none" stroke="{{line}}"/>',
            t(cx + 18, cy + 44, big, 34, "acc", 700),
            t(cx + 18, cy + 66, lab, 12, "fg", 600),
            t(cx + 18, cy + 82, sub, 10, "dim"),
        ]
    return p, y + 2 * 104 + 4


def projects():
    p, y = section("03", "PROJECTS", "~/03-projects")
    for i, (name, desc, tags) in enumerate(PROJECTS, 1):
        p += [t(M, y, f"{i:02d} / {name}", 14, "fg", 700, 1),
              t(M, y + 19, desc, 12),
              t(M, y + 35, tags, 10, "dim", 400, 1),
              rule(y + 47)]
        y += 62
    return p, y - 8


def stack():
    p, y = section("04", "STACK", "~/04-stack")
    for k, v in STACK:
        p += [t(M, y, k, 10, "dim", 400, 2), t(M + 130, y, v, 12), rule(y + 14)]
        y += 32
    return p, y - 8


def certs():
    p, y = section("05", "CREDENTIALS", "~/05-certifications")
    for yr, name, org in CERTS:
        p += [t(M, y, yr, 12, "acc", 700), t(M + 70, y, name, 13, "fg", 600), t(M + 70, y + 17, org, 10, "dim", 400, 1)]
        y += 42
    return p, y - 8


def bare(num, label, path):
    return section(num, label, path)


def footer():
    y = 40
    return [rule(10), t(M, y + 8, ">_ " + FOOTER, 13, "dim"),
            f'<rect x="{M + 3 * 7.9 + len(FOOTER) * 7.9 + 8}" y="{y - 4}" width="8" height="15" fill="{{acc}}"/>'], 68


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
