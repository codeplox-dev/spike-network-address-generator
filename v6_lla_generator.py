#!/usr/bin/env python3

"""."""

import sys
import math
import ipaddress
from typing import Iterable, List

# seems like fe80::/10 is defined (so fe80...febf are all valid prefixes) but
# systems use a 64-bit length so we stick with fe80::/64 and this code is much
# simpler b/c of it
_canned_net_prefix = 0xfe80
_canned_net_prefix_size = 64

def _pad_my_val(v: int, pad_to: int) -> int:
    hv = hex(v)
    prefix_bit_length = (len(hv)-2) * 4
    return int(hv, base=16) << pad_to - prefix_bit_length

def _v6_network_address() -> int:
    return _pad_my_val(_canned_net_prefix, 128)

def _v6_subnet_address() -> int:
    return _pad_my_val(0, 128-48) # 128bit is full ipv6 length, 48 is length of network part, so we start after that

def _v6_device_address(mac_r: str, vlan_id: int, netns: int) -> int:
    # create a v6 ULA using the eui 64 standard
    spl = mac_r.split(":")
    assert len(spl) == 6

    custo = 0xfffe ^ ((vlan_id<<1)|(netns<<13))
    spl.insert(3, f"{((custo & 0xff00) >> 8):x}")
    spl.insert(4, f"{(custo & 0x00ff):x}")

    # invert seventh bit in first 16 bits if interface ID
    spl[0] = f"{(int(spl[0], base=16) ^ 0x02):x}"

    v = 0
    for s in spl:
        v = v << 8
        v += int(s, base=16)

    return int(v)


def main(args: Iterable[str]) -> int:
    if len(args) != 4:
        raise RuntimeError(f"Invocation: {args[0]} mac vlanid netns")

    mac = args[1]
    vlan_id = int(args[2])
    netns = int(args[3])

    v6_network_address = _v6_network_address()
    v6_subnet_address = _v6_subnet_address()
    v6_device_address = _v6_device_address(mac, vlan_id, netns)

    v6_address = ipaddress.IPv6Address(v6_network_address + v6_subnet_address + v6_device_address)
    print(f"{v6_address}/{_canned_net_prefix_size}")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))

# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4
