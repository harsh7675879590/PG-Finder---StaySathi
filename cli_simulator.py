import asyncio
import sys
from app.agent.prompts import build_system_prompt
from app.agent.llm import llm_client
from app.agent.extractor import extract_post_call_data

def run_cli_simulation():
    print("=" * 60)
    print("  PG FINDER - STAYSATHI VOICE AI TERMINAL SIMULATOR")
    print("=" * 60)
    print("Simulating inbound/outbound call session...\n")

    # Step 1: Input metadata or defaults
    name = input("Enter customer name [Press Enter for default 'Harsh']: ").strip() or "Harsh"
    city = input("Enter city [Press Enter for default 'Gurgaon']: ").strip() or "Gurgaon"
    budget = input("Enter budget [Press Enter to leave blank / missing]: ").strip() or None

    metadata = {
        "customer_name": name,
        "phone_number": "+91 98112 34567",
        "city": city,
        "gender": None,
        "budget": budget
    }

    # Step 2: System Prompt & Opening
    sys_prompt = build_system_prompt(metadata)
    first_msg = f"Hello, kya meri baat {name} ji se ho rahi hai? Main PG Finder se StaySathi bol rahi hoon."
    
    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "assistant", "content": first_msg}
    ]

    print("\n" + "-" * 50)
    print(f"StaySathi: {first_msg}")
    print("-" * 50)

    # Conversation loop
    while True:
        try:
            user_input = input("\nYou (Caller): ").strip()
            if not user_input or user_input.lower() in ["bye", "exit", "quit", "end"]:
                print("\n[Call Ended by user]")
                break

            messages.append({"role": "user", "content": user_input})
            reply = llm_client.chat_turn(messages)
            messages.append({"role": "assistant", "content": reply})

            print(f"\nStaySathi: {reply}")

            if any(term in reply.lower() for term in ["have a wonderful day", "have a great day", "thank you so much for your time", "bye"]):
                print("\n[Call concluded naturally by StaySathi]")
                break
        except (KeyboardInterrupt, EOFError):
            print("\n[Call terminated]")
            break

    # Post-call Extraction
    print("\n" + "=" * 60)
    print("  RUNNING POST-CALL DATA EXTRACTION & ANALYSIS...")
    print("=" * 60)
    extracted = extract_post_call_data(messages, metadata)
    import json
    print(json.dumps(extracted, indent=2))
    print("\n[Data successfully saved to PG Finder CRM schema]")

if __name__ == "__main__":
    run_cli_simulation()
