# Session: appointment reminder texts
2026-10-19. Dana Brooks (Ferncliff, customer marketing) with an AI assistant.
Ferncliff is scheduling software for dental clinics in the US. Clinics send these reminders to their patients through Ferncliff.

**Dana:** Write the default reminder text clinics send two days before an appointment.

**Assistant (draft 1):** "Hi Sam! This is a reminder from Brightsmile Dental Centre about your root canal appointment on Thursday, 14 November at 2:30pm. Please reply to confirm, or call us if you need to reschedule. If you've cancelled, ignore this message. We look forward to seeing you!"

**Dana:** Several things.
1. It has to fit in one SMS: 160 characters max, including the clinic name. Two texts look like spam and cost clinics double.
2. Never put the procedure in the text. "Root canal" on a lock screen is a privacy problem. Just "your appointment".
3. We're a US company and the clinics are American: American spelling. "Center", "canceled". Not "Centre", not "cancelled".
4. Every reminder ends with the reply options exactly like this: "Reply C to confirm, R to reschedule."
5. Date format is "Thu Nov 14, 2:30 PM". No ordinals, no "14 November".

**Assistant (draft 2):** "Brightsmile Dental Center: reminder of your appointment Thu Nov 14, 2:30 PM. Reply C to confirm, R to reschedule." (110 characters)

**Dana:** That's it. One more: no exclamation marks, and don't use the patient's first name. Shared phones.

**Assistant (draft 3):** confirmed same as draft 2.

**Dana:** Great. We need this for the 24-hour reminder and the same-day one too, same rules.
