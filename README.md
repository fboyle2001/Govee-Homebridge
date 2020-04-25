# Packet Descriptions
Firstly, I would like to note that finding these packets would not have been possible without this [original repository containing the colour packet by egold555](https://github.com/egold555/Govee-H6113-Reverse-Engineering) and this [repository containing some Python code with `gatttool` and Govee Light packets by ddxtanx](https://github.com/ddxtanx/GoveeAPI). To find these packets I used a few methods:
- [A Bluetooth Low Energy sniffer by Adafruit](https://learn.adafruit.com/reverse-engineering-a-bluetooth-low-energy-light-bulb/sniff-protocol). It ultimately wasn't successful for me because it seemed to only pick up the advertisement packets rather than any ATT protocol packets that were being sent once a connection was established.
- The method that worked was using an [Android device to capture Bluetooth communications](https://medium.com/@urish/reverse-engineering-a-bluetooth-lightbulb-56580fcb7546) and then analysing the results in WireShark.
## Connecting and Sending
Govee lights can be accessed over the Bluetooth Low Energy protocol. It is easiest to do this with `gatttool` and `hcitool` on Linux (I used a Raspberry Pi Zero for this). To find the device address to send the packets to use `sudo hcitool lescan`. Then use `gatttool` like so:
```
gatttool -I
connect <device address>
char-write-cmd 0x0015 <packet>
disconnect
```
All the packets listed here are sent to the `0x0015` handle. Each packet is exactly 20 bytes long. The generic form of each packet is:

|Part      |Location |Size    |Description                                                           |
|----------|---------|--------|----------------------------------------------------------------------|
|Identifier|Byte 0   |1 Byte  |Seems to be used to differentiate between responses and requests.     |
|Data      |Byte 1-18|18 Bytes|Contains the data corresponding to each action such as colour.        |
|Checksum  |Byte 19  |1 Byte  |An XOR of all 19 previous bytes. Must be correct or packet is refused.|

In the descriptions below `...` represents `0x00` bytes filling the remaining the bytes that are available. I haven't tested if these have to be `0x00` but it is probably best to use `0x00`.

## Power
### On
Format: `0x33 0x01 0x01 0x00 ... 0x00 0x33`

Example Command `char-write-cmd 0x0015 3301010000000000000000000000000000000033`

### Off
Format: `0x33 0x01 0x00 0x00 ... 0x00 0x32`

Example Command: `char-write-cmd 0x0015 3301000000000000000000000000000000000032`

## Colour, Brightness and Modes
The lights seem to have 4 modes:
- [X] RGB Colour
- [X] Temperature Colour
- [X] Music Mode
- [ ] Scenes 

### RGB Colour

Format: `0x33 0x05 0x02 RED GREEN BLUE 0x00 ... 0x00 XOR`

Example Command (makes light red): `char-write-cmd 0x0015 330502ff000000000000000000000000000000cb`

### Temperature Colour

Format: `0x33 0x05 0x02 0xFF 0xFF 0xFF 0x01 RED GREEN BLUE 0x00 ... 0x00 XOR`

Example Command (~2000K): `char-write-cmd 0x0015 330502ffffff01ff880d000000000000000000b0`

It is probably best to use an algorithm such as [this one by Tanner Helland](https://tannerhelland.com/2012/09/18/convert-temperature-rgb-algorithm-code.html) to calculate the corresponding RGB values.

### Brightness

Format: `0x33 0x04 BRIGHTNESS 0x00 ... 0x00 XOR`

Example Command (maximum brightness): `char-write-cmd 0x0015 3304ff00000000000000000000000000000000c8`

### Music Mode

Format: `0x33 0x05 0x03 0x01 SENSITIVITY RED GREEN BLUE 0x00 ... 0x00 XOR`

Example Command (200 sensitivity with purple lights): `char-write-cmd 33050301c87e42f5000000000000000000000035`

## Other Packets

### Keep Alive
This packet is sent by the mobile app (along with another minor variation)

Format: `0xAA 0x01 0x00 ... 0x00 0xAB`

Example Command: `char-write-cmd 0x0015 aa010000000000000000000000000000000000ab`
