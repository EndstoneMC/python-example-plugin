"""Example plugin demonstrating commands, configuration, and lifecycle methods."""

from endstone import Player
from endstone.command import Command, CommandSender, ConsoleCommandSender
from endstone.plugin import Plugin
from typing_extensions import override

from endstone_example.listener import ExampleListener


class ExamplePlugin(Plugin):
    # The prefix shown in log messages, e.g. [ExamplePlugin] Hello!
    prefix = "ExamplePlugin"

    # Must match the major.minor version of the Endstone API you are targeting.
    api_version = "0.11"

    # Commands are declared as a dict. Each key is the command name, and the value
    # configures how it appears in-game. The "permissions" list controls who can use it.
    commands = {
        "hello": {
            "description": "Send a greeting",
            "usages": ["/hello"],
            "permissions": ["example.command.hello"],
        },
        "broadcast": {
            "description": "Broadcast a message to all players",
            "usages": ["/broadcast <message: message>"],
            "permissions": ["example.command.broadcast"],
        },
    }

    # Permissions are declared separately from commands. The "default" field controls
    # who gets the permission automatically: True = everyone, "op" = operators only,
    # False = no one (must be explicitly granted).
    permissions = {
        "example.command.hello": {
            "description": "Allow users to use the /hello command.",
            "default": True,
        },
        "example.command.broadcast": {
            "description": "Allow users to use the /broadcast command.",
            "default": "op",
        },
    }

    @override
    def on_enable(self) -> None:
        """Called when the plugin is enabled. Use this for setup."""

        # Copies config.toml to the plugin's data folder on first run.
        # On subsequent runs it does nothing, preserving the user's edits.
        self.save_default_config()

        # Register event listeners. Endstone scans the object for @event_handler
        # methods and hooks them into the event system.
        self.register_events(ExampleListener(self))

        self.logger.info("ExamplePlugin enabled!")

    @override
    def on_disable(self) -> None:
        """Called when the plugin is disabled. Use this for cleanup."""
        self.logger.info("ExamplePlugin disabled!")

    @override
    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        """Called when a player or the console runs one of this plugin's commands.

        Args:
            sender: Who ran the command (Player, ConsoleCommandSender, etc.).
            command: The command that was executed.
            args: The arguments passed after the command name.

        Returns:
            True if the command was handled successfully.
        """
        match command.name:
            case "hello":
                # Use .get() with a default to avoid crashing if the key is missing
                # from config.toml (e.g. if the admin deleted it).
                greeting = self.config.get("greeting", "Hello")

                # Use isinstance to tailor behavior to the sender type.
                # This is a common pattern since players and the console have
                # different capabilities (e.g. players can receive chat messages,
                # but the console can only write to the log).
                if isinstance(sender, Player):
                    sender.send_message(f"{greeting}, {sender.name}!")
                elif isinstance(sender, ConsoleCommandSender):
                    self.logger.info(f"{greeting} from the console!")
                else:
                    sender.send_message(f"{greeting}!")

            case "broadcast":
                # args contains everything after the command name.
                # The "message" parameter type captures the rest of the line as one string.
                if not args:
                    sender.send_error_message("Usage: /broadcast <message>")
                    return False

                message = " ".join(args)
                prefix = self.config.get("broadcast_prefix", "[Broadcast]")
                self.server.broadcast_message(f"{prefix} {message}")

        return True
