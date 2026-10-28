# CallKaro FDE Assignment Submission Tracker

## 1. Submission Deliverables Required by CallKaro:
1. **Test call recordings** (Download the audio files or get public shareable links from the CallKaro call logs).
2. **The email address** used to create your CallKaro account.
3. **The exact agent name** created on the platform (`PG Finder - StaySathi`).

---

## 2. Pre-Submission Checklist:

- [ ] **Agent Name Check:** Is it exactly `PG Finder - StaySathi` on the dashboard?
- [ ] **Account Email:** ______________________________
- [ ] **Model Check:** OpenAI `gpt-4o-mini` selected?
- [ ] **STT & Voice Check:** Low-latency Indian English / Hindi voice selected?
- [ ] **Recordings Ready:**
  - [ ] Recording 1: Happy Path (Gurgaon / partial data)
  - [ ] Recording 2: Zero Metadata / Correction (Bangalore)
  - [ ] Recording 3: Busy Edge Case / Callback
  - [ ] (Optional) Recording 4: English language switch
- [ ] **Post-Call Data Verification:** In CallKaro dashboard call logs, did `city`, `monthly_budget`, `call_outcome`, etc. populate with 100% accuracy?

---

## 3. Submission Format (Email Template to `hiring@callkaro.ai` or submission form):

```text
Subject: FDE Take-Home Assignment Submission - PG Finder Voice AI Agent - [Your Name]

Hi CallKaro Team,

Please find my submission for the Forward Deployed Engineer (FDE) take-home assignment:

1. Exact Agent Name: PG Finder - StaySathi
2. CallKaro Account Email: [YOUR_CALLKARO_EMAIL_HERE]
3. Test Call Recordings:
   - Call 1 (Happy Path - Partial Metadata): [Link / Attachment]
   - Call 2 (Zero Metadata & Correction): [Link / Attachment]
   - Call 3 (Edge Case - Busy / Callback): [Link / Attachment]
   - Call 4 (Multilingual Mirroring - English): [Link / Attachment]

Key highlights implemented:
- Strict turn-taking (strictly 1 question per turn).
- Zero hallucination of missing metadata (empty fields are never spoken).
- Resilient edge case handling (busy, wrong number, not interested).
- Clean post-call variable extraction schema for downstream CRM/property matching.

Looking forward to your feedback!

Best regards,
[Your Name]
[Your Phone Number]
```

