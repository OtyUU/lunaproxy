from luna_cache import LunaCache
from summary_manager import SummaryManager
from config import settings

cache = LunaCache(settings.LUNA_CACHE_PATH)
summary_manager = SummaryManager(settings.STATE_FILE)
