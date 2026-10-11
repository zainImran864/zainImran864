#!/usr/bin/env python3
"""
Weekly Profile Refresh Script for Zain Imran's GitHub Profile.
- Updates the dynamic weekly engineering & DevSecOps insight without duplicating titles.
Runs via GitHub Actions once every week (Mondays at 00:00 UTC).
"""

from datetime import datetime, timezone
import re
from pathlib import Path

# Curated rotation of high-impact engineering, architecture, and cybersecurity insights
WEEKLY_INSIGHTS = [
    {
        "topic": "🛡️ Continuous Threat Exposure Management (CTEM)",
        "quote": "Security is not a static checkbox; it is a continuous posture. Continuous exposure management and automated surface discovery beat point-in-time compliance audits every single time.",
        "author": "Cybersecurity & CTEM Engineering Axiom"
    },
    {
        "topic": "⚡ System Architecture & Simplicity",
        "quote": "Simplicity is prerequisite for reliability. Complex systems fail in complex and unexpected ways. Keep the critical path transparent.",
        "author": "Edsger W. Dijkstra"
    },
    {
        "topic": "🚀 Clean Code & Craftsmanship",
        "quote": "Any fool can write code that a computer can understand. Good software engineers write code that humans can understand and maintain.",
        "author": "Martin Fowler"
    },
    {
        "topic": "🔒 Zero Trust & Defense in Depth",
        "quote": "Never trust, always verify. Assume breach and enforce least privilege from the edge reverse-proxy down to database tables.",
        "author": "Zero Trust Security Model"
    },
    {
        "topic": "🔄 Automation & DevOps Velocity",
        "quote": "If you perform a task manually more than twice, automate it. If it touches production, observe, measure, and audit it continuously.",
        "author": "Modern DevSecOps Philosophy"
    },
    {
        "topic": "🧩 Resilient API Architecture",
        "quote": "Good APIs are intuitive to use and practically impossible to misuse. Design interfaces from consumer ergonomics backward to the database.",
        "author": "Joshua Bloch"
    },
    {
        "topic": "💡 Engineering Iteration",
        "quote": "The only way to move fast with high confidence is to build well. High velocity is a byproduct of high internal code quality.",
        "author": "Robert C. Martin"
    },
    {
        "topic": "🌐 Full-Stack Synergy",
        "quote": "Delightful frontend experiences are enabled by predictable, type-safe, and low-latency backends. Great engineers bridge both worlds.",
        "author": "Full-Stack Design Principle"
    }
]

def get_weekly_insight():
    now = datetime.now(timezone.utc)
    week_num = now.isocalendar()[1]
    insight = WEEKLY_INSIGHTS[week_num % len(WEEKLY_INSIGHTS)]
    return insight, now, week_num

def generate_insight_markdown(insight, now, week_num):
    return f"""> **{insight['topic']}**
> 
> *"{insight['quote']}"*
> 
> — **{insight['author']}**"""

def update_readme():
    readme_path = Path(__file__).resolve().parent.parent.parent / "README.md"
    if not readme_path.exists():
        print(f"Error: {readme_path} not found.")
        return

    content = readme_path.read_text(encoding="utf-8")
    insight, now, week_num = get_weekly_insight()

    insight_md = generate_insight_markdown(insight, now, week_num)

    # Replace insight section
    insight_pattern = r"(<!-- WEEKLY-INSIGHT:START -->)(.*?)(<!-- WEEKLY-INSIGHT:END -->)"
    if re.search(insight_pattern, content, flags=re.DOTALL):
        content = re.sub(
            insight_pattern,
            f"\\1\n{insight_md}\n\\3",
            content,
            flags=re.DOTALL
        )

    readme_path.write_text(content, encoding="utf-8")
    print("Successfully updated README.md.")

if __name__ == "__main__":
    update_readme()
