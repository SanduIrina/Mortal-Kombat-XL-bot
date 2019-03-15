# Problem statement

See https://docs.google.com/document/d/1IWDF3L83Ozi81bvt2E3cWb77NnCV01m3ABiAlqw71Lc/edit?usp=sharing


# Sample codes

Video streaming sample code can be found in ./stream_example

Simple in-game commands implementation over sockets.io can be found in ./commands_example

The implementations are intentionally short and in different programming languages so you can port them into your preferred language.


# API

All the following methods are exposed as both sockets.io commands and REST (POST) requests.

All received data must be formatted as JSON.

Both REST and Sockets.io servers accept the same body format.

## In game commands

### Path

```
http://<IP>/command  (REST)

socketsio.emit('command', BODY)   (SOCKETS.IO)
```


### Body
```
{
  "key": // string, mandatory (your player key)
  "commands": {
      // dictionary, mandatory
      // must specify **only one** property
      // values are boolean (specify if a key becomes pressed or released)
      "up": // bool
      "down": // bool,
      "left": // bool,
      "right": // bool,
      "front_punch": // bool,
      "back_punch": // bool,
      "front_kick": // bool,
      "back_kick": // bool,
      "interact": // bool,
      "throw": // bool,
      "block": // bool,
    }
}
```

### Example
```
{
  "key": "123456789",
  "commands": {
    "up": true
  }
}
```
