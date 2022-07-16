from django.apps import AppConfig

class ChattyConfig(AppConfig):
    name = 'chatty'

    # import signals
    def ready(self):
        import chatty.signals