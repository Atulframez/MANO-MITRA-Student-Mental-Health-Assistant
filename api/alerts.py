import os
from .db import get_db


TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')
TWILIO_FROM = os.getenv('TWILIO_FROM')




def check_and_send_alert(db, user_id, result):
# VERY SIMPLE: if result contains "danger" or negative dominant emotion, create alert
should_alert = False
reason = None
if isinstance(result, dict):
# emotion result
dom = result.get('dominant')
if dom and dom[0] in ('angry', 'sad') and dom[1] > 0.7:
should_alert = True
reason = f"Detected dominant emotion {dom[0]} ({dom[1]:.2f})"
if result.get('warning') and 'suicide' in str(result).lower():
should_alert = True
reason = 'suicidal content'


if should_alert:
# store alert
db.alerts.insert_one({'user_id': user_id, 'reason': reason})
# send external alert (Twilio/Email) - placeholder
_send_twilio_alert(user_id, reason)




def _send_twilio_alert(user_id, reason):
# Placeholder: implement Twilio/SendGrid send logic here.
print(f"ALERT for {user_id}: {reason}")