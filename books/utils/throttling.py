from rest_framework.throttling import UserRateThrottle

class GeminiUserThrottle(UserRateThrottle):
    rate = '20/day'  # هر کاربر ۲۰ درخواست در روز