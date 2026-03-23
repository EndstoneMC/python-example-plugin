"""Example plugin demonstrating commands, configuration, and lifecycle methods."""

from endstone import Player
from endstone.command import Command, CommandSender, ConsoleCommandSender
from endstone.plugin import Plugin

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
    }

    # Permissions are declared separately from commands. The "default" field controls
    # who gets the permission automatically: True = everyone, "op" = operators only,
    # False = no one (must be explicitly granted).
    permissions = {
        "example.command.hello": {
            "description": "Allow users to use the /hello command.",
            "default": True,
        },
    }

    def on_enable(self) -> None:
        """Called when the plugin is enabled. Use this for setup."""

        # Copies config.toml to the plugin's data folder on first run.
        # On subsequent runs it does nothing, preserving the user's edits.
        self.save_default_config()

        # Register event listeners. Endstone scans the object for @event_handler
        # methods and hooks them into the event system.
        self.register_events(ExampleListener(self))

        self.logger.info("ExamplePlugin enabled!")

    def on_disable(self) -> None:
        """Called when the plugin is disabled. Use this for cleanup."""
        self.logger.info("ExamplePlugin disabled!")

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
                # Read the greeting from config.toml (editable by server admins)
                greeting = self.config["greeting"]

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

        return True
