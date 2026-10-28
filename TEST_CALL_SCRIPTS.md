# Test Call Rehearsal Scripts for CallKaro

Use these exact scripts when placing test calls to your phone from the CallKaro dashboard. This ensures your submitted recordings sound natural, professional, and directly prove all key evaluation criteria.

---

## 🎙️ CALL 1: Happy Path with Partial Metadata (The Baseline Call)
**Purpose:** Prove that the agent confirms known data, asks only what's missing, and never mentions empty fields.

* **Set Metadata in CallKaro before calling:**
  - `customer_name`: Harsh
  - `city`: Gurgaon
  - `budget`: [LEAVE BLANK / NULL]
  - `gender`: [LEAVE BLANK / NULL]

### Dialogue Script:
* **Agent:** "Hello, kya meri baat Harsh ji se ho rahi hai? Main PG Finder se StaySathi bol rahi hoon."
* **You:** "Haanji Harsh bol raha hoon, bataiye."
* **Agent:** "Kya abhi 2 minute baat karne ka convenient time hai?"
* **You:** "Haan haan, boliye."
* **Agent:** "Aapne Gurgaon ke liye PG enquire kiya tha, right?"
* **You:** "Haanji, Gurgaon mein Cyber City ke paas dekh raha hoon."
* **Agent:** "Great! Aap single private room prefer karenge ya sharing option chalega?"
* **You:** "Mujhe single room chahiye."
* **Agent:** "Theek hai. Aapka approximate monthly budget kitna rahega?"
* **You:** "Around 15 se 18 hazaar tak."
* **Agent:** "Noted. Aap kab tak shift karne ka plan kar rahe hain?"
* **You:** "Next month ki first date ko, 1st November."
* **Agent:** "Aur aapka stay approximately kitne duration ka hoga?"
* **You:** "Around 6 months."
* **Agent:** "Awesome! Maine aapki requirements note kar li hain — Gurgaon, single room, 15 to 18 hazaar budget, 1st November se 6 months ke liye. Hamari team matching properties ki details aur photos 1 ghante mein WhatsApp pe bhej degi. Thank you so much, have a great day!"
* **You:** "Thank you, bye."

---

## 🎙️ CALL 2: Zero Metadata & User Correction (The Resilience Call)
**Purpose:** Prove the agent handles zero prior data gracefully, asks for caller name, and accepts user corrections without arguing.

* **Set Metadata in CallKaro before calling:**
  - All variables left completely EMPTY / BLANK.

### Dialogue Script:
* **Agent:** "Hello, main PG Finder se StaySathi bol rahi hoon. Aapne recently hamari website par PG search kiya tha, kya main aapka shubh naam jaan sakti hoon?"
* **You:** "Mera naam Aman hai."
* **Agent:** "Hi Aman ji! Kya abhi 2 minute baat kar sakte hain?"
* **You:** "Haanji, bataiye."
* **Agent:** "Aap kis city mein PG dhoondh rahe hain — Gurgaon, Bangalore ya Chennai?"
* **You:** "Actually pehle Chennai soch raha tha, par ab mujhe Bangalore mein chahiye, Koramangala side."
* **Agent:** "Noted Aman ji, main Bangalore update kar leti hoon. Aap single room dhoondh rahe hain ya sharing?"
* **You:** "Double sharing chalega."
* **Agent:** "Theek hai ji. Monthly budget kitna rahega aapka?"
* **You:** "Max 12,000."
* **Agent:** "Samajh gayi. Kab tak move in karna chahte hain?"
* **You:** "Within a week, immediately."
* **Agent:** "Aur stay duration kitna plan kiya hai aapne?"
* **You:** "Kam se kam 1 saal ke liye."
* **Agent:** "Great! Maine Bangalore mein double sharing PG under 12,000 note kar liya hai, immediate move-in ke liye. Hamari team verified options WhatsApp pe bhej degi. Thank you so much for your time!"
* **You:** "Thanks StaySathi, bye."

---

## 🎙️ CALL 3: Edge Case - Busy / In a Meeting (The UX Sense Call)
**Purpose:** Showcases real-world empathy, no pushiness, and capturing callback details cleanly.

* **Set Metadata in CallKaro before calling:**
  - `customer_name`: Harsh
  - `city`: Gurgaon

### Dialogue Script:
* **Agent:** "Hello, kya meri baat Harsh ji se ho rahi hai? Main PG Finder se StaySathi bol rahi hoon."
* **You:** "Haanji Harsh bol raha hoon, par main abhi ek meeting mein hoon, abhi baat nahi kar sakta."
* **Agent:** "Arre bilkul koi baat nahi ji! Kya main aapko shaam ko call karu ya saari details directly WhatsApp pe bhej doon?"
* **You:** "Aap shaam ko 7 baje call kar lijiye ya WhatsApp kar dijiye."
* **Agent:** "Noted ji! Main shaam ko 7 baje follow up karungi aur WhatsApp pe details drop kar doongi. Sorry for disturbing, have a great day!"
* **You:** "Thank you."

---

## 🎙️ CALL 4: English Language Switch (The Multilingual Mirroring Call)
**Purpose:** Proves the agent naturally mirrors language when a caller switches to full English.

### Dialogue Script:
* **Agent:** "Hello, kya meri baat Harsh ji se ho rahi hai? Main PG Finder se StaySathi bol rahi hoon."
* **You:** *(in English)* "Yes, Harsh this side. Could you please speak in English? What is this call regarding?"
* **Agent:** *(switches to English immediately)* "Sure Harsh! I'm calling from PG Finder regarding your inquiry for accommodation on our website. Do you have 2 quick minutes to discuss your preferences?"
* **You:** "Yes, sure. I'm moving to Chennai for an on-site project."
* **Agent:** "Great! What is your preferred room type and monthly budget in Chennai?"
* **You:** "Looking for a single room, budget is around 20,000 per month."
* **Agent:** "Understood. When are you planning to move in?"
* **You:** "By mid of next month, for about 6 months."
* **Agent:** "Perfect! I've noted down Chennai, single room, 20k budget, mid-next month for 6 months. Our property team will share the best verified options on your WhatsApp shortly. Thank you for your time, have a great day!"
* **You:** "Thanks, have a good day."

