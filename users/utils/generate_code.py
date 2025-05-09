import random
from django.core.cache import cache
from django.core.signing import TimestampSigner, BadSignature
from django.conf import settings

signer = TimestampSigner()


def generate_code(email, action_type):
    code = str(random.randint(100000, 999999))
    cache.set(f"{action_type}_{email}_{code}", code, timeout=300)
    signed = signer.sign(f"{action_type}:{email}:{code}")
    return code, signed


def validate_code(email, action_type, input_code):
    print()
    cached_code = cache.get(f"{action_type}_{email}_{input_code}")
    print(cached_code)
    if cached_code:
        return cached_code == input_code
    else:
        return False
