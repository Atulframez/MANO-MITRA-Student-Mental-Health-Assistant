from transformers import pipeline
from tenacity import retry, wait_exponential


# initialize sentiment / conversational pipeline lazily
_sentiment = None


@retry(wait=wait_exponential(min=1, max=10))
def _get_sentiment_pipeline():
global _sentiment
if _sentiment is None:
_sentiment = pipeline('sentiment-analysis')
return _sentiment




def simple_rule_response(text):
text_low = text.lower()
if any(w in text_low for w in ['suicide', 'kill myself', 'end my life']):
return ("I hear you — I'm really sorry you're feeling this way. If you are in danger, "
"please contact local emergency services now. If you want, I can connect you to a human counselor.")
return None




def get_bot_response(text, user_id=None):
# Rule-based high-priority checks
rule = simple_rule_response(text)
if rule:
return rule


# Sentiment-based reply (simple)
sentiment = _get_sentiment_pipeline()(text)[0]
label = sentiment['label']
score = sentiment['score']


if label == 'NEGATIVE' and score > 0.85:
return "I’m sorry you’re going through a tough time. Would you like some breathing exercises or to talk to a counselor?"
elif label == 'POSITIVE':
return "That’s good to hear. Do you want tips to keep this momentum?"
else:
return "I’m here to listen. Tell me more about what’s on your mind."