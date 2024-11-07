# address-generator

In infrastructure projects I often want to network addresses deterministically
from hostnames or other identifiers in an environment. The scripts in this
repository generate MAC addresses and ipv6 LLAs from useful input.

Usage example:

# Generating conforming locally-administered addresses (LLAs) in IEEE Mac Address Spec

```
./mac_generator.py ns1.zebo.codeplox.dev
ns1.zebo.codeplox.dev 06:00:8F:7D:A3:6D
```

# Generating conforming IPv6 unique local addresses (ULAs)

```
./v6_lla_generator.py 06:00:8F:7D:A3:6D 52 2
fe80::400:8fbf:967d:a36d/64
```
