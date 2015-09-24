# procutil
Lists processes and their related TCP connections (in native python). Must be root.

```
import procutil
>>> for c in procutil.connections() :
...    print c
... 
{'local': ('127.0.0.1', 631), 'proc': 'cupsd', 'remote': ('0.0.0.0', 0)}
{'local': ('127.0.1.1', 53), 'proc': 'dnsmasq', 'remote': ('0.0.0.0', 0)}
{'local': ('0.0.0.0', 22), 'proc': 'sshd', 'remote': ('0.0.0.0', 0)}
{'local': ('192.168.0.2', 34855), 'proc': 'firefox', 'remote': ('63.245.100.100', 443)}
```
