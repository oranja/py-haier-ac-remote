from construct import (
    Bytes,
    Checksum,
    Const,
    Container,
    Enum,
    Int8ub,
    Int16ub,
    Int32ub,
    Padding,
    RawCopy,
    Struct,
    this,
)

from .types import FanSpeed, HexStringMacAddressAdapter, Limits, Mode, Response, State

state_struct = Struct(
    Const(0xFFFF, Int16ub) * "start",
    Const(0x2200, Int16ub) * "state (magic)",
    Padding(8),
    "current_temperature" / Int16ub,
    Padding(8),
    "mode" / Enum(Int16ub, Mode),
    "fan_speed" / Enum(Int16ub, FanSpeed),
    "limits" / Enum(Int16ub, Limits),
    "power" / Int16ub,
    "health" / Int16ub,
    Padding(2),
    "target_temperature" / Int16ub,  # From 16!
)

response_struct = Struct(
    Padding(2),
    Const(0x27, Int8ub) * "magic",
    Const(0x15, Int8ub) * "type: response",
    Padding(4),
    Padding(4),
    # MAC address nibbles encoded into a string
    "mac_address" / HexStringMacAddressAdapter(),
    Padding(2),
    "seq" / Int32ub,
    "payload_length" / Int32ub,
    # Dynamic payload array
    "payload"
    / RawCopy(
        Struct(
            Const(0xFFFF, Int16ub) * "payload magic",
            "type" / Int8ub,
            "data" / Bytes(this._.payload_length - 4),
        )
    ),
    "checksum" / Checksum(Int8ub, lambda data: sum(data[2:]) & 0xFF, this.payload.data),
)

# TODO check execute() on parsers.ts for verifications

# Expects the payload from response
def parse_state(raw_payload: bytes) -> State:
    # Get the constructed data
    state: Container = state_struct.parse(raw_payload)

    # Adjust and convert to State object
    return State(
        current_temperature=state.current_temperature,
        target_temperature=state.target_temperature + 16,
        fan_speed=state.fan_speed,
        mode=state.mode,
        health=bool(state.health),
        limits=state.limits,
        power=bool(state.power),
    )


def parse_response(raw_response: bytes) -> Response:
    response: Container = response_struct.parse(raw_response)
    state: State = parse_state(response.payload.data)
    return Response(
        mac_address=response.mac_address, sequence_number=response.seq, state=state
    )


def hex_str_to_bytes(hex_str: str) -> bytes:
    return bytes.fromhex(hex_str)
