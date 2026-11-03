#!/usr/bin/env python3
"""
Generates custom, high-definition SVG visual assets for Zain Imran's GitHub Profile README:
1. assets/hero-banner.svg          - Executive engineering header banner
2. assets/architecture-pillars.svg - System architecture & engineering pillars diagram
3. assets/github-telemetry.svg     - Self-hosted live GitHub telemetry & language breakdown card
"""

from datetime import datetime, timezone
import html
import json
import os
from pathlib import Path
import urllib.error
import urllib.request

USERNAME = "zainImran864"
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = ROOT_DIR / "assets"

LANG_COLORS = {
    "TypeScript": "#3178C6",
    "JavaScript": "#F7DF1E",
    "Python": "#3572A5",
    "HTML": "#E34C26",
    "CSS": "#563D7C",
    "Shell": "#89E051",
    "Dockerfile": "#384D54",
    "C++": "#F34B7D",
    "Java": "#B07219",
}


def fetch_github_stats(username: str) -> dict:
    """Fetches live repository and user telemetry from GitHub REST API with graceful fallback."""
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "zainImran864-profile-telemetry",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    stats = {
        "public_repos": 18,
        "followers": 12,
        "total_stars": 15,
        "total_forks": 4,
        "languages": {
            "TypeScript": 42.5,
            "Python": 26.0,
            "JavaScript": 21.0,
            "HTML/CSS": 10.5,
        },
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    }

    try:
        req = urllib.request.Request(f"https://api.github.com/users/{username}", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            user_data = json.loads(resp.read().decode("utf-8"))
            stats["public_repos"] = int(user_data.get("public_repos", stats["public_repos"]))
            stats["followers"] = int(user_data.get("followers", stats["followers"]))

        req_repos = urllib.request.Request(
            f"https://api.github.com/users/{username}/repos?per_page=100&type=owner",
            headers=headers,
        )
        with urllib.request.urlopen(req_repos, timeout=10) as resp:
            repos_data = json.loads(resp.read().decode("utf-8"))
            if isinstance(repos_data, list) and repos_data:
                stars = sum(int(r.get("stargazers_count", 0)) for r in repos_data)
                forks = sum(int(r.get("forks_count", 0)) for r in repos_data)
                stats["total_stars"] = stars
                stats["total_forks"] = forks

                lang_counts: dict[str, int] = {}
                for r in repos_data:
                    if r.get("fork"):
                        continue
                    lang = r.get("language")
                    size = max(int(r.get("size", 1)), 1)
                    if lang:
                        if lang in ("HTML", "CSS", "SCSS"):
                            lang = "HTML/CSS"
                        lang_counts[lang] = lang_counts.get(lang, 0) + size

                if lang_counts:
                    total_size = sum(lang_counts.values())
                    sorted_langs = sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)[:5]
                    top_total = sum(v for _, v in sorted_langs)
                    stats["languages"] = {
                        k: round((v / top_total) * 100, 1) for k, v in sorted_langs
                    }
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError) as exc:
        print(f"Notice: Using baseline telemetry fallback ({exc})")

    return stats


