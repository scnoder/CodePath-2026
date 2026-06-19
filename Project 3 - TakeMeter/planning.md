## Goals
The goal is too properly detect which types of posts are of the different types (discussions, news, etc.).

## Community
I chose this community because it has a lot of internal bias. Additionally most of the data is already be defined by users and the discourse can detect which posts are actually more biased or more informative than others.

## Data Information
The data is collected manually from r/realmadrid. It is collected manually and specially chosen for proper testing. There are 205 posts where 50 posts per label.

### Labels
| Reddit Flair | Label |
|------|-------------|
| Discussion | discussion |
| Team News | news |
| History | history |
| Rumor | rumor |

Data is stored in an excel sheet

The distinctions matter because a lot of the rumors are more question-like and more biased compared to news or history. This matters to the community because it adds more details for new viewers on what is new and unbiased and what isn't and could be fake.

## Metrics
I will use accuracy for all of the labels and per-label in order to deduce what is different in accuracy between classes and how to make sure what is the problem. I also plan to use an F1 score as a general score to understand and give the model a proper score. A "good enough" performance would be 85%+ accuracy and a high F1 score.

## Baseline Metrics
🎯 Baseline accuracy: 0.935  (evaluated on 31/31 parseable responses)

Per-class metrics (baseline):
              precision    recall  f1-score   support

  discussion       1.00      1.00      1.00         8
        news       0.88      0.88      0.88         8
     history       1.00      1.00      1.00         8
       rumor       0.86      0.86      0.86         7

    accuracy                           0.94        31
   macro avg       0.93      0.93      0.93        31
weighted avg       0.94      0.94      0.94        31
