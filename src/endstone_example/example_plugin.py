import datetime

from endstone.command import Command, CommandSender
from endstone.event import EventPriority, ServerLoadEvent, event_handler
from endstone.plugin import Plugin

from endstone_example.example_listener import ExampleListener
from endstone_example.python_command import PythonCommandExecutor


class ExamplePlugin(Plugin):
    name = "PythonExamplePlugin"
    version = "0.4.0"
    api_version = "0.4"
    description = "Python example plugin for Endstone servers"
    authors = ["Endstone Developers <hello@endstone.dev>"]
    website = "https://github.com/EndstoneMC/python-example-plugin"
    load = "POSTWORLD"

    commands = {
        "python": {
            "description": "Zen of python",
            "usages": ["/python"],
            "aliases": ["py"],
            "permissions": ["python_example.command.python"],
        },
        "test": {
            "description": "This is a test command from python",
            "usages": [
                "/test",
                "/test [value: int]",
                "/test [value: float]",
            ],
            "permissions": ["python_example.command.test"],
        },
        "kickme": {
            "description": "Ask the server to kick you with a custom message",
            "usages": ["/kickme [reason: message]"],
            "permissions": ["python_example.command.kickme"],
        },
    }

    permissions = {
        "python_example.command": {
            "description": "Allow users to use all commands provided by this plugin.",
            "default": True,
            "children": {
                "python_example.command.python": True,
                "python_example.command.test": True,
                "python_example.command.kickme": True,
            },
        },
        "python_example.command.python": {
            "description": "Allow users to use the /python command.",
            "default": "op",
        },
        "python_example.command.test": {
            "description": "Allow users to use the /test command.",
            "default": True,
        },
        "python_example.command.kickme": {
            "description": "Allow users to use the /kickme command.",
            "default": True,
        },
    }

    def on_load(self) -> None:
        self.logger.info("on_load is called!")

    def on_enable(self) -> None:
        self.logger.info("on_enable is called!")
        self.get_command("python").executor = PythonCommandExecutor()

        self.register_events(self)  # register event listeners defined directly in Plugin class
        self._listener = ExampleListener(self)
        self.register_events(self._listener)  # you can also register event listeners in a separate class

        self.server.scheduler.run_task_timer(self, self.log_time, 0, 20 * 1)  # every second

    def on_disable(self) -> None:
        self.logger.info("on_disable is called!")

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        # You can also handle commands here instead of setting an executor in on_enable if you prefer
        match command.name:
            case "test":
                if len(args) > 0:
                    sender.send_message(f"Test with number: {args[0]}!")
                else:
                    sender.send_message("Test!!")
            case "kickme":
                player = sender.as_player()
                if player is None:
                    sender.send_error_message("You must be a player to execute this command.")
                    return False

                if len(args) > 0:
                    player.kick(args[0])
                else:
                    player.kick("You asked for it!")

        return True

    @event_handler
    def on_server_load(self, event: ServerLoadEvent):
        self.logger.info(f"{event.event_name} is passed to on_server_load")

    @event_handler(priority=EventPriority.HIGH)
    def on_server_load_2(self, event: ServerLoadEvent):
        self.logger.info(f"{event.event_name} is passed to on_server_load_2. This will be called after on_server_load.")

    def log_time(self):
        now = datetime.datetime.now().strftime("%c")
        for player in self.server.online_players:
            player.send_popup(now)
