from typing import Optional
from app.core.config import settings


class AICoach:
    def __init__(self):
        self.client = None
        if settings.OPENAI_API_KEY:
            try:
                from openai import AsyncOpenAI
                self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            except Exception:
                self.client = None

    async def teach_concept(self, topic: str, skill_level: str = "beginner") -> dict:
        if not self.client:
            return self._fallback_lesson(topic, skill_level)

        try:
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": f"You are a friendly cybersecurity teacher. Explain topics at {skill_level} level. Use analogies and real-world examples."},
                    {"role": "user", "content": f"Teach me about {topic} in cybersecurity. I'm a {skill_level}."}
                ],
                max_tokens=1000,
                temperature=0.7,
            )
            return {"lesson": response.choices[0].message.content, "source": "ai"}
        except Exception:
            return self._fallback_lesson(topic, skill_level)

    async def give_hint(self, mission: dict, hint_level: int = 1) -> str:
        if not self.client:
            return self._fallback_hint(mission, hint_level)

        try:
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a cybersecurity coach. Give progressive hints for recon missions. Start vague, get specific."},
                    {"role": "user", "content": f"Mission: {mission.get('title', '')}\nDescription: {mission.get('description', '')}\nObjectives: {mission.get('objectives', [])}\nHint level (1-5): {hint_level}\nGive me a hint to solve this recon mission."}
                ],
                max_tokens=300,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception:
            return self._fallback_hint(mission, hint_level)

    async def evaluate_progress(self, user_stats: dict) -> dict:
        if not self.client:
            return self._fallback_evaluation(user_stats)

        try:
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a cybersecurity coach evaluating a student's progress. Be encouraging and constructive."},
                    {"role": "user", "content": f"Evaluate my progress: {user_stats}"}
                ],
                max_tokens=500,
                temperature=0.7,
            )
            return {"evaluation": response.choices[0].message.content, "source": "ai"}
        except Exception:
            return self._fallback_evaluation(user_stats)

    def _fallback_lesson(self, topic: str, skill_level: str) -> dict:
        lessons = {
            "subdomain enumeration": {
                "beginner": "Subdomain enumeration is like finding all the doors and windows of a building. Just like a house has a front door, back door, and maybe a garage, websites have subdomains like 'mail.example.com' or 'admin.example.com'. We find them using tools and public records like certificate logs.",
                "intermediate": "Subdomain enumeration involves both passive techniques (Certificate Transparency logs, DNS records, search engines) and active techniques (brute-forcing common names, DNS zone transfers). Tools like Subfinder, Amass, and our built-in scanner can help.",
                "advanced": "Advanced subdomain enumeration uses permutation scanning, recursive DNS resolution, and correlation across multiple data sources (Shodan, SecurityTrails, VirusTotal). You can also use NLP-based discovery from JavaScript files and HTML comments.",
            },
        }

        lesson = lessons.get(topic.lower(), {}).get(skill_level, f"Let me teach you about {topic} at the {skill_level} level. This is a great topic in cybersecurity!")
        return {"lesson": lesson, "source": "fallback"}

    def _fallback_hint(self, mission: dict, hint_level: int) -> str:
        hints = [
            "Start with basic reconnaissance - check the target's DNS records.",
            "Look at certificate transparency logs for subdomains.",
            "Try common subdomain names related to the target's technology.",
            "Check if there are any interesting endpoints or services exposed.",
            "Look for the specific vulnerability pattern mentioned in the mission objectives.",
        ]
        idx = min(hint_level - 1, len(hints) - 1)
        return hints[idx]

    def _fallback_evaluation(self, user_stats: dict) -> dict:
        scans = user_stats.get("scan_count", 0)
        findings = user_stats.get("total_findings", 0)
        xp = user_stats.get("xp", 0)
        level = user_stats.get("level", 1)

        return {
            "evaluation": f"""## Cybersecurity Progress Report

### Stats
- Level: {level}
- XP: {xp}
- Scans Completed: {scans}
- Findings Discovered: {findings}

### Feedback
You're making great progress! Keep exploring and learning. Try completing more recon missions in the Cyber Range to practice your skills.

### Next Steps
1. Complete more scanning missions
2. Practice with different target types
3. Learn about API security testing
4. Try the advanced JavaScript analysis challenges""",
            "source": "fallback",
        }


ai_coach = AICoach()
