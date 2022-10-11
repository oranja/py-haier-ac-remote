from construct import ConstructError
from haierlib.parsers import parse_response, parse_state
from haierlib.types import FanSpeed, Limits, Mode, Response, State
from pytest import raises


class TestParsers:
    response_payload = (
        b"\x00\x00\x27\x15\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x30\x30\x30\x37"
        b"\x41\x38\x31\x37\x45\x39\x41\x43"
        b"\x00\x00\x00\x00\x00\x01\x00\x00"
        b"\x00\x25\xff\xff\x22\x00\x00\x00"
        b"\x00\x00\x01\x06\x6d\x01\x00\x15"
        b"\x00\x00\x00\x7f\x00\x00\x00\x00"
        b"\x00\x02\x00\x02\x00\x00\x00\x09"
        b"\x00\x01\x00\x00\x00\x0c\x45"
    )
    state_payload = (
        b"\xff\xff\x22\x00"
        b"\x00\x00\x00\x00\x01\x06\x6d\x01"
        b"\x00\x15\x00\x00\x00\x7f\x00\x00"
        b"\x00\x00\x00\x02\x00\x02\x00\x00"
        b"\x00\x09\x00\x01\x00\x00\x00\x0c"
    )

    async def test_parse_response(self) -> None:
        response: Response = parse_response(self.response_payload)
        assert response is not None
        assert response.mac_address == b"\x00\x07\xa8\x17\xe9\xac"
        assert response.sequence_number == 1
        assert response.state is not None

    async def test_parse_response_corrupt_payload_raises(self) -> None:
        bad_payload = self.response_payload[2:]
        with raises(ConstructError):
            parse_response(bad_payload)

    async def test_parse_response_state(self) -> None:
        response: Response = parse_response(self.response_payload)
        state: State = response.state
        self._verify_state(state)

    async def test_parse_state(self) -> None:
        state: State = parse_state(self.state_payload)
        self._verify_state(state)

    async def test_parse_state_corrupt_payload_raises(self) -> None:
        bad_payload = self.state_payload[2:]
        with raises(ConstructError):
            parse_state(bad_payload)

    def _verify_state(self, state: State) -> None:
        assert state.current_temperature == 21
        assert state.target_temperature == 28
        assert int(state.fan_speed) == FanSpeed.MIN.value
        assert int(state.limits) == Limits.OFF.value
        assert int(state.mode) == Mode.HEAT.value
        assert state.health == True
        assert state.power == True
