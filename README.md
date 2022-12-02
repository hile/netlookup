![Unit Tests](https://github.com/hile/netlookup/actions/workflows/unittest.yml/badge.svg)
![Style Checks](https://github.com/hile/netlookup/actions/workflows/lint.yml/badge.svg)

# Command line network lookups and operations

This python tool implements pretty much same things as `netcalc` and `netblocks` libraries, but
with minor differences in the way things are done.

The library is intended to be usable both as a command line tool `netlookup` and as a library from
server code. Personally I use it for splitting IP ranges to subnets.

## Installing

```bash
pip install netlookup
```

# Command line tool `netlookup` basic usage

Following examples illustrate Usage of netlookup tool.

Lookup details for IPv4 host with CIDR mask and IPv6 subnet:

```bash
netlookup info 172.31.1.19/17 2c0f:fb50:4000::/56
             CIDR 172.31.0.0/17
          Netmask 255.255.128.0
          Network 172.31.0.0
        Broadcast 172.31.127.255
       First host 172.31.0.1
        Last host 172.31.127.254
      Total hosts 32766
             Next 172.31.128.0/17
         Previous 172.30.128.0/17
             Bits 10101100.00011111.00000000.00000000
      Reverse DNS 0.0.31.172.in-addr.arpa.
             CIDR 2c0f:fb50:4000::/56
          Netmask ffff:ffff:ffff:ff00::
          Network 2c0f:fb50:4000::
        Broadcast 2c0f:fb50:4000:ff:ffff:ffff:ffff:ffff
       First host 2c0f:fb50:4000::1
        Last host 2c0f:fb50:4000:ff:ffff:ffff:ffff:fffe
      Total hosts 4722366482869645213694
             Next 2c0f:fb50:4000:100::/56
         Previous 2c0f:fb50:3fff:ff00::/56
             Bits 0010110000001111:1111101101010000:0100000000000000:0000000000000000:0000000000000000:0000000000000000:0000000000000000:0000000000000000
      Reverse DNS 0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.4.0.5.b.f.f.0.c.2.ip6.arpa.
```

Split subnet with defaults (to next smaller subnet / larger prefix):

```bash
netlookup split 172.31.1.19/17 2c0f:fb50:4000::/56
    172.31.0.0/18
    172.31.64.0/18
    2c0f:fb50:4000::/57
    2c0f:fb50:4000:80::/57
```

Split IPv4 subnets with specific prefix:

```bash
netlookup split --mask 19 172.31.1.19/17 172.31.5.39/17
    172.31.0.0/19
    172.31.32.0/19
    172.31.64.0/19
    172.31.96.0/19
    172.31.0.0/19
    172.31.32.0/19
    172.31.64.0/19
    172.31.96.0/19
```

Using the python library
------------------------

Some practical examples for using the API where a CLI command is not yet available.

Create set of networks and show minimal merged CIDR prefixes to cover this range:

```python
from netlookup.network_sets.base import NetworkSet
ns = NetworkSet()
ns.add_network('172.31.0.0/23')
ns.add_network('172.31.4.0/22')
ns.add_network('172.31.8.0/24')
ns.add_network('172.31.9.0/25')
ns.add_network('172.31.9.128/25')
print('\n'.join(str(x.cidr) for x in ns.merged))
```

Previous example returns

```bash
172.31.0.0/23
172.31.4.0/22
172.31.8.0/23
```

Using same example, remove one /29 from the result set

```python
from netlookup.network_sets.base import NetworkSet
ns = NetworkSet()
ns.add_network('172.31.0.0/23')
ns.add_network('172.31.4.0/22')
ns.add_network('172.31.8.0/24')
ns.add_network('172.31.9.0/25')
ns.add_network('172.31.9.128/25')
print('\n'.join(str(x.cidr) for x in ns.substract('172.31.8.64/29')))
```

This example returns

```bash
172.31.0.0/23
172.31.4.0/22
172.31.8.0/26
172.31.8.72/29
172.31.8.80/28
172.31.8.96/27
172.31.8.128/25
172.31.9.0/24
````

# Cloud vendor prefixes

This tool contains lookup caches for some cloud vendors. Currently supported vendors are:

- AWS
- Cloudflare
- Google Cloud
- Google Services

Note: Azure support was removed because their data is in a silly URL and I just don't
care about them.

Example to load data for cloud vendor IP prefix lookups and save it to user specific cache
directory `~/.config/netlookup`.

Following command requires internet connection to update the prefix lists.

```python
from netlookup.prefixes import Prefixes
ns = Prefixes()
print(ns.cache_directory)
ns.update()
ns.save()
````

## Get prefixes for cloud vendors

Use the previously loaded cached cloud vendor IP prefix lookup and find some addresses.

```python
>>> ns.find('3.81.2.1')
aws us-east-1 3.80.0.0/12
````

Similarly, you can get specific vendor network set and lookup address from there:

```python
>>> ns.get_vendor('google').find('216.58.210.142')
google 216.58.192.0/19
```
