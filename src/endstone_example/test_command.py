from endstone.command import Command


class TestCommand(Command):
    def __init__(self):
        Command.__init__(self, "test")
        self.description = "This is a test command from python"
        self.usages = ["/test", "/test [value: int]"]
