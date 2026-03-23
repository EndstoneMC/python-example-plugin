# Endstone Plugin Development Guide

This file helps AI coding agents understand how to build Endstone plugins in Python.

Endstone is a plugin framework for Minecraft Bedrock Dedicated Server (BDS). Plugins are
Python packages installed into the server's `plugins/` folder as `.whl` files.

Docs: https://endstone.dev/latest/
Example plugin: see `src/endstone_example/` in this repo.

## Project Setup

Package name convention: `endstone-<name>` (PyPI) / `endstone_<name>` (Python package).

Minimal `pyproject.toml`:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "endstone-my-plugin"
version = "0.1.0"
description = "My Endstone plugin"

[project.entry-points."endstone"]
my-plugin = "endstone_my_plugin:MyPlugin"
```

The entry point under `[project.entry-points."endstone"]` tells Endstone which class to load.

## Plugin Class

Every plugin extends `endstone.plugin.Plugin` and declares `api_version`:

```python
from endstone.plugin import Plugin

class MyPlugin(Plugin):
    api_version = "0.11"

    def on_enable(self) -> None:
        self.logger.info("Plugin enabled!")

    def on_disable(self) -> None:
        self.logger.info("Plugin disabled!")
```

Lifecycle methods (all optional):
- `on_load()` -- called when the plugin is loaded (before enable, rarely needed)
- `on_enable()` -- called when the plugin is enabled (register events, load config here)
- `on_disable()` -- called when the plugin is disabled (cleanup here)

Key properties available on `self`:
- `self.logger` -- plugin logger
- `self.server` -- the Server instance
- `self.config` -- plugin config (dict-like, loaded from config.toml)
- `self.data_folder` -- path to plugin's data directory

## Commands

Define commands and permissions as class-level dicts:

```python
from endstone import Player
from endstone.command import Command, CommandSender, ConsoleCommandSender
from endstone.plugin import Plugin

class MyPlugin(Plugin):
    api_version = "0.11"

    commands = {
        "greet": {
            "description": "Send a greeting",
            "usages": ["/greet [player: target]"],
            "aliases": ["hi"],
            "permissions": ["my_plugin.command.greet"],
        },
    }

    permissions = {
        "my_plugin.command.greet": {
            "description": "Allow users to use the /greet command.",
            "default": True,  # True = everyone, "op" = operators only, False = no one
        },
    }

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        match command.name:
            case "greet":
                if isinstance(sender, Player):
                    sender.send_message(f"Hello, {sender.name}!")
                elif isinstance(sender, ConsoleCommandSender):
                    self.logger.info("Hello from the console!")
        return True
```

### Command Parameter Types

Parameters in `usages` use the syntax `<name: type>` (mandatory) or `[name: type]` (optional).

Built-in types: `int`, `float`, `bool`, `str`, `message`, `json`, `target`, `block_pos`, `pos`,
`block`, `block_states`, `entity_type`.

User-defined enums: `(value1|value2|value3)` -- e.g. `/home (add|list|del)<action: HomeAction>`.

### Permission Defaults

- `True` or `"true"` -- everyone can use
- `False` or `"false"` -- no one can use (must be granted)
- `"op"` -- operators only (default if not specified)
- `"not_op"` -- non-operators only
- `"console"` -- console only

## Events

Use the `@event_handler` decorator. Register listeners with `self.register_events()`:

```python
from endstone import ColorFormat
from endstone.event import PlayerJoinEvent, PlayerQuitEvent, event_handler
from endstone.plugin import Plugin

class MyListener:
    def __init__(self, plugin: Plugin) -> None:
        self._plugin = plugin

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent) -> None:
        event.join_message = f"{ColorFormat.YELLOW}{event.player.name} joined"

    @event_handler
    def on_player_quit(self, event: PlayerQuitEvent) -> None:
        event.quit_message = f"{ColorFormat.YELLOW}{event.player.name} left"
```

Register in `on_enable`:

```python
def on_enable(self) -> None:
    self.register_events(MyListener(self))
    # You can also register the plugin itself if it has @event_handler methods:
    self.register_events(self)
