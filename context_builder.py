from luna_cache import LunaCache
from summary_manager import SummaryManager
from config import settings

class ContextBuilder:
    def __init__(self, cache: LunaCache, summary_manager: SummaryManager):
        self.cache = cache
        self.summary_manager = summary_manager

    def build(self) -> str:
        history = self.cache.get_recent_history(limit=settings.HISTORY_LINES)
        summary = self.summary_manager.get_summary()
        notes = self.summary_manager.get_notes()

        sections = []

        if notes:
            sections.append(f"## GAME INFO\n{notes}")
        
        if summary:
            sections.append(f"## STORY SUMMARY\n{summary}")

        if history:
            history_lines = []
            for h in history:
                history_lines.append(f"JP: {h['source']}\nRU: {h['trans']}")
            sections.append("## RECENT DIALOGUE\n" + "\n\n".join(history_lines))

        if not sections:
            return ""

        return "\n\n".join(sections) + "\n\n---\n"
