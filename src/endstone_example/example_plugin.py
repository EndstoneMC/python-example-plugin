from endstone.command import Command, CommandSender
from endstone.plugin import Plugin

from endstone_example.python_command import PythonCommandExecutor


class ExamplePlugin(Plugin):
    name = "PythonExamplePlugin"
    version = "0.3.0"
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
    }

    permissions = {
        "python_example.command": {
            "description": "Allow users to use all commands provided by this plugin.",
            "default": True,
            "children": {"python_example.command.python": True, "python_example.command.test": True},
        },
        "python_example.command.python": {
            "description": "Allow users to use the /python command.",
            "default": "op",
        },
        "python_example.command.test": {
            "description": "Allow users to use the /test command.",
            "default": True,
        },
    }

    def on_load(self) -> None:
        self.logger.info("on_load is called!")

    def on_enable(self) -> None:
        self.logger.info("on_enable is called!")
        self.get_command("python").executor = PythonCommandExecutor()

    def on_disable(self) -> None:
        self.logger.info("on_disable is called!")

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        # You can also handle commands here instead of setting an executor in on_enable if you prefer
        match command.name, args:
            case "test", []:
                # handle /test
                sender.send_message("Test!!")
            case "test", [n]:
                # handle /test n
                sender.send_message(f"Test with number: {n}!")
            case _, []:
                # handle /* (wildcard)
                sender.send_message(f"/{command.name} is executed from Python!")
            case _, *args:
                # handle /* args... (wildcard)
                sender.send_message(f"/{command.name} is executed from Python with arguments {args}!")

        return True
