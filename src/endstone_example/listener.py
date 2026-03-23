"""Event listener demonstrating how to respond to player events.

Listeners are separate classes (not the Plugin itself) that hold @event_handler
methods. Register them in on_enable with self.register_events(). This keeps
event handling logic organized and out of the main plugin class.
"""

from endstone import ColorFormat
from endstone.event import PlayerJoinEvent, PlayerQuitEvent, event_handler
from endstone.plugin import Plugin


class ExampleListener:
    def __init__(self, plugin: Plugin) -> None:
        # Keep a reference to the plugin so we can use its logger and config.
        self._plugin = plugin

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent) -> None:
        """Called when a player joins the server."""
        player = event.player

        # Modify the join message broadcast to all players.
        # ColorFormat constants add Minecraft formatting codes.
        event.join_message = f"{ColorFormat.YELLOW}{player.name} joined the game"

        # Log the player's network address (useful for debugging, not shown to players)
        self._plugin.logger.info(f"{player.name} joined from {player.address}")

    @event_handler
    def on_player_quit(self, event: PlayerQuitEvent) -> None:
        """Called when a player leaves the server."""
        event.quit_message = f"{ColorFormat.YELLOW}{event.player.name} left the game"