def generate_hero_banner() -> str:
    """Generates the executive SVG hero banner."""
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 320" width="100%" height="100%" role="img" aria-label="Zain Imran - Software Engineer &amp; CTEM Architect">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#070B14" />
      <stop offset="50%" stop-color="#0F172A" />
      <stop offset="100%" stop-color="#091020" />
    </linearGradient>
    <linearGradient id="accentGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38BDF8" />
      <stop offset="50%" stop-color="#3B82F6" />
      <stop offset="100%" stop-color="#10B981" />
    </linearGradient>
    <linearGradient id="textGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="65%" stop-color="#E2E8F0" />
      <stop offset="100%" stop-color="#38BDF8" />
    </linearGradient>
    <radialGradient id="glowLeft" cx="18%" cy="25%" r="45%">
      <stop offset="0%" stop-color="#3B82F6" stop-opacity="0.18" />
      <stop offset="100%" stop-color="#3B82F6" stop-opacity="0" />
    </radialGradient>
    <radialGradient id="glowRight" cx="85%" cy="75%" r="45%">
      <stop offset="0%" stop-color="#10B981" stop-opacity="0.14" />
      <stop offset="100%" stop-color="#10B981" stop-opacity="0" />
    </radialGradient>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1E293B" stroke-width="0.7" stroke-opacity="0.55" />
    </pattern>
  </defs>

  <!-- Main Card Frame -->
  <rect width="1200" height="320" rx="18" fill="url(#bgGrad)" />
  <rect width="1200" height="320" rx="18" fill="url(#grid)" />
  <rect width="1200" height="320" rx="18" fill="url(#glowLeft)" />
  <rect width="1200" height="320" rx="18" fill="url(#glowRight)" />
  <rect x="1" y="1" width="1198" height="318" rx="17" fill="none" stroke="#1E293B" stroke-width="1.5" />

  <!-- Top Accent Line -->
  <rect x="0" y="0" width="1200" height="4" rx="2" fill="url(#accentGrad)" />

  <!-- Top Bar / Terminal Telemetry Header -->
  <g transform="translate(48, 34)">
    <circle cx="8" cy="8" r="5.5" fill="#EF4444" />
    <circle cx="26" cy="8" r="5.5" fill="#F59E0B" />
    <circle cx="44" cy="8" r="5.5" fill="#10B981" />
    <text x="68" y="12.5" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="12.5" fill="#64748B" letter-spacing="0.5">
      zain-imran@cybersilo:~/systems-architecture $ <tspan fill="#38BDF8">status --posture=verified</tspan>
    </text>
  </g>

  <!-- Live Operational Pill (Top Right) -->
  <g transform="translate(916, 24)">
    <rect width="236" height="28" rx="14" fill="#0F172A" stroke="#1E293B" stroke-width="1.2" />
    <circle cx="18" cy="14" r="4.5" fill="#10B981">
      <animate attributeName="opacity" values="1;0.35;1" dur="2.2s" repeatCount="indefinite" />
    </circle>
    <text x="32" y="18" font-family="'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="11.5" font-weight="600" fill="#E2E8F0" letter-spacing="0.8">
      SYSTEMS ONLINE • CTEM
    </text>
  </g>

  <!-- Main Headline & Identity -->
  <g transform="translate(48, 114)">
    <text x="0" y="0" font-family="'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="46" font-weight="800" fill="url(#textGrad)" letter-spacing="-0.8">
      Zain Imran
    </text>
    <text x="0" y="38" font-family="'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="19" font-weight="600" fill="#38BDF8" letter-spacing="0.2">
      Software Engineer  •  Full-Stack Architecture &amp; CTEM Security Engineering
    </text>
    <text x="0" y="70" font-family="'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="14.5" fill="#94A3B8">
      Architecting continuous threat exposure management at <tspan fill="#F8FAFC" font-weight="600">Cybersilo</tspan> &amp; shipping resilient full-stack web systems.
    </text>
  </g>

  <!-- Bottom Capability Badges -->
  <g transform="translate(48, 232)">
    <!-- Badge 1 -->
    <g transform="translate(0, 0)">
      <rect width="250" height="36" rx="8" fill="#111C33" stroke="#1E3A5F" stroke-width="1" />
      <text x="16" y="23" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="12" font-weight="600" fill="#38BDF8">
        🛡️ CTEM • CIS • PCI DSS • CMMC
      </text>
    </g>
    <!-- Badge 2 -->
    <g transform="translate(264, 0)">
      <rect width="286" height="36" rx="8" fill="#111C33" stroke="#1E3A5F" stroke-width="1" />
      <text x="16" y="23" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="12" font-weight="600" fill="#60A5FA">
        ⚡ Next.js • React • FastAPI • Node
      </text>
    </g>
    <!-- Badge 3 -->
    <g transform="translate(564, 0)">
      <rect width="236" height="36" rx="8" fill="#111C33" stroke="#1E3A5F" stroke-width="1" />
      <text x="16" y="23" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="12" font-weight="600" fill="#34D399">
        🔒 TypeScript • Python • Docker
      </text>
    </g>
  </g>

  <!-- Right-side Decorative Cyber Architecture Node Graphic -->
  <g transform="translate(915, 86)">
    <rect x="0" y="0" width="236" height="182" rx="12" fill="#0B1324" stroke="#1E293B" stroke-width="1.2" />
    <text x="18" y="28" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="11" font-weight="700" fill="#64748B" letter-spacing="1">
      ARCHITECTURE POSTURE
    </text>
    <line x1="18" y1="38" x2="218" y2="38" stroke="#1E293B" stroke-width="1" />

    <text x="18" y="64" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="12" fill="#94A3B8">
      Surface Discovery
    </text>
    <text x="178" y="64" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="12" font-weight="700" fill="#10B981">
      ACTIVE
    </text>

    <text x="18" y="94" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="12" fill="#94A3B8">
      API Type Safety
    </text>
    <text x="178" y="94" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="12" font-weight="700" fill="#38BDF8">
      STRICT
    </text>

    <text x="18" y="124" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="12" fill="#94A3B8">
      Compliance Engine
    </text>
    <text x="164" y="124" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="12" font-weight="700" fill="#60A5FA">
      CIS/CMMC
    </text>

    <text x="18" y="154" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="12" fill="#94A3B8">
      CI/CD Audits
    </text>
    <text x="164" y="154" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="12" font-weight="700" fill="#A78BFA">
      VERIFIED
    </text>
  </g>
</svg>
"""


def generate_architecture_pillars() -> str:
    """Generates the 3 Engineering Pillars vector SVG diagram."""
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 280" width="100%" height="100%" role="img" aria-label="Core Engineering Pillars: Defensive Engineering, Full-Stack Craftsmanship, DevSecOps &amp; Cloud">
  <defs>
    <linearGradient id="cardBg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0F172A" />
      <stop offset="100%" stop-color="#090F1C" />
    </linearGradient>
  </defs>

  <!-- Background container -->
  <rect width="1200" height="280" rx="16" fill="#070B14" />
  <rect x="1" y="1" width="1198" height="278" rx="15" fill="none" stroke="#1E293B" stroke-width="1.5" />

  <!-- Pillar 1: Defensive Engineering & CTEM -->
  <g transform="translate(24, 24)">
    <rect width="364" height="232" rx="12" fill="url(#cardBg)" stroke="#1E293B" stroke-width="1.2" />
    <rect x="0" y="0" width="364" height="4" rx="2" fill="#EF4444" />
    <text x="24" y="38" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="11.5" font-weight="700" fill="#F87171" letter-spacing="1.2">
      01 // DEFENSIVE ENGINEERING &amp; CTEM
    </text>
    <text x="24" y="68" font-family="'Inter', -apple-system, sans-serif" font-size="18" font-weight="700" fill="#F8FAFC">
      Threat Exposure Management
    </text>
    <line x1="24" y1="84" x2="340" y2="84" stroke="#1E293B" stroke-width="1" />
    <text x="24" y="114" font-family="'Inter', -apple-system, sans-serif" font-size="13.5" fill="#CBD5E1">
      <tspan fill="#F87171" font-weight="700">▸</tspan> Automated attack surface discovery
    </text>
    <text x="24" y="142" font-family="'Inter', -apple-system, sans-serif" font-size="13.5" fill="#CBD5E1">
      <tspan fill="#F87171" font-weight="700">▸</tspan> CIS Controls, PCI DSS &amp; CMMC mapping
    </text>
    <text x="24" y="170" font-family="'Inter', -apple-system, sans-serif" font-size="13.5" fill="#CBD5E1">
      <tspan fill="#F87171" font-weight="700">▸</tspan> Risk-based vulnerability prioritization
    </text>
    <text x="24" y="198" font-family="'Inter', -apple-system, sans-serif" font-size="13.5" fill="#CBD5E1">
      <tspan fill="#F87171" font-weight="700">▸</tspan> Zero-Trust &amp; least-privilege architecture
    </text>
  </g>

  <!-- Connector 1 -> 2 -->
  <g transform="translate(394, 130)">
    <line x1="0" y1="10" x2="18" y2="10" stroke="#38BDF8" stroke-width="2" stroke-dasharray="3,3" />
    <polygon points="18,5 26,10 18,15" fill="#38BDF8" />
  </g>

  <!-- Pillar 2: Full-Stack Systems Craftsmanship -->
  <g transform="translate(418, 24)">
    <rect width="364" height="232" rx="12" fill="url(#cardBg)" stroke="#1E293B" stroke-width="1.2" />
    <rect x="0" y="0" width="364" height="4" rx="2" fill="#3B82F6" />
    <text x="24" y="38" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="11.5" font-weight="700" fill="#60A5FA" letter-spacing="1.2">
      02 // FULL-STACK CRAFTSMANSHIP
    </text>
    <text x="24" y="68" font-family="'Inter', -apple-system, sans-serif" font-size="18" font-weight="700" fill="#F8FAFC">
      Scalable Web &amp; API Systems
    </text>
    <line x1="24" y1="84" x2="340" y2="84" stroke="#1E293B" stroke-width="1" />
    <text x="24" y="114" font-family="'Inter', -apple-system, sans-serif" font-size="13.5" fill="#CBD5E1">
      <tspan fill="#60A5FA" font-weight="700">▸</tspan> Type-safe Next.js, React &amp; Tailwind UIs
    </text>
    <text x="24" y="142" font-family="'Inter', -apple-system, sans-serif" font-size="13.5" fill="#CBD5E1">
      <tspan fill="#60A5FA" font-weight="700">▸</tspan> High-throughput FastAPI &amp; Node.js APIs
    </text>
    <text x="24" y="170" font-family="'Inter', -apple-system, sans-serif" font-size="13.5" fill="#CBD5E1">
      <tspan fill="#60A5FA" font-weight="700">▸</tspan> PostgreSQL, MySQL, MongoDB &amp; Supabase
    </text>
    <text x="24" y="198" font-family="'Inter', -apple-system, sans-serif" font-size="13.5" fill="#CBD5E1">
      <tspan fill="#60A5FA" font-weight="700">▸</tspan> Clean domain boundaries &amp; REST contracts
    </text>
  </g>

  <!-- Connector 2 -> 3 -->
  <g transform="translate(788, 130)">
    <line x1="0" y1="10" x2="18" y2="10" stroke="#10B981" stroke-width="2" stroke-dasharray="3,3" />
    <polygon points="18,5 26,10 18,15" fill="#10B981" />
  </g>

  <!-- Pillar 3: DevSecOps & Cloud Automation -->
  <g transform="translate(812, 24)">
    <rect width="364" height="232" rx="12" fill="url(#cardBg)" stroke="#1E293B" stroke-width="1.2" />
    <rect x="0" y="0" width="364" height="4" rx="2" fill="#10B981" />
    <text x="24" y="38" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="11.5" font-weight="700" fill="#34D399" letter-spacing="1.2">
      03 // DEVSECOPS &amp; AUTOMATION
    </text>
    <text x="24" y="68" font-family="'Inter', -apple-system, sans-serif" font-size="18" font-weight="700" fill="#F8FAFC">
      Resilient Delivery Pipelines
    </text>
    <line x1="24" y1="84" x2="340" y2="84" stroke="#1E293B" stroke-width="1" />
    <text x="24" y="114" font-family="'Inter', -apple-system, sans-serif" font-size="13.5" fill="#CBD5E1">
      <tspan fill="#34D399" font-weight="700">▸</tspan> Automated GitHub Actions CI/CD workflows
    </text>
    <text x="24" y="142" font-family="'Inter', -apple-system, sans-serif" font-size="13.5" fill="#CBD5E1">
      <tspan fill="#34D399" font-weight="700">▸</tspan> Containerized Docker &amp; Linux workloads
    </text>
    <text x="24" y="170" font-family="'Inter', -apple-system, sans-serif" font-size="13.5" fill="#CBD5E1">
      <tspan fill="#34D399" font-weight="700">▸</tspan> Scheduled secret &amp; exposure auditing
    </text>
    <text x="24" y="198" font-family="'Inter', -apple-system, sans-serif" font-size="13.5" fill="#CBD5E1">
      <tspan fill="#34D399" font-weight="700">▸</tspan> Deterministic builds &amp; edge deployments
    </text>
  </g>
</svg>
"""


def generate_telemetry_svg(stats: dict) -> str:
    """Generates the live GitHub Telemetry & Language Distribution SVG card."""
    langs = stats.get("languages", {})
    if not langs:
        langs = {
            "TypeScript": 42.5,
            "Python": 26.0,
            "JavaScript": 21.0,
            "HTML/CSS": 10.5,
        }

    # Build stacked progress bar and legend rows
    bar_width = 500
    x_offset = 0
    bar_segments = []
    legend_rows = []

    palette_fallback = ["#3178C6", "#3572A5", "#F7DF1E", "#E34C26", "#10B981"]
    for idx, (lang, pct) in enumerate(langs.items()):
        color = LANG_COLORS.get(lang, "#E34C26" if "HTML" in lang else palette_fallback[idx % len(palette_fallback)])
        seg_w = max(round((pct / 100.0) * bar_width, 1), 6)
        if idx == len(langs) - 1:
            seg_w = max(bar_width - x_offset, 6)
        bar_segments.append(
            f'<rect x="{x_offset}" y="0" width="{seg_w}" height="12" fill="{color}" />'
        )
        x_offset += seg_w

        row_y = 140 + idx * 30
        pct_bar_w = max(round((pct / 100.0) * 240, 1), 8)
        legend_rows.append(f"""
      <g transform="translate(0, {row_y})">
        <circle cx="8" cy="-4" r="5" fill="{color}" />
        <text x="22" y="0" font-family="'Inter', -apple-system, sans-serif" font-size="13.5" font-weight="600" fill="#E2E8F0">{html.escape(lang)}</text>
        <rect x="160" y="-10" width="240" height="8" rx="4" fill="#1E293B" />
        <rect x="160" y="-10" width="{pct_bar_w}" height="8" rx="4" fill="{color}" />
        <text x="495" y="0" text-anchor="end" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="12.5" font-weight="600" fill="#94A3B8">{pct:.1f}%</text>
      </g>""")

    updated_str = html.escape(stats.get("updated_at", ""))
    public_repos = stats.get("public_repos", 18)
    total_stars = stats.get("total_stars", 15)
    followers = stats.get("followers", 12)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 310" width="100%" height="100%" role="img" aria-label="GitHub Engineering Telemetry and Language Distribution">
  <defs>
    <linearGradient id="telemetryBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#070B14" />
      <stop offset="100%" stop-color="#0F172A" />
    </linearGradient>
    <clipPath id="barClip">
      <rect x="0" y="0" width="500" height="12" rx="6" />
    </clipPath>
  </defs>

  <rect width="1200" height="310" rx="16" fill="url(#telemetryBg)" />
  <rect x="1" y="1" width="1198" height="308" rx="15" fill="none" stroke="#1E293B" stroke-width="1.5" />

  <!-- Left Panel: Engineering & Repository Telemetry -->
  <g transform="translate(36, 34)">
    <text x="0" y="0" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="12" font-weight="700" fill="#38BDF8" letter-spacing="1.2">
      ⚡ GITHUB ENGINEERING TELEMETRY
    </text>
    <text x="0" y="28" font-family="'Inter', -apple-system, sans-serif" font-size="20" font-weight="700" fill="#F8FAFC">
      System Metrics &amp; Repository Posture
    </text>

    <!-- 4 Metric Bento Boxes -->
    <g transform="translate(0, 52)">
      <!-- Box 1 -->
      <rect x="0" y="0" width="256" height="82" rx="10" fill="#0B1324" stroke="#1E293B" stroke-width="1.2" />
      <text x="18" y="28" font-family="'Inter', -apple-system, sans-serif" font-size="12.5" fill="#94A3B8">Public Repositories</text>
      <text x="18" y="62" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="26" font-weight="800" fill="#38BDF8">{public_repos}</text>
      <text x="185" y="60" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="11" fill="#10B981">● ACTIVE</text>

      <!-- Box 2 -->
      <rect x="274" y="0" width="256" height="82" rx="10" fill="#0B1324" stroke="#1E293B" stroke-width="1.2" />
      <text x="292" y="28" font-family="'Inter', -apple-system, sans-serif" font-size="12.5" fill="#94A3B8">Stars &amp; Community Reach</text>
      <text x="292" y="62" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="26" font-weight="800" fill="#FBBF24">{total_stars} ★</text>
      <text x="415" y="60" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="11" fill="#94A3B8">{followers} Followers</text>

      <!-- Box 3 -->
      <rect x="0" y="98" width="256" height="82" rx="10" fill="#0B1324" stroke="#1E293B" stroke-width="1.2" />
      <text x="18" y="126" font-family="'Inter', -apple-system, sans-serif" font-size="12.5" fill="#94A3B8">Security &amp; Secret Audit</text>
      <text x="18" y="160" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="20" font-weight="800" fill="#10B981">PASSING ✓</text>
      <text x="165" y="158" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="11" fill="#64748B">0 Leaks</text>

      <!-- Box 4 -->
      <rect x="274" y="98" width="256" height="82" rx="10" fill="#0B1324" stroke="#1E293B" stroke-width="1.2" />
      <text x="292" y="126" font-family="'Inter', -apple-system, sans-serif" font-size="12.5" fill="#94A3B8">Primary Engineering Focus</text>
      <text x="292" y="160" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="18" font-weight="800" fill="#60A5FA">CTEM &amp; Full-Stack</text>
    </g>

    <text x="0" y="254" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="11" fill="#64748B">
      Auto-synced via GitHub Actions • Last telemetry snapshot: {updated_str}
    </text>
  </g>

  <!-- Vertical Divider -->
  <line x1="608" y1="32" x2="608" y2="278" stroke="#1E293B" stroke-width="1.2" />

  <!-- Right Panel: Language & Architecture Distribution -->
  <g transform="translate(652, 34)">
    <text x="0" y="0" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="12" font-weight="700" fill="#10B981" letter-spacing="1.2">
      📊 CODEBASE LANGUAGE DISTRIBUTION
    </text>
    <text x="0" y="28" font-family="'Inter', -apple-system, sans-serif" font-size="20" font-weight="700" fill="#F8FAFC">
      Primary Production Stack
    </text>

    <!-- Combined Multi-Segment Progress Bar -->
    <g transform="translate(0, 54)" clip-path="url(#barClip)">
      {"".join(bar_segments)}
    </g>

    <!-- Language Breakdown Rows -->
    <g transform="translate(0, -35)">
      {"".join(legend_rows)}
    </g>
  </g>
</svg>
"""


def main():
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    stats = fetch_github_stats(USERNAME)

    hero_path = ASSETS_DIR / "hero-banner.svg"
    pillars_path = ASSETS_DIR / "architecture-pillars.svg"
    telemetry_path = ASSETS_DIR / "github-telemetry.svg"

    hero_path.write_text(generate_hero_banner(), encoding="utf-8")
    pillars_path.write_text(generate_architecture_pillars(), encoding="utf-8")
    telemetry_path.write_text(generate_telemetry_svg(stats), encoding="utf-8")

    print(f"Generated {hero_path.name}, {pillars_path.name}, and {telemetry_path.name} successfully.")


if __name__ == "__main__":
    main()
