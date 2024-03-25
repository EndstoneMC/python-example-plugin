from endstone.event import ServerListPingEvent, event_handler, EventPriority
from endstone.util import ColorFormat


class ExampleListener:
    @event_handler(priority=EventPriority.HIGHEST)
    def on_server_list_ping(self, event: ServerListPingEvent):
        event.motd = ColorFormat.BOLD + ColorFormat.AQUA + "Example MOTD"
        event.level_name = f"Your IP is {ColorFormat.YELLOW}{event.remote_host}:{event.remote_port}{ColorFormat.RESET}"
