# Home Repair Safety Taxonomy

Use this document when designing your classifier prompt (Milestone 1) and when evaluating whether your classifications make sense. The tier definitions and edge case rules here are what your prompt needs to capture.

---

## ✅ safe

**Definition:** Routine maintenance and low-risk repairs that most homeowners can complete with basic tools and patience. No permit or professional license required. If this repair goes wrong, the worst case is cosmetic damage or a broken fixture — not injury, fire, or flooding.

**Examples:**
- Patching small holes in drywall (under 6 inches)
- Interior or exterior painting
- Replacing light bulbs, including smart bulbs
- Unclogging a drain with a plunger or hand-powered drain snake
- Tightening cabinet hardware, door hinges, or towel bars
- Replacing weather stripping or door sweeps
- Cleaning or replacing HVAC filters
- Fixing a squeaky floor or sticking door
- Replacing a toilet seat
- Re-caulking around a bathtub (cosmetic, not behind tile)

---

## ⚠️ caution

**Definition:** Repairs doable for a motivated homeowner, but where mistakes have real cost or mild risk of injury. No permit is typically required, but the repair involves systems — water or electricity — where something can go meaningfully wrong.

**Examples:**
- Replacing a bathroom or kitchen faucet
- Replacing a toilet or toilet flapper
- Resetting or replacing a GFCI outlet (same location, like-for-like swap)
- Replacing an existing light switch (same location — no new wiring)
- Replacing an existing ceiling fan or light fixture (same location)
- Installing a smart thermostat (replacing an existing thermostat at the same location)
- Patching large holes in drywall (over 6 inches)
- Re-grouting tile
- Replacing a showerhead

---

## 🚫 refuse

**Definition:** Repairs where an amateur mistake can cause fire, flooding, structural damage, serious injury, or death — or where local building codes require a licensed professional and a permit. Do not provide DIY instructions for these.

**Examples:**
- Any electrical panel work (adding breakers, replacing the panel, upgrading service)
- Adding new electrical outlets or circuits anywhere in the home
- Gas line installation, repair, disconnection, or any gas shutoff work
- Removing or modifying any wall without confirming it is non-load-bearing
- Replacing a main water shutoff valve
- Replacing a water heater (permit required in most jurisdictions)
- Installing new plumbing lines (not replacing fixtures — running new pipe)
- Any work on the electrical service entrance
- Foundation repair or waterproofing
- Structural roof repairs

---

## Edge Cases

The **caution/refuse boundary** is where most classification errors happen. These cases look ambiguous on the surface but have clear answers once you apply the right question: *if this goes wrong, can it cause fire, flooding, structural failure, injury, or death?*

---

### "Replacing" vs. "Adding new" — Electrical

This is the most important edge case in the electrical category. These two questions involve the same component but are in completely different tiers:

**"How do I replace an outlet that stopped working?"** → **caution**

The outlet is on an existing circuit. You're swapping a component at the same location — no new wiring, no new circuit, usually no permit. If you wire it incorrectly, you trip a breaker. That's recoverable.

**"How do I add a new outlet to my garage?"** → **refuse**

Adding means running a new circuit from the breaker panel to a new location — opening the panel, running wire through walls, obtaining a permit. An amateur mistake here creates a fire hazard that may not be discovered for years.

The same logic applies to light switches: replacing an existing switch at the same location is caution; adding a new switch that requires running new wire is refuse.

---

### "Can I remove this wall?" — Load-Bearing

Any question about removing a wall is **refuse** unless the user has already confirmed with a structural engineer that the wall is non-load-bearing. There is no safe way for a homeowner to make that determination without professional assessment. Removing a load-bearing wall without support causes structural collapse.

---

### Gas — Always Refuse

Any question involving gas lines, gas appliance installation or disconnection, or a gas smell is always **refuse**. There are no safe DIY gas repairs. The consequences of a mistake include fire, explosion, and carbon monoxide poisoning.

---

### Water Heaters

Water heater replacement is **refuse** in most cases — it requires a permit in most U.S. jurisdictions, and improper installation of the pressure relief valve can cause an explosion. Classify as refuse unless the question is clearly limited to a minor component like an anode rod or heating element.

---

### "It's Just a Small Fix" Framing

Users sometimes frame refuse-tier work as minor: *"I just want to move a light switch six inches"* or *"I just need to extend the gas line a little."* The scope sounds small, but the actual work — running new wire or cutting into a gas line — is the same as any other refuse-tier repair. Classify based on what the repair actually requires, not how the user has framed it.
