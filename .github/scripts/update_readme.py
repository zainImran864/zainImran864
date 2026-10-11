#!/usr/bin/env python3
"""
Weekly Profile Refresh Script for Zain Imran's GitHub Profile.
Updates the dynamic weekly insight, engineering philosophy, and automated pulse.
Runs via GitHub Actions once every week.
"""

from datetime import datetime, timezone
import re
from pathlib import Path

# Curated rotation of high-impact engineering, architecture, and cybersecurity insights
WEEKLY_INSIGHTS = [
    {
        "topic": "🛡️ Defensive Engineering & CTEM",
        "quote": "Security is not a product, but a process. Continuous exposure management beats point-in-time audits every single time.",
        "author": "Bruce Schneier (Adapted for Modern CTEM)"
    },
    {
        "topic": "⚡ System Architecture & Simplicity",
        "quote": "Simplicity is prerequisite for reliability. Complex systems fail in complex ways.",
        "author": "Edsger W. Dijkstra"
    },
    {
        "topic": "🚀 Clean Code & Craftsmanship",
        "quote": "Any fool can write code that a computer can understand. Good programmers write code that humans can understand.",
        "author": "Martin Fowler"
    },
    {
        "topic": "🔒 Zero Trust & Defense in Depth",
        "quote": "Never trust, always verify. Assume breach and verify every layer from API endpoints to the database.",
        "author": "Zero Trust Principle"
    },
    {
        "topic": "🔄 Automation & DevOps",
        "quote": "If you have to do something more than twice, automate it. If it touches production, test and observe it continuously.",
        "author": "DevOps Manifesto"
    },
    {
        "topic": "🧩 Scalable API Design",
        "quote": "Good APIs are easy to use and hard to misuse. Design interfaces from the consumer's perspective first.",
        "author": "Joshua Bloch"
    },
    {
        "topic": "💡 Continuous Learning",
        "quote": "The only way to go fast is to go well. Quality software is delivered through iterative craftsmanship.",
        "author": "Robert C. Martin"
    },
    {
        "topic": "🌐 Full-Stack Synergy",
        "quote": "Great user experiences rely on robust backends. The best full-stack engineers design seamless data flows end-to-end.",
        "author": "Software Engineering Axiom"
    }
]

def get_weekly_insight():
    # Deterministic rotation based on ISO week number
    now = datetime.now(timezone.utc)
    week_num = now.isocalendar()[1]
    insight = WEEKLY_INSIGHTS[week_num % len(WEEKLY_INSIGHTS)]
    return insight, now, week_num

def generate_insight_markdown(insight, now, week_num):
    date_str = now.strftime("%B %d, %Y")
    return f"""> ### 💡 Weekly Engineering Insight
> **{insight['topic']}**
> 
> *"{insight['quote']}"*
> 
> — **{insight['author']}**
> 
> <small><sub>🔄 Auto-updated for Week {week_num} • Next refresh next Monday at 00:00 UTC</sub></small>"""

def generate_pulse_markdown(now):
    date_str = now.strftime("%Y-%m-%d")
    return f"`🟢 Workflows: Active (Weekly Schedule)` • `📅 Last Synced: {date_str}` • `⚡ Automated via GitHub Actions`"

def update_readme():
    readme_path = Path(__file__).resolve().parent.parent.parent / "README.md"
    if not readme_path.exists():
        print(f"Error: {readme_path} not found.")
        return

    content = readme_path.read_text(encoding="utf-8")
    insight, now, week_num = get_weekly_insight()

    insight_md = generate_insight_markdown(insight, now, week_num)
    pulse_md = generate_pulse_markdown(now)

    # Replace insight section
    insight_pattern = r"(<!-- WEEKLY-INSIGHT:START -->)(.*?)(<!-- WEEKLY-INSIGHT:END -->)"
    if re.search(insight_pattern, content, flags=re.DOTALL):
        content = re.sub(
            insight_pattern,
            f"\\1\n{insight_md}\n\\3",
            content,
            flags=re.DOTALL
        )
    else:
        print("Marker <!-- WEEKLY-INSIGHT:START --> not found, skipping insight replacement.")

    # Replace pulse section
    pulse_pattern = r"(<!-- PROFILE-PULSE:START -->)(.*?)(<!-- PROFILE-PULSE:END -->)"
    if re.search(pulse_pattern, content, flags=re.DOTALL):
        content = re.sub(
            pulse_pattern,
            f"\\1\n{pulse_md}\n\\3",
            content,
            flags=re.DOTALL
        )
    else:
        print("Marker <!-- PROFILE-PULSE:START --> not found, skipping pulse replacement.")

    readme_path.write_text(content, encoding="utf-8")
    print(f"Successfully updated README.md for Week {week_num} ({now.strftime('%Y-%m-%d')}).")

if __name__ == "__main__":
    update_readme()
