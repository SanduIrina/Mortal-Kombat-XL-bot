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

During the final championship, any manual request is prohibited once champion selection phase ends.

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

### Notes

When using this as REST request, the server also returns the current state of your keypresses.

If you need increased performance/better timing of your actions, implement it using sockets.io instead of REST.


## Player select

During the champion selection phase, use this to select who you're playing with.

### Path

```
http://<IP>/player_select  (REST)

socketsio.emit('player_select', BODY)   (SOCKETS.IO)
```

### Body
```
{
  "key": // string, mandatory (your player key)
  "champion": // string, mandatory, one of ['scorpio', 'subzero']
}
```

### Example

```
{
  "key": "123456789",
  "champion": "scorpio"
}
```

### Notes

You can only play with the default champion style.

During the final championship, you can send this request manually using tools like Postman.
## Stream config

Use this to specify where the stream servers should send frames to.



Frames can be sent at a maximum of 800x600 resolution.

Use "downscale_ratio" to request lower resolution frames.

i.e. setting "downscale_ratio" to 0.5 means you'll receive 400x300 frames from now on.

### Path

```
http://<IP>/stream_config  (REST)

socketsio.emit('stream_config', BODY)   (SOCKETS.IO)
```

### Body

```
{
  "key": // string, mandatory (your player key)
  "ip": // string, mandatory (your machine's ip)
  "port": // natural number, mandatory (your listening port)
  "downscale_ratio": // float between (0, 1];
}
```

### Example

```
{
  "key": "123123123",
  "ip": "169.254.11.79",
  "port": 5005,
  "downscale_ratio": 0.4
}
```
### Notes

Lower resolution = more, faster frames

Higher resolution = fewer, slower frames

Your downscale factor will not impact the other player's streaming performance in any way.

During the final championship, you can send this request manually using tools like Postman, until the champion select phase ends.

## Admin commands

Use these to manipulate the game state.

These requests are only available during the development stage. Access to them will be denied in the final championship.

### Path

```
http://<IP>/admin  (REST)

socketsio.emit('admin', BODY)   (SOCKETS.IO)
```

### Menu commands

Grants access to "escape", "enter" and "arrow keys" for manipulating the game menu
#### Body

```
{
  key: // string, mandatory (your ADMIN key)
  type: // string, must be 'menu_command'
  menu_key: // string, mandatory;
    // one of  ['up', 'down', 'left', 'right', 'enter', 'escape']
  is_player_2: // boolean, mandatory;
    // specify is given menu command is interpreted from player1 or player2
}
```


#### Example
```
{
  "key": "puterea_prieteniei",
  "type": "menu_command",
  "menu_key": "enter",
  "is_player_2": false
}
```

### Menu shortcuts

Some menu flows require a lot of input and can be boring to insert everytime you want to start a new game.

Valid types for shortcuts are:

- "new_2p_game" : from main menu, starts a new 2p game and the player selection phase (no need to call start_player_select after)

- "in_game_to_reset_game": while in-game (players fighting eachother), restart the game immediately

- "in_game_to_player_select": while in-game (players fighting eachother), go back to the player selection screen

- "in_game_to_main_menu": while in-game (players fighting eachother), go back to main-menu

- "start_player_select": let the server know that we are in the player selection phase and allow players to choose their champions. Must sometimes be called if the game is not started using the 'new_2p_game' command


The following types allow setting the "hide_post_game_details" flag.

Sometimes there can be an annoying post game results screen.

Specify {hide_post_game_details: true} to remove it when it happens.
(Don't set it to true otherwise, it will show the results screen instead)

- "reset_game_after_endscreen" : after a fighting game finished, restart with same players

- "new_game_after_endscreen": after a fighting game finished, start a new game with new players

- "main_menu_after_endscreen": after a fighting game finished, go back to main menu
#### Body

```
{
  key: // string, mandatory (your ADMIN key)
  type: // string, mandatory, must be one of the above
  hide_post_game_details: // boolean, NOT MANDATORY
}
```

#### Example

```
{
  "key": "puterea_prieteniei",
  "type": "reset_game_after_endscreen",
  "hide_post_game_details": true
}
```

### Change playing teams

#### Body

```
{
  key: // string, mandatory (your ADMIN key)
  type: // string, mandatory, must be "change_teams"
  team1: // string, mandatory, the name of the first playing team
  team2: // string, mandatory, the name of the second playing team
}
```

#### Example

```
{
  "key": "puterea_prieteniei",
  "type": "change_teams",
  "team1": "T25",
  "team2": "T25_P2"
}
```

## Status request

Only useful to let you know if you've been assigned player1 or player2
### Path
Only exposed as a REST method because it doesn't change anything in the server state and just returns info.

```
http://<IP>/get_status  (REST)
```

### Body
```
{
  key: // string, mandatory (your ADMIN key)
}
```
### Example
```
{
  "key": "123456789"
}
```
