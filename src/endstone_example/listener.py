import datetime

from endstone import ColorFormat
from endstone.event import EventPriority, PlayerJoinEvent, PlayerQuitEvent, ServerListPingEvent, event_handler
from endstone.plugin import Plugin


class ExampleListener:
    def __init__(self, plugin: Plugin) -> None:
        self._plugin = plugin

    @event_handler(priority=EventPriority.HIGHEST)
    def on_server_list_ping(self, event: ServerListPingEvent) -> None:
        event.motd = ColorFormat.BOLD + ColorFormat.AQUA + datetime.datetime.now().strftime("%c")
        addr = event.address
        event.level_name = f"Your IP is {ColorFormat.YELLOW}{addr.hostname}:{addr.port}{ColorFormat.RESET}"

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent) -> None:
        player = event.player
        self._plugin.logger.info(
            ColorFormat.YELLOW + f"{player.name}[/{player.address}] joined the game with UUID {player.unique_id}"
        )

        # example of explicitly removing one's permission of using /me command
        player.add_attachment(self._plugin, "minecraft.command.me", False)
        player.update_commands()  # don't forget to resend the commands

    @event_handler
    def on_player_quit(self, event: PlayerQuitEvent) -> None:
        player = event.player
        self._plugin.logger.info(ColorFormat.YELLOW + f"{player.name}[/{player.address}] left the game.")
