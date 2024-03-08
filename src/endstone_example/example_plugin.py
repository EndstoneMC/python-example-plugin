from endstone.command import Command, CommandSender
from endstone.plugin import Plugin

from endstone_example.python_command import PythonCommandExecutor


class ExamplePlugin(Plugin):
    def on_load(self) -> None:
        self.logger.info("on_load is called!")

    def on_enable(self) -> None:
        self.logger.info("on_enable is called!")

        self.register_command(
            name="python", description="Zen of python", usages=["/python"], aliases=["py"]
        ).executor = PythonCommandExecutor()

        self.register_command(
            name="test", description="This is a test command from python", usages=["/test", "/test [value: int]"]
        )

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
