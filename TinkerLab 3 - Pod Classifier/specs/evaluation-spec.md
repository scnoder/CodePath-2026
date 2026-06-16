# Evaluation Spec — Pod Classifier

Complete this spec **before** writing any code for Milestone 3.

Use Plan or Ask mode to think through each blank field. When you're done,
your answers here become the blueprint for `compute_accuracy()` and
`compute_per_class_accuracy()` in `evaluate.py`.

---

## Background: What is evaluation?

After building a classifier, we need to know how well it works. Evaluation answers:
- **Overall:** What fraction of episodes did we classify correctly?
- **Per-class:** Are we better at some labels than others?

Both functions take the same inputs: a list of predicted labels and a list of
ground-truth labels, in the same order.

---

## compute_accuracy(predictions, ground_truth)

### What it does
Returns the fraction of predictions that exactly match the ground truth.

### Inputs

| Parameter | Type | Description |
|---|---|---|
| `predictions` | `list[str]` | Labels predicted by `classify_episode()`, one per episode. |
| `ground_truth` | `list[str]` | The correct labels, in the same order as `predictions`. |

### Output

| Return value | Type | Description |
|---|---|---|
| accuracy | `float` | A value between 0.0 and 1.0. |

---

### Spec fields — fill these in before writing code

**Formula:**

```
Correct is defined by if they match the ground_truth. The correct predictions are divided by the total predictions.
```

---

**Step-by-step logic:**

```
1. Match the predictions to the ground_truth
2. Sum up all of the predictions that match
3. Divide the sum by the total predictions made
```

---

**Edge case — what if both lists are empty?**

```
If both lists are zero the function should return -1.0 to show that nothing happened.
```

---

**Worked example:**

```
predictions  = ["interview", "solo", "panel", "interview"]
ground_truth = ["interview", "solo", "solo",  "narrative"]

Corrent predictions / total predictions = 2/4 = 0.5
```

---

## compute_per_class_accuracy(predictions, ground_truth)

### What it does
Returns accuracy broken down by each label. For each label in `VALID_LABELS`,
reports how many episodes with that ground-truth label were classified correctly.

### Inputs

| Parameter | Type | Description |
|---|---|---|
| `predictions` | `list[str]` | Labels predicted by `classify_episode()`. |
| `ground_truth` | `list[str]` | Correct labels, in the same order. |

### Output

A `dict` keyed by label. Each value is a dict with three keys:

```python
{
    "interview": {"correct": int, "total": int, "accuracy": float},
    "solo":      {"correct": int, "total": int, "accuracy": float},
    "panel":     {"correct": int, "total": int, "accuracy": float},
    "narrative": {"correct": int, "total": int, "accuracy": float},
}
```

---

### Spec fields — fill these in before writing code

**What does "correct" mean for a given class?**

```
An episode counts as correctly classified if the prediction matches the ground_truth.
```

---

**What does "total" mean for a given class?**

```
Total is the total number of episodes with a ground_truth label.
```

---

**Step-by-step logic:**

```
 1. Intialize the label
 2. Loop over the predictions and check if it is the proper label and add it to the counter
 3. Calculate the accuracy
 4. Add the values to the dictionary
 5. Return the dictionary
```

---

**Edge case — what if a class has no examples in ground_truth (total == 0)?**

```
The accuracy should be set to 0.0.
```

---

**Worked example:**

```
predictions  = ["interview", "interview", "solo", "panel", "panel"]
ground_truth = ["interview", "solo",      "solo", "panel", "narrative"]

[blank — fill in the per-class results table below]

label       correct  total  accuracy
----------  -------  -----  --------
interview   [blank]  [blank]  [blank]
solo        [blank]  [blank]  [blank]
panel       [blank]  [blank]  [blank]
narrative   [blank]  [blank]  [blank]
```

---

## Reflection questions (discuss at the checkpoint)

1. Your overall accuracy might be decent even if one class has very low accuracy.
   Why is per-class accuracy a more informative metric than overall accuracy alone?

   This per-class accuracy is more informative because it provides detailed information on what is making the accuracy low and which class doesn't have the best label description.

2. If `panel` episodes consistently get misclassified as `interview`, what does
   that tell you about your training labels or your prompt?

   This tells me that the training label for `panel` is not as specific or detailed as it is supposed to be and it should be better differentiated from `interview`.

3. You labeled 20 training episodes and evaluated on 20 test episodes (5 per class).
   How might the evaluation results change if you had labeled 100 training episodes?
   What if you had 200 test episodes?

   The evaluation results would be more specific and the total for the classes would not be the same and would vary the results.