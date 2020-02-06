import sys 
import base64
import zlib

data=zlib.compress(sys.stdin.read(), 9)
b64=base64.urlsafe_b64encode(data)
print(b64)