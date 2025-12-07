import numpy as np
from io import BytesIO
from PIL import Image


# try fer first
try:
from fer import FER
FER_AVAILABLE = True
except Exception:
FER_AVAILABLE = False




def analyze_image_bytes(image_bytes: bytes) -> dict:
img = Image.open(BytesIO(image_bytes)).convert('RGB')
img_np = np.array(img)


if FER_AVAILABLE:
detector = FER(mtcnn=True)
res = detector.detect_emotions(img_np)
if not res:
return {'error': 'No face detected'}
# pick the largest face
best = max(res, key=lambda x: x['box'][2] * x['box'][3])
emotions = best['emotions']
dominant = max(emotions.items(), key=lambda kv: kv[1])
return {'emotions': emotions, 'dominant': dominant}
else:
# fallback: very simple heuristic using average brightness as stress proxy
gray = np.array(img.convert('L'))
avg = gray.mean()
# lower brightness -> possible tired/stress (very rough)
proxy = 'low_energy' if avg < 80 else 'neutral'
return {'warning': 'fer library not installed; returning proxy', 'proxy': proxy, 'avg_brightness': float(avg)}