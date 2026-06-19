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