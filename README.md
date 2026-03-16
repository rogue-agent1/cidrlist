# cidrlist
CIDR range utility: expand, check membership, info, merge, split.

## Usage
```bash
python cidrlist.py info 10.0.0.0/24
python cidrlist.py expand 192.168.1.0/28
python cidrlist.py contains 10.0.0.0/8 10.1.2.3
python cidrlist.py merge 10.0.0.0/25 10.0.0.128/25
python cidrlist.py split 10.0.0.0/24 26
```
## Zero dependencies. Python 3.6+.
