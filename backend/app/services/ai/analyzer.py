from typing import Optional
from app.core.config import settings


class AIJSAnalyzer:
    def __init__(self):
        self.client = None
        if settings.OPENAI_API_KEY:
            try:
                from openai import AsyncOpenAI
                self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            except Exception:
                self.client = None

    async def analyze_js_findings(self, js_analysis: dict) -> dict:
        if not self.client:
            return self._fallback_analysis(js_analysis)

        try:
            secrets = js_analysis.get("secrets", [])
            endpoints = js_analysis.get("endpoints", [])
            risky = js_analysis.get("risky_patterns", [])

            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": """You are an expert JavaScript security analyst.
Analyze JS file findings and provide:
1. Risk prioritization (which secrets to fix first)
2. Remediation advice (how to fix each issue)
3. Business impact assessment
4. Recommended security controls
Be specific and actionable."""},
                    {"role": "user", "content": f"""Analyze these JavaScript security findings:

Secrets found ({len(secrets)}):
{secrets}

API Endpoints found ({len(endpoints)}):
{endpoints}

Risky patterns found ({len(risky)}):
{risky}

Provide risk prioritization and remediation advice."""}
                ],
                max_tokens=1000,
                temperature=0.7,
            )
            return {"analysis": response.choices[0].message.content, "source": "ai"}
        except Exception as e:
            return self._fallback_analysis(js_analysis)

    async def prioritize_findings(self, findings: list[dict]) -> dict:
        if not self.client:
            return self._fallback_prioritization(findings)

        try:
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "Prioritize security findings by risk level, exploitability, and business impact. Output as ordered list."},
                    {"role": "user", "content": f"Prioritize these security findings:\n{findings}"}
                ],
                max_tokens=800,
                temperature=0.3,
            )
            return {"prioritization": response.choices[0].message.content, "source": "ai"}
        except Exception:
            return self._fallback_prioritization(findings)

    async def generate_remediation(self, finding: dict) -> dict:
        if not self.client:
            return self._fallback_remediation(finding)

        try:
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "Provide step-by-step remediation for security findings. Include code examples where relevant."},
                    {"role": "user", "content": f"Generate remediation steps for:\nTitle: {finding.get('title')}\nDescription: {finding.get('description')}\nType: {finding.get('type')}"}
                ],
                max_tokens=800,
                temperature=0.5,
            )
            return {"remediation": response.choices[0].message.content, "source": "ai"}
        except Exception:
            return self._fallback_remediation(finding)

    def _fallback_analysis(self, js_analysis: dict) -> dict:
        secrets = js_analysis.get("secrets", [])
        endpoints = js_analysis.get("endpoints", [])
        risky = js_analysis.get("risky_patterns", [])

        return {
            "analysis": f"""## AI JavaScript Security Analysis

### Risk Prioritization

**Critical Priority (Fix Immediately):**
{[s for s in secrets if s.get('severity') == 'critical'][:5] or 'No critical secrets found'}

**High Priority:**
{[s for s in secrets if s.get('severity') == 'high'][:5] or 'No high-severity secrets found'}

### Discovered Endpoints
{endpoints[:10] or 'No endpoints discovered'}

### Risky Patterns Detected
{risky[:10] or 'No risky patterns detected'}

### Remediation Recommendations
1. **Remove exposed credentials** - Never hardcode secrets in client-side code
2. **Use environment variables** for API keys
3. **Implement secret scanning** in CI/CD pipeline
4. **Rotate any exposed keys** immediately
5. **Review risky patterns** and refactor code
6. **Implement CSP** to mitigate XSS risks
7. **Use Subresource Integrity** for external scripts""",
            "source": "fallback",
        }

    def _fallback_prioritization(self, findings: list[dict]) -> dict:
        sorted_findings = sorted(findings, key=lambda f: {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(f.get("severity", "low"), 4))
        return {
            "prioritization": f"""## Prioritized Findings

1. **{sorted_findings[0].get('title', 'N/A')}** ({sorted_findings[0].get('severity', 'N/A')}) - Fix immediately
2. **{sorted_findings[1].get('title', 'N/A')}** ({sorted_findings[1].get('severity', 'N/A')}) - Fix within week
3. **{sorted_findings[2].get('title', 'N/A')}** ({sorted_findings[2].get('severity', 'N/A')}) - Fix within sprint""" if len(sorted_findings) >= 3 else "Not enough findings to prioritize",
            "source": "fallback",
        }

    def _fallback_remediation(self, finding: dict) -> dict:
        return {
            "remediation": f"""## Remediation Steps for: {finding.get('title', '')}

### Step 1: Understand the Issue
- Review the finding details carefully
- Reproduce the vulnerability in a test environment
- Understand the business impact

### Step 2: Implement Fix
- Apply appropriate security controls
- Use framework-provided security features
- Validate the fix with automated testing

### Step 3: Verify
- Retest to confirm the vulnerability is resolved
- Run regression tests
- Monitor for any side effects

### Step 4: Documentation
- Document the fix and lessons learned
- Update security guidelines
- Share knowledge with the team""",
            "source": "fallback",
        }


ai_js_analyzer = AIJSAnalyzer()
