#!/usr/bin/env python3

from typing import List
import uuid
import hashlib
import sys

class AddressGenerator:
    # LAA (locally administered addresses in the IEEE Mac Address spec) have
    # the second-least-significant bit of the first octet set to 1. This is
    # the range we use when generating so our default prefix conforms to this.
    _mac_prefix = [6, 0]

    def __init__(self, id_seed: str):
        '''Idea is to set the mac address to something unique by tying it to a
        seed value (id_seed). Good seed values are a hostname (if unique in the
        env), a concatenation of the hostname and environment, or something
        similarly unique among a set of machines.'''

        self._digest = hashlib.sha256(id_seed.encode("utf-8"), usedforsecurity=False)

    @property
    def mac_address(self) -> str:
        sb = ""
        for o in self._mac_prefix + [d for d in self._digest.digest()[:4]]:
            if sb != "":
                sb += ":"
            sb += "{:02x}".format(o).upper()

        return sb

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise RuntimeError(f"Invocation: {sys.argv[0]} id_seed")

    gen = AddressGenerator(sys.argv[1])
    print(f"{sys.argv[1]} {gen.mac_address}")
    sys.exit(0)

# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4
