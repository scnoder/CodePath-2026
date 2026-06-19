# Takemeter
Contains a colab notebook and the CSV file which contains data from r/realmadrid.

## Dataset
`realmadrid posts.csv` contains 205 items labeled as discussion, history, rumors, and news.
 
| Reddit Flair | Label | Descriptions |
|------|-------------|----------------|
| Discussion | discussion | Fan-written opinion posts where the author analyzes a player, match, or tactical situation and shares their personal take. Usually multi-sentence, conversational in tone, and ends with a question or open-ended thought inviting community debate. No news source is cited. |
| Team News | news | Short, factual headline-style statements reporting a confirmed or developing event — signings, contracts, lineups, awards, managerial changes. Usually one or two sentences. Often references a real person taking a specific action (signing, departing, starting, winning). |
| History | history | Posts recalling a past Real Madrid moment, typically anchored to a specific date ("OTD," "X years ago today"). Written with nostalgia or reverence, referencing a historic match, goal, or milestone. May include the author's emotional reaction to the memory. |
| Rumor | rumor | Transfer or managerial speculation attributed to a journalist, outlet, or source (e.g. "Cadena SER," "El Confidencial," Twitter handles). The language signals uncertainty — words like "wants," "set to," "close to," "interested in." Not confirmed, always tied to a named source. |

## Running
Pull the Jupyter notebook and run to properly. Upload the dataset provided and use the API key to run Groq.

## Confusion Matrix

Discussion (8 total): 
- Perfect
- All 8 predicted correctly

News (8 total):
- Bad
- Only 1 correct
- 2 got misclassified as discussion
- 5 got misclassified as rumor
- The model can barely distinguish news from rumor.

History (8 total): 
- Half right
- 4 correct
- 4 misclassified as rumor
- The model is confusing historical posts with rumors.

Rumor (7 total): 
- Good
- 5 correct
- 2 misclassified as discussion.

The main issue is that most of the other data aside from disucssion is being confused as a rumor. Posts without an OTD seem to be more as rumors instead of history.

### Wrong Predictions
```
--- #1 ---
Text:      José Mourinho is the new Real Madrid coach. Presented Next week.
True:      news
Predicted: rumor  (confidence: 0.26)

--- #2 ---
Text:      [COPE] Real Madrid have offered 10 million for Brahim Diaz but City want 20 million but the clubs are close to reaching an agreement on the transfer of the Spaniard. if he joins, Brahim won't be sent ...
True:      rumor
Predicted: discussion  (confidence: 0.27)

--- #3 ---
Text:      Kylian Mbappe is BACK in training. He will be included in the squad against City
True:      news
Predicted: discussion  (confidence: 0.27)
```
These have all been classified as wrong. The issue with the first one is because there is the header is short which makes the model think that it is a rumor because some of the rumors seems to have smaller data.

The issue with the second one is that the length of the post.

The reason the third one seems to be thought of as discussion is because of the capitalized letters which makes the model think that this is exaggerated text.

## Results Comparison
Model                               Accuracy
---------------------------------------------
Zero-shot baseline (Groq)              0.935
Fine-tuned DistilBERT                  0.581
---------------------------------------------

Fine-tuning regression: 0.355

## Reflection
What it missed was the structural and contextual difference between news and rumor. Both are short, both cite external sources, both talk about transfers and contracts. The difference is epistemic — one is confirmed, one isn't — and that distinction lives in words like "close to," "set to," "interested in" versus "signs," "confirmed," "announced." That's a subtle boundary, and with only ~50 examples per class it wasn't enough data to learn it reliably. The model essentially collapsed news into rumor.

The deeper issue is that the label definitions were human and intentional, but the training signal was statistical and accidental. The model didn't learn what each label means — it learned which words tend to appear in each label's posts. For a small dataset like this, those two things diverge significantly, and the confusion matrix is showing exactly where they diverge most.

## AI Usage
I asked it about shuffling my dataset because I forgot to. Other than that I didnt use Claude for much.