# Code Review Notes

Fill this in as you work through the milestones. Each section mirrors the structure of a real GitHub pull request review.

---

## PR #1 — Bulk Purchase (`pr1_bulk_purchase.py`)

### Summary
*What does this PR do? (1–2 sentences in your own words)*

> This PR adds a bulk purchase endpoint that marks all items in a grocery list as purchased. It updates the purchase metadata for items and returns the number of purchased items.

### Issues

For each issue you find, note: where it is (file + function), what's wrong, and why it matters in production.

**Issue 1**
- Location: `pr1_bulk_purchase.py` — `purchase_all_items()`
- What's wrong: The query uses `Item.query.filter_by(list_id=list_id).all()`, which retrieves every item in the list instead of only items that are not already purchased.
- Why it matters: Already-purchased items are modified again. This can overwrite purchase history and change the `purchased_by` value of an item that was purchased by another user.
- Suggested fix: Filter the query to only return unpurchased items, for example by adding `is_purchased=False` to the query conditions.

**Issue 2**
- Location: `pr1_bulk_purchase.py` — `purchase_all_items()`
- What's wrong: The function returns `len(items)`, but `items` contains every item in the list, including items that were already purchased before this request.
- Why it matters: The API response gives an inaccurate count. A caller may think the operation purchased more items than it actually changed.
- Suggested fix: Return the number of items that were actually updated from unpurchased to purchased.

**Issue 3** *(if found)*
- Location: `app.py` — purchase-all route
- What's wrong: The route uses `data.get("user_id")` without checking whether `user_id` exists in the request body.
- Why it matters: Requests without a user ID can succeed and store `None` as `purchased_by`, creating invalid purchase records.
- Suggested fix: Validate that `user_id` is provided before calling `purchase_all_items()`. Return a 400 error if it is missing.

### Questions for the Author
*Things you're uncertain about — design choices that could be intentional or bugs depending on intent.*

> Should already-purchased items be skipped or should the endpoint intentionally allow users to reassign purchases? The current behavior overwrites the previous purchaser, which seems risky.
>
> Should the response count represent the total number of purchased items in the list or only the items changed by this request? The PR description suggests it should be the number of newly purchased items.

### Verdict
- [ ] Approve — ship it
- [X] Request Changes — needs fixes before merging
- [ ] Comment — needs discussion before a verdict

**Rationale** *(1–2 sentences)*:

> This PR has correctness issues that can overwrite existing purchase data and return misleading results. The endpoint should only update unpurchased items and validate required inputs before merging.

---

## PR #2 — List Stats (`pr2_list_stats.py`)

### Summary
*What does this PR do? (1–2 sentences in your own words)*

>

### Issues

**Issue 1**
- Location:
- What's wrong:
- Why it matters:
- Suggested fix:

**Issue 2**
- Location:
- What's wrong:
- Why it matters:
- Suggested fix:

**Issue 3** *(if found)*
- Location:
- What's wrong:
- Why it matters:
- Suggested fix:

### Questions for the Author
*A good code review often surfaces design questions, not just bugs. What would you want to clarify before approving?*

>

### Verdict
- [ ] Approve — ship it
- [ ] Request Changes — needs fixes before merging
- [ ] Comment — needs discussion before a verdict

**Rationale** *(1–2 sentences)*:

>

---

## Reflection

*Answer after completing both reviews.*

**1.** Which issue was hardest to spot, and why?

>

**2.** Which issues do you think an LLM reviewer (like Claude reviewing its own code) would most likely miss? Why?

>

**3.** One thing you'd add to a code review checklist for AI-generated backend code:

>
