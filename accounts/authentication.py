from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.throttling import AnonRateThrottle

class LoginThrottle(AnonRateThrottle):
    scope = "login"

class LoginAPIView(TokenObtainPairView):
    throttle_classes = [LoginThrottle]
