import json
import os
import httpx
from config import settings
from typing import Dict, Any

class SummaryManager:
    def __init__(self, state_file: str):
        self.state_file = state_file
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "summary": "",
            "notes": "",
            "last_summary_line_count": 0
        }

    def _save_state(self):
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)

    def get_summary(self) -> str:
        return self.state.get("summary", "")

    def get_notes(self) -> str:
        return self.state.get("notes", "")

    def update_notes(self, notes: str):
        self.state["notes"] = notes
        self._save_state()

    def update_summary(self, summary: str):
        self.state["summary"] = summary
        self._save_state()

    async def generate_summary(self, history: list):
        if not history:
            return

        # Prepare prompt for summarization
        history_text = "\n".join([f"JP: {h['source']}\nRU: {h['trans']}" for h in history])
        
        prompt = f"""Based on the following recent translation history, update the story summary. 
The summary should be concise and include key events and character developments.

Current Summary:
{self.get_summary()}

Recent History:
{history_text}

New Summary:"""

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.LLM_BASE_URL}/chat/completions",
                    headers={"Authorization": f"Bearer {settings.LLM_API_KEY}"},
                    json={
                        "model": "gpt-3.5-turbo", # Or another model
                        "messages": [{"role": "user", "content": prompt}]
                    },
                    timeout=60.0
                )
                if response.status_code == 200:
                    new_summary = response.json()['choices'][0]['message']['content'].strip()
                    self.update_summary(new_summary)
                else:
                    print(f"Error generating summary: {response.text}")
        except Exception as e:
            print(f"Exception during summary generation: {e}")

    def should_generate_summary(self, current_line_count: int) -> bool:
        last_count = self.state.get("last_summary_line_count", 0)
        if current_line_count >= last_count + settings.SUMMARY_EVERY_N_LINES:
            self.state["last_summary_line_count"] = current_line_count
            self._save_state()
            return True
        return False
