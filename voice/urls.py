from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import call, StreamConsumer, TwillioOutgoing

websocket_urlpatterns = [
    path("voice/stream/", StreamConsumer.as_asgi()),
]

urlpatterns = [
    path("call/", call, name="call"),
    path("outgoing/", TwillioOutgoing.as_view(), name="outgoing"),

]