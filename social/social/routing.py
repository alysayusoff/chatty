from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import public_chat.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(URLRouter(public_chat.routing.websocket_urlpatterns)),
})