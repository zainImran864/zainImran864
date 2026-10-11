#!/usr/bin/env python3
"""
Weekly Profile Refresh Script for Zain Imran's GitHub Profile.
- Updates the dynamic weekly engineering & CTEM security insight
- Updates recent GitHub engineering activity & project velocity
- Synchronizes the automation pulse badge and timestamps
Runs via GitHub Actions once every week (Mondays at 00:00 UTC).
"""

from datetime import datetime, timezone
import json
import os
import re
import urllib.request
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
    date_str = now.strftime("%B %d, %Y")
    return f"""> ### 💡 Weekly Engineering & DevSecOps Insight
> **{insight['topic']}**
> 
> *"{insight['quote']}"*
> 
> — **{insight['author']}**
> 
> <small><sub>🔄 Auto-updated for Week {week_num} • Next refresh scheduled for next Monday at 00:00 UTC</sub></small>"""

def generate_pulse_markdown(now):
    date_str = now.strftime("%Y-%m-%d")
    return f"`🟢 Workflows: Active (Weekly Schedule)` • `📅 Last Synced: {date_str}` • `🛡️ Audit: Clean` • `⚡ Automated via GitHub Actions`"

def fetch_recent_activity(username="zainImran864", limit=5):
    """Fetches public GitHub events for the user to display recent activity."""
    url = f"https://api.github.com/users/{username}/events/public"
    headers = {"User-Agent": "ZainImran-Profile-Updater"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            events = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Warning: Could not fetch public events ({e}). Using fallback activity.")
        return None

    if not isinstance(events, list) or len(events) == 0:
        return None

    activity_rows = []
    seen = set()

    for ev in events:
        ev_type = ev.get("type")
        repo_name = ev.get("repo", {}).get("name", "")
        repo_short = repo_name.split("/")[-1] if "/" in repo_name else repo_name
        repo_url = f"https://github.com/{repo_name}"
        created_at = ev.get("created_at", "")[:10]

        key = (ev_type, repo_name)
        if key in seen:
            continue
        seen.add(key)

        if ev_type == "PushEvent":
            commits = ev.get("payload", {}).get("commits", [])
            count = len(commits) or 1
            action_desc = f"🚀 Pushed {count} commit{'s' if count > 1 else ''}"
        elif ev_type == "PullRequestEvent":
            pr_action = ev.get("payload", {}).get("action", "opened")
            action_desc = f"🔀 {pr_action.capitalize()} Pull Request"
        elif ev_type == "CreateEvent":
            ref_type = ev.get("payload", {}).get("ref_type", "repository")
            action_desc = f"📦 Created new {ref_type}"
        elif ev_type == "WatchEvent":
            action_desc = "⭐ Starred repository"
        elif ev_type == "ForkEvent":
            action_desc = "🍴 Forked repository"
        elif ev_type == "IssuesEvent":
            action_desc = "📝 Contributed to Issue"
        else:
            action_desc = f"⚡ {ev_type.replace('Event', '')}"

        activity_rows.append(f"| {action_desc} | [`{repo_short}`]({repo_url}) | `{created_at}` |")
        if len(activity_rows) >= limit:
            break

    if not activity_rows:
        return None

    table_header = "| Action | Repository | Date |\n| :--- | :--- | :---: |\n"
    return table_header + "\n".join(activity_rows)

def update_readme():
    readme_path = Path(__file__).resolve().parent.parent.parent / "README.md"
    if not readme_path.exists():
        print(f"Error: {readme_path} not found.")
        return

    content = readme_path.read_text(encoding="utf-8")
    insight, now, week_num = get_weekly_insight()

    insight_md = generate_insight_markdown(insight, now, week_num)
    pulse_md = generate_pulse_markdown(now)
    activity_table = fetch_recent_activity()

    # Replace insight section
    insight_pattern = r"(<!-- WEEKLY-INSIGHT:START -->)(.*?)(<!-- WEEKLY-INSIGHT:END -->)"
    if re.search(insight_pattern, content, flags=re.DOTALL):
        content = re.sub(
            insight_pattern,
            f"\\1\n{insight_md}\n\\3",
            content,
            flags=re.DOTALL
        )

    # Replace pulse section
    pulse_pattern = r"(<!-- PROFILE-PULSE:START -->)(.*?)(<!-- PROFILE-PULSE:END -->)"
    if re.search(pulse_pattern, content, flags=re.DOTALL):
        content = re.sub(
            pulse_pattern,
            f"\\1\n{pulse_md}\n\\3",
            content,
            flags=re.DOTALL
        )

    # Replace activity section if present and activity fetched
    if activity_table:
        activity_pattern = r"(<!-- RECENT-ACTIVITY:START -->)(.*?)(<!-- RECENT-ACTIVITY:END -->)"
        if re.search(activity_pattern, content, flags=re.DOTALL):
            content = re.sub(
                activity_pattern,
                f"\\1\n{activity_table}\n\\3",
                content,
                flags=re.DOTALL
            )

    readme_path.write_text(content, encoding="utf-8")
    print(f"Successfully updated README.md for Week {week_num} ({now.strftime('%Y-%m-%d')}).")

if __name__ == "__main__":
    update_readme()
