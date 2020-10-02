# Simple Http server
No additional info required. :D


## Prerequisites
First you need to get a copy for yourself:

```commandline
git clone https://github.com/komnen0v1c/diy-http-server.git
```
Then change directory:
```commandline
cd diy-http-server
```
Install packages:

``` commandline
pip3 install asyncio
pip3 install netcat
```

## Running terminal socket

1 . Run:
```commandline
python3 server.py
```

2 . Once you start a script, open another terminal window and run:

```commandline
netcat -v -v localhost 8080
```

## Making browser requests

1 . Run:
```commandline
python3 server_browser.py
```

2 . Once you start a script, open browser and search for:

```commandline
127.0.0.1:8888/test.txt
```

## Misc
Kudos to Kibb#4205 for starting this challenge on [TPH](https://theprogrammershangout.com/resources/projects/http-project-guide/intro.md)
