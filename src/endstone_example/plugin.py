from endstone import Player
from endstone.command import Command, CommandSender, ConsoleCommandSender
from endstone.plugin import Plugin

from endstone_example.listener import ExampleListener


class ExamplePlugin(Plugin):
    prefix = "ExamplePlugin"
    api_version = "0.11"

    commands = {
        "hello": {
            "description": "Send a greeting",
            "usages": ["/hello"],
            "permissions": ["example.command.hello"],
        },
    }

    permissions = {
        "example.command.hello": {
            "description": "Allow users to use the /hello command.",
            "default": True,
        },
    }

    def on_enable(self) -> None:
        self.save_default_config()
        self.register_events(ExampleListener(self))
        self.logger.info("ExamplePlugin enabled!")

    def on_disable(self) -> None:
        self.logger.info("ExamplePlugin disabled!")

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        match command.name:
            case "hello":
                greeting = self.config["greeting"]  # from config.toml

                # Use isinstance to check the sender type
                if isinstance(sender, Player):
                    sender.send_message(f"{greeting}, {sender.name}!")
                elif isinstance(sender, ConsoleCommandSender):
                    self.logger.info(f"{greeting} from the console!")
                else:
                    sender.send_message(f"{greeting}!")

        return True
