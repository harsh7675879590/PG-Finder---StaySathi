import json
import logging
from typing import List, Dict, Any
from app.config import settings
from app.models import ExtractedCallData

logger = logging.getLogger(__name__)

EXTRACTION_SYSTEM_PROMPT = """You are a senior data extraction specialist for PG Finder CRM.
Analyze the following transcript between our voice AI agent 'StaySathi' and a customer.
Extract structured details into the exact JSON schema provided.

Guidelines:
- city: Must be one of ["Gurgaon", "Bangalore", "Chennai", "Other"] or null.
- monthly_budget: Standardize to INR number or string (e.g. "15k" -> "15000").
- call_outcome: Must be one of ["interested", "busy_callback", "wrong_number", "not_interested"].
- If customer was busy, extract requested callback_time or "WhatsApp".
- call_summary: Provide a crisp 1-2 sentence overview of customer accommodation needs.

Output ONLY valid raw JSON with no markdown wrapping.
"""

def extract_post_call_data(transcript: List[Dict[str, str]], metadata: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Parses full call transcript and returns structured CRM data.
    """
    metadata = metadata or {}
    formatted_transcript = ""
    for turn in transcript:
        role = turn.get("role", "speaker")
        content = turn.get("content", "")
        formatted_transcript += f"{role.upper()}: {content}\n"

    # Default baseline extraction
    default_data = {
        "caller_name": metadata.get("customer_name") or "Unspecified",
        "city": metadata.get("city") or "Other",
        "preferred_locality": None,
        "gender_pg_type": metadata.get("gender") or "Unspecified",
        "monthly_budget": metadata.get("budget") or "Unspecified",
        "move_in_date": "Immediate",
        "stay_duration": "6 months",
        "call_outcome": "interested",
        "callback_time": None,
        "call_summary": "Call completed successfully. Requirements registered for PG matching."
    }

    # Attempt LLM extraction if client available
    from app.agent.llm import llm_client
    if llm_client.client:
        try:
            prompt_content = f"METADATA GIVEN:\n{json.dumps(metadata)}\n\nCALL TRANSCRIPT:\n{formatted_transcript}"
            
            response = llm_client.client.chat.completions.create(
                model=llm_client.model,
                messages=[
                    {"role": "system", "content": EXTRACTION_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt_content}
                ],
                temperature=0.1,
                response_format={"type": "json_object"} if "gpt" in llm_client.model else None
            )
            raw_json = response.choices[0].message.content.strip()
            # Clean possible markdown blocks
            if raw_json.startswith("```"):
                raw_json = raw_json.split("\n", 1)[1].rsplit("\n", 1)[0].strip()
            extracted = json.loads(raw_json)
            return extracted
        except Exception as e:
            logger.error(f"Post-call LLM extraction failed: {e}. Falling back to heuristic extractor.")

    # Heuristic fallback if LLM not present
    lower_t = formatted_transcript.lower()
    if "busy" in lower_t or "meeting" in lower_t or "shaam ko" in lower_t:
        default_data["call_outcome"] = "busy_callback"
        default_data["callback_time"] = "Evening / WhatsApp requested"
        default_data["call_summary"] = "Caller was occupied; requested follow up later."
    elif "wrong number" in lower_t or "galat number" in lower_t:
        default_data["call_outcome"] = "wrong_number"
        default_data["call_summary"] = "Wrong number. Removed from calling list."
    elif "not interested" in lower_t or "nahi chahiye" in lower_t:
        default_data["call_outcome"] = "not_interested"
        default_data["call_summary"] = "Caller indicated they do not need accommodation currently."
    else:
        for c in ["gurgaon", "bangalore", "chennai"]:
            if c in lower_t:
                default_data["city"] = c.capitalize()
                break
        if "single" in lower_t:
            default_data["gender_pg_type"] = "Single Room"
        elif "sharing" in lower_t or "double" in lower_t:
            default_data["gender_pg_type"] = "Sharing"

    return default_data

