from dataclasses import dataclass
from enum import Enum


class Limits(Enum):
    OFF = 0
    ONLY_VERTICAL = 1


class FanSpeed(Enum):
    MAX = 0
    MID = 1
    MIN = 2
    AUTO = 3


class Mode(Enum):
    SMART = 0
    COOL = 1
    HEAT = 2
    FAN = 3
    DRY = 4


@dataclass
class State:
    # Temperatures in Celsius
    current_temperature: int = 21
    target_temperature: int = 21
    fan_speed: FanSpeed = FanSpeed.MIN
    mode: Mode = Mode.FAN
    health: bool = False
    limits: Limits = Limits.OFF
    power: bool = False

    def __str__(self) -> str:
        return f"""Haier AC State:
        Power: {self.power},
        Current Temp: {self.current_temp}
        Target Temp: {self.target_temp}
        Fan Speed: {self.fan_speed}
        Mode: {self.mode}
        Health: {self.health}
        Limits: {self.limits}"""

    def update(
        self,
        current_temp: int,
        target_temp: int,
        fan_speed: FanSpeed,
        mode: Mode,
        health: bool,
        limits: Limits,
        power: bool,
    ):
        self.current_temperature = current_temp
        self.target_temperature = target_temp
        self.fan_speed = fan_speed
        self.mode = mode
        self.health = health
        self.limits = limits
        self.power = power


@dataclass
class Response:
    mac_address: bytes
    sequence_number: int
    state: State
