import os
import json
import logging
from typing import List, Dict, Any, Optional
from app.config import settings

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.model = settings.LLM_MODEL
        self._init_client()

    def _init_client(self):
        self.client = None
        if settings.OPENAI_API_KEY and self.provider == "openai":
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
                logger.info(f"Initialized OpenAI client with model: {self.model}")
            except Exception as e:
                logger.warning(f"Could not initialize OpenAI client: {e}")
        elif settings.GROQ_API_KEY and self.provider == "groq":
            try:
                from groq import Groq
                self.client = Groq(api_key=settings.GROQ_API_KEY)
                logger.info(f"Initialized Groq client with model: {self.model}")
            except Exception as e:
                logger.warning(f"Could not initialize Groq client: {e}")
        else:
            # Check if any key is available
            if settings.OPENAI_API_KEY:
                from openai import OpenAI
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
                self.provider = "openai"
                self.model = "gpt-4o-mini"
            elif settings.GROQ_API_KEY:
                from groq import Groq
                self.client = Groq(api_key=settings.GROQ_API_KEY)
                self.provider = "groq"
                self.model = "llama-3.3-70b-versatile"
            else:
                logger.warning("No OPENAI_API_KEY or GROQ_API_KEY provided. Operating in Mock/Simulation fallback mode.")

    def chat_turn(self, messages: List[Dict[str, str]], temperature: float = 0.4) -> str:
        """
        Takes conversation history and returns StaySathi's next turn.
        """
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=150
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                logger.error(f"Error invoking {self.provider} LLM: {e}")
                # Fallback to smart rule-based response if API call fails
                return self._mock_fallback_response(messages)
        else:
            return self._mock_fallback_response(messages)

    def _mock_fallback_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Deterministic mock fallback for local testing without an active API key.
        """
        last_user_msg = ""
        for m in reversed(messages):
            if m.get("role") == "user":
                last_user_msg = m.get("content", "").lower()
                break

        if not last_user_msg:
            return "Hello, main PG Finder se StaySathi bol rahi hoon. Kya 2 minute baat karne ka sahi time hai?"
        
        if any(w in last_user_msg for w in ["busy", "meeting", "drive", "driving", "driving"]):
            return "Arre bilkul koi baat nahi ji! Kya main aapko shaam ko call karu ya saari details WhatsApp pe bhej doon?"
        
        if any(w in last_user_msg for w in ["wrong number", "galat number"]):
            return "Oh, really sorry for disturbing you! Main hamare system se ye number abhi remove kar deti hoon. Have a good day!"
            
        if any(w in last_user_msg for w in ["not interested", "nahi chahiye", "already mila"]):
            return "Koi problem nahi ji! Agar future mein PG ki requirement ho toh PG Finder zaroor yaad rakhiyega. Thank you!"

        if any(w in last_user_msg for w in ["gurgaon", "bangalore", "chennai", "city"]):
            return "Noted! Aap single private room prefer karenge ya double sharing option chalega?"

        if any(w in last_user_msg for w in ["single", "sharing", "double", "private"]):
            return "Theek hai ji. Aapka approximate monthly budget kitna rahega?"

        if any(w in last_user_msg for w in ["15000", "12000", "10000", "20000", "budget", "k", "hazaar"]):
            return "Great! Aap kab tak shift karne ka plan kar rahe hain?"

        if any(w in last_user_msg for w in ["immediate", "next month", "november", "tarikh", "week"]):
            return "Awesome! Maine aapki requirements note kar li hain. Hamari property team verified options 1 ghante mein aapke WhatsApp par share kar degi. Thank you so much, have a great day!"

        return "Samajh gayi! Kya aapka monthly budget around 15 hazaar ke aas-paas hai?"

llm_client = LLMClient()

