# AUTOTERM

Automaticaly write data to serial device if output matches with **key** in **key**=**value** data structure

```
Periodic Test TimeOut(min., 0 = disable) [5] : <<-- 10
AC_R [0A03]  : <<-- 0A03
AC_L [0903]  : <<-- 0903
BATR [0A02]  : <<-- 0A02
```

Keys matheth form beginnig.

## CLI arguments

    Usage: autoterm.py [options] <data> [<connection>]

###Options:

**SLEEP** *-s SLEEP, --sleep=SLEEP*
    
>(float) - wait time before start read from serial port

**FILE** *-f FILE, --file=FILE*

>(filename) - json file with settings. Default: same as python script

**Connection settings:**

**PORT** *-p PORT, --port=PORT*

>*port* is a device name: depending on operating system. e.g. `/dev/ttyUSB0` on GNU/Linux or `COM3` on Windows.
>
>enter **-**(dash) for port list

**BAUDRATE** *-b BAUDRATE, --baudrate=BAUDRATE*

>The parameter baudrate can be one of the standard values: 50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600, 19200, 38400, 57600, 115200. These are well supported on all platforms.
>
>The parameter baudrate can be one of the standard values: 50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600, 19200, 38400, 57600, 115200. These are well supported on all platforms.
    
### JSON File Format

####settings

Contains serial connection settings. **default** is default settings.

####data

Contains **key**=**value** pairs. **default** is default settings.

If serial devise send strintg that matches with **key** (from beginning), **value** will be sended back to device automaticaly. 
Use empty "" value for just carriage return.   

**Example:**
```json
{
  "settings": {
    "default": {
      "port": "COM1",
      "baudrate": 9600,
      "sleep": 0.5
    }
  },
  "data": {
    "eth": {
      "DHCP": "Y",
      "ETH Protocol": "Y",
      "Local port": "",
      "ID": "123"
    },
     "gsm": {
      "DHCP": "Y",
      "ETH Protocol": "Y",
      "Local port": "",
      "ID": "321"
    }
  }
}
```
