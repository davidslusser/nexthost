from django.apps import AppConfig


class HostmgrConfig(AppConfig):
    name = 'hostmgr'

    verbose_name = "Host Manager Application"

    def ready(self):
        import hostmgr.signals
