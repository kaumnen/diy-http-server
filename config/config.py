from configparser import ConfigParser

# get the configparser object
config_object = ConfigParser()

# set config
config_object["SERVERCONFIG_BROWSER"] = {
    "host": "127.0.0.1",
    "port": "8888",
    "web_directory": "www/"
}

config_object["SERVERCONFIG"] = {
    "host": "127.0.0.1",
    "port": "8080",
}

# Write the above sections to config.ini file
with open('config.ini', 'w') as conf:
    config_object.write(conf)