```

Event handlers can also be defined directly on the Plugin class.

### Event Priorities

```python
from endstone.event import EventPriority, event_handler

@event_handler(priority=EventPriority.HIGH, ignore_cancelled=True)
def on_player_join(self, event: PlayerJoinEvent) -> None:
    ...
```

Priorities (lowest runs first): `LOWEST`, `LOW`, `NORMAL` (default), `HIGH`, `HIGHEST`, `MONITOR`.

### Common Events

Player: `PlayerJoinEvent`, `PlayerQuitEvent`, `PlayerChatEvent`, `PlayerCommandEvent`,
`PlayerInteractEvent`, `PlayerDeathEvent`, `PlayerMoveEvent`, `PlayerTeleportEvent`,
`PlayerLoginEvent`, `PlayerKickEvent`, `PlayerGameModeChangeEvent`.

Block: `BlockBreakEvent`, `BlockPlaceEvent`, `BlockExplodeEvent`.

Actor: `ActorSpawnEvent`, `ActorDeathEvent`, `ActorDamageEvent`.

Server: `ServerLoadEvent`, `ServerListPingEvent`, `ServerCommandEvent`.

Packet: `PacketReceiveEvent`, `PacketSendEvent` (for low-level protocol access).

## Configuration

Place a `config.toml` next to your plugin module. Call `self.save_default_config()` in
`on_enable` to copy it to the plugin's data folder on first run:

```toml
# config.toml
greeting = "Hello"
max_homes = 3
```

```python
def on_enable(self) -> None:
    self.save_default_config()
    greeting = self.config["greeting"]
    max_homes = self.config["max_homes"]
```

## Scheduler

Schedule delayed or repeating tasks (1 second = 20 ticks):

```python
def on_enable(self) -> None:
    # Run once after 5 seconds
    self.server.scheduler.run_task(self, self.my_task, delay=100)

    # Run every 10 seconds
    self.server.scheduler.run_task(self, self.my_repeating_task, delay=0, period=200)
```

## Color Formatting

```python
from endstone import ColorFormat

msg = f"{ColorFormat.GREEN}Success! {ColorFormat.RESET}Back to normal."
```

Common codes: `BLACK`, `DARK_BLUE`, `DARK_GREEN`, `DARK_AQUA`, `DARK_RED`, `DARK_PURPLE`,
`GOLD`, `GRAY`, `DARK_GRAY`, `BLUE`, `GREEN`, `AQUA`, `RED`, `LIGHT_PURPLE`, `YELLOW`,
`WHITE`, `BOLD`, `ITALIC`, `OBFUSCATED`, `RESET`.

Always end colored text with `ColorFormat.RESET`.

## Common Imports

```python
# Plugin base
from endstone.plugin import Plugin

# Commands
from endstone.command import Command, CommandSender, CommandExecutor, ConsoleCommandSender

# Events
from endstone.event import event_handler, EventPriority
from endstone.event import PlayerJoinEvent, PlayerQuitEvent, PlayerChatEvent
from endstone.event import BlockBreakEvent, BlockPlaceEvent
from endstone.event import ActorDamageEvent, ActorDeathEvent

# Entities and formatting
from endstone import Player, ColorFormat, GameMode

# Forms (GUI)
from endstone.form import ActionForm, ModalForm, MessageForm
```

## Player Methods

```python
player.send_message("text")          # Chat message
player.send_popup("text")            # Popup on screen
player.send_tip("text")              # Tip at top
player.send_title("title", "sub")    # Title screen
player.send_toast("title", "body")   # Toast notification
player.kick("reason")                # Kick from server
player.perform_command("say hi")     # Execute command as player
player.teleport(location)            # Teleport
```

## Building and Installing

```bash
uv build                    # Build .whl
uv sync --extra dev         # Install dev dependencies
uv run ruff check src/      # Lint
```

Copy the `.whl` from `dist/` to your server's `plugins/` folder.

For development, use editable installs: `pip install -e .` (with the server's venv activated),
then `/reload` in-game to pick up changes.