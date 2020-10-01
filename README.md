# Simple Http server

No need for additional explanation. :D

## Running
1 . You need to get a copy for yourself:

```commandline
git clone https://github.com/komnen0v1c/diy-http-server.git

cd diy-http-server
```

2 . Install a package:

``` commandline
pip3 install asyncio
```

3 . Then run:
```commandline
python3 server.py
```

4 . Once you start a script, open another terminal window and run:

```commandline
netcat -v -v localhost 8888
```

_. If you see an error, just run following code, and try again:

```commandline
pip3 install netcat
```

## Misc
Kudos to Kibb#4205 for starting this challenge on [TPH](https://theprogrammershangout.com/resources/projects/http-project-guide/intro.md)
