from endstone import ColorFormat
from endstone.event import PlayerJoinEvent, PlayerQuitEvent, event_handler
from endstone.plugin import Plugin


class ExampleListener:
    def __init__(self, plugin: Plugin) -> None:
        self._plugin = plugin

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent) -> None:
        player = event.player
        event.join_message = f"{ColorFormat.YELLOW}{player.name} joined the game"
        self._plugin.logger.info(f"{player.name} joined from {player.address}")

    @event_handler
    def on_player_quit(self, event: PlayerQuitEvent) -> None:
        event.quit_message = f"{ColorFormat.YELLOW}{event.player.name} left the game"
