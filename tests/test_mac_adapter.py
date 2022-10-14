from heapq import _heapify_max

from haierlib.types import HexStringMacAddressAdapter


class TestMacAdapter:
    async def test_decode_encode(self) -> None:
        mac_bytes = b"\x00\x07\xa8\x17\xe9\xac"
        assert len(mac_bytes) == 6
        
        mac_field = HexStringMacAddressAdapter()

        encoded = mac_field.build(mac_bytes)
        assert len(encoded) == 12

        decoded = mac_field.parse(encoded)
        assert decoded == mac_bytes
