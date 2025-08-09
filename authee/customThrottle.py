from rest_framework.throttling import UserRateThrottle

class MyThrottle(UserRateThrottle):
    scope = 'mythrottle'