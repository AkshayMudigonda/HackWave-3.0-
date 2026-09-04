"""
Parses browser operation commands into structured requests.
"""
import re
from urllib.parse import quote_plus


class BrowserParser:

    def parse(self, command: str) -> dict:

        text = command.strip()
        lower = text.lower()

        youtube_match = re.search(r"(?:open\s+)?youtube\s*,?\s*(?:and\s*)?search(?:\s+for)?\s+(.+?)(?=\s*,?\s*(?:then\s+)?(?:open|wait|save|create)\b|\.?$)", text, re.I)
        if youtube_match:
            query = self._clean_query(youtube_match.group(1))
            parsed = self._search("youtube", query, "first" in lower)
            parsed["requires_page_automation"] = any(word in lower for word in ("first", "title", "save", "create", "wait"))
            return parsed

        google_match = re.search(r"(?:open\s+)?google\s*,?\s*(?:and\s*)?search(?:\s+for)?\s+(.+?)(?=\s*,?\s*(?:then\s+)?(?:open|and|save|create)\b|\.?$)", text, re.I)
        if google_match:
            parsed = self._search("google", self._clean_query(google_match.group(1)), "first" in lower)
            parsed["requires_page_automation"] = any(word in lower for word in ("first", "official", "title", "save", "create", "summary"))
            return parsed

        if lower.startswith("open "):
            target = text[5:].strip()

            urls = {
                "google": "https://www.google.com",
                "youtube": "https://www.youtube.com",
                "github": "https://github.com",
                "wikipedia": "https://en.wikipedia.org",
                "maps": "https://www.google.com/maps",
                "stackoverflow": "https://stackoverflow.com",
            }

            if target.lower() in urls:
                return {
                    "action": "open",
                    "target": target,
                    "url": urls[target.lower()],
                }

            if target.startswith(
                ("http://", "https://")
            ):
                return {
                    "action": "open",
                    "target": target,
                    "url": target,
                }

            if "." in target and " " not in target:
                return {
                    "action": "open",
                    "target": target,
                    "url": f"https://{target}",
                }

        if lower.startswith("search ") or lower.startswith("search for "):
            query = text[11:].strip() if lower.startswith("search for ") else text[7:].strip()
            return self._search("google", self._clean_query(query))

        if lower.startswith("youtube "):
            query = text[8:].strip()

            return self._search("youtube", self._clean_query(query))

        if lower.startswith("github "):
            query = text[7:].strip()

            return {
                "action": "search",
                "engine": "github",
                "query": query,
                "url": (
                    "https://github.com/search?q="
                    + quote_plus(query)
                ),
            }

        if lower.startswith("wikipedia "):
            query = text[10:].strip()

            return {
                "action": "search",
                "engine": "wikipedia",
                "query": query,
                "url": (
                    "https://en.wikipedia.org/wiki/"
                    + quote_plus(query.replace(" ", "_"))
                ),
            }

        if lower.startswith("maps "):
            query = text[5:].strip()

            return {
                "action": "search",
                "engine": "maps",
                "query": query,
                "url": (
                    "https://www.google.com/maps/search/"
                    + quote_plus(query)
                ),
            }

        if lower.startswith("stackoverflow "):
            query = text[14:].strip()

            return {
                "action": "search",
                "engine": "stackoverflow",
                "query": query,
                "url": (
                    "https://stackoverflow.com/search?q="
                    + quote_plus(query)
                ),
            }

        return {
            "action": "unknown",
            "target": text,
        }

    def _search(self, engine: str, query: str, requested_first_result: bool = False) -> dict:
        prefix = "https://www.youtube.com/results?search_query=" if engine == "youtube" else "https://www.google.com/search?q="
        return {"action": "search", "engine": engine, "query": query,
                "url": prefix + quote_plus(query), "requested_first_result": requested_first_result}

    @staticmethod
    def _clean_query(query: str) -> str:
        return query.strip().strip(" '\"‘’“”")
