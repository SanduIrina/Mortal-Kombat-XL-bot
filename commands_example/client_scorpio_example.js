const Logger = require('tracer').console();
// const socket = require('socket.io-client')('http://172.24.1.100');

if (process.argv.length != 4) {
  Logger.log('Usage:\nnode client_scorpio_example.js <IP> <YOUR_PLAYER_KEY>')
  process.exit()
}

const IP = process.argv[2]
const KEY = process.argv[3]
Logger.log(IP)

// the server ip
const socket = require('socket.io-client')(`http://${IP}`);

function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

class Player {
  constructor(key) {
    this.secretKey = key;
    this.addKey = this.addKey.bind(this);
    this.playScorpio = this.playScorpio.bind(this);
    this.sendCmd = this.sendCmd.bind(this);
  }

  addKey(body) {
    return {
      key: this.secretKey,
      ...body,
    };
  }


  async sendCmd(cmd, timeout = 100) {
    try {
      // prepateTimeDiff();
      socket.emit('command', this.addKey({
        commands: cmd,
      }));
      // printTimeDiff('socket emit');
      Logger.log('Sending ', cmd);
      await sleep(timeout);
    } catch (e) {
      Logger.error(e);
    }
  }

  async playScorpio() {
    const { sendPlayerSelect, sendPlayerConfirm, sendCmd } = this;
    setInterval(async () => {
      try {
        Logger.log('new command series');
        // sprint to right
        await sendCmd({ right: true });
        await sendCmd({ right: false });
        await sendCmd({ right: true });
        await sendCmd({ right: false });

        // stand down + leg kick
        await sendCmd({ down: true }, 250);
        await sendCmd({ front_kick: true }, 250);
        await sendCmd({ front_kick: false });
        await sendCmd({ down: false });
        await sleep(100);

        // sword combo
        await sendCmd({ back_punch: true });
        await sendCmd({ back_punch: false });
        await sendCmd({ front_punch: true });
        await sendCmd({ front_punch: false });
        await sendCmd({ back_punch: true });
        await sendCmd({ back_punch: false });
        await sleep(500); // ending animation time for combo


        // teleport combo
        await sendCmd({ down: true }, 20);
        await sendCmd({ down: false }, 20);
        await sendCmd({ left: true }, 20);
        await sendCmd({ left: false }, 20);
        await sendCmd({ front_kick: true }, 20);
        await sendCmd({ front_kick: false });

        // teleport combo reversed
        await sendCmd({ down: true }, 20);
        await sendCmd({ down: false }, 20);
        await sendCmd({ right: true }, 20);
        await sendCmd({ right: false }, 20);
        await sendCmd({ front_kick: true }, 20);
        await sendCmd({ front_kick: false });
      } catch (e) {
        Logger.error('Error trying to send commands: ', e);
      }
    }, 3000);
  }
}

// your client key
const p1 = new Player(KEY);// new Player('123123123');
p1.playScorpio(); // dont wait for this
module.exports = {
  Player,
};
