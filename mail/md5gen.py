import hmac
import base64
import hashlib

k='stas'

print hashlib.md5(k).hexdigest()
