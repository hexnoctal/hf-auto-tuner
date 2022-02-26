# hf-tuner
Flask App for the Palstar HF-Auto Auto-Tuner

## Overview

The Palstar HF-Auto is truly a luxury device for amateur radio HF operations.  No longer is time wasted spinning inductor cranks and capacitor knobs listening for noise floor changes before making final tweaks under power.  The HF-Auto engages in smart calculations to determine antenna tuning, and then stores those values by frequency for each antenna port.  The spin-and-hunt is replaced by just a few seconds of smart tuning once power is applied.

I was able to pick one up used along with the accompanying remote unit at a swap from the station of a deceased amateur.  It quickly became my favorite station accessory.

## My Use Case

My station was always in the basement next to the antenna ingress point.  Working permanently from home allowed me to create a home-office, and I planned to move my station into that room.  The remote cable supplied was not going to be long enough, so I researched the requirements to start using the remote unit.  As the station arrangement in the home-office as temporary (awaiting a new desk), the surface area became scarce and I started to think of that maybe I could
control the tuner in the basement in a different manner.

There had to be a better way and the work for a remote Flask app began.

## Your Requirements

* Python 3.9
* Flask dependencies installed
* Contemporary web browser 
* Basic knowledge of running Python apps, Pip, setting up local networking

Note:  This is a Flask application and is not intended to sit on the internet as provided.  Please use a proper wsgi front-end or proxy (such as Nginx) if this is to face the internet.  ZERO access controls are provided!  You have been warned


## Starting

./app.py --tty=/dev/ttyUSB0 --url_host=hostname/ip --port=10000

The url_host option fills in the template for url callbacks.
Port is optional, defaults to 10000.


## To Do

* Debug other frames (input and output)
* Better UI (likely not by me, ever)
* Eliminate url_host config option
* Investigate endian problems with byte/str/int translations on other CPUs

## Footnotes

### How to Debug Serial Protocols

Long ago in a different career, I was tasked with creating remote control interfaces for some very legacy equipment
such as satellite controllers, receivers, RF monitors, modulation monitors and various other equipment using RS-232, RS-422 and RS-485.  Some used established protocols, some used a mix of protocols, some had their own weird methods.  It was this kind of work that gave me the troubleshooting skills with serial data.

If you wish to engage in this type of effort, I have detailed my methods.

#### 1.  Be Certain of the Speed and Format

It is easy to plug into a device and see data and think, "hey, I'm set".  Not so fast, turbo.  While the bytes streaming across your terminal might change with button presses or input to the device you are exploring, that doesn't mean it is correct.  Incorrect speed, stop-bits or parity can send your work down a non-returnable rabbit hole of wasted time.  Research the port settings.

What if you can't find information on the port settings?  Break out the oscilloscope.  The 'oscope will guide your path as to speed and format.

#### 2.  Get the Right Tools

You'll need a good breakout box, preferably one with jumpers that allows you to assert control lines.  Another valuable tool is a Y-cable that allows for selecting transmit through diode steering to a third device.  This is how I have monitored serial sessions since, well forever.  

Usually, hardware is unforgiving if you do not present the right control signals or have a test fixture that loads the line.

#### 3.  Look for Bit Patterns

Now that you're watching the device work, you can see what data is available.  Nearly all well thought-out industrial grade protocols send in a repeated pattern of an instruction/mnemonic code(s), data and a checksum.  The first step is to identify the start and end.  This can be tricky, and next to impossible if you don't have the line settings correct.  

01 02 <byte + 1> ... <byte N-1> FF 

The example above is a typical frame sent from a device.  01 describes the type of frame, with byte 02 possibly being related.
The byte FF is the checksum.  And the whole thing repeats again and again.  Often the instruction/mnemonic bytes for frame identifiers are close in value as the developer has reserved 16 addresses or more.

#### 4.  Test Your Captures

Once a frame has been detected, you can test if the frame has a checksum.  Fortunately, most small microcontrollers use easy to find checksum methods.  Try the standard of sum all bytes up to the checksum, and the XOR it.  Start with FF and work your way down.  If you get occasional success, then it is possible they compute the checksum and add 1 to  avoid having 0x00 as a checksum value.  Or they add something else.

#### 5.  Figuring Out the Inputs

Obviously the easiest way to figure out input is to watch it.  But what if you can't?  You can always try to brute force a control input, but only if the device is out of operation.  Input frames will follow a similar format to the output, but usually smaller.  Snooping, these will often have 0x00 padding empty values.  Small programs to cycle through bit codes with proper checksums until something changes (brute force) will work, but requires constant attention looking for signs that you've tripped a firmware upload loader or other signs that you've gone too far.  Again, the addresses/frame identifiers/mnemonics for input is possibly close in value to those of outputs.

If brute forcing seems dangerous, the next step is to try to break out a logic analyzer.  If you are handy with Texas Instruments development boards, the tools and features afforded often provide insight into the operation of the device.

### The HF-Auto Protocol

This device requires 4800-N-2 serial settings.  It streams a 12 byte status frame continuously.

77 02 03 04 05 06 07 08 09 10 11 12

77 - Instruction byte.  Labels this as a status frame  
01 - 1=auto 2=manual 3=bypass  
02 - Frequency high word  
03 - Frequency low word  
04 - Capacitance  
05 - ?? bit packed with antenna port. Port is highest two bits of lowest byte  
06 - Inductance  
08 - Power (likely low word)  
09 - Power high word (untested but likely)  
10 - VSWR high word  
11 - VSWR low word  
12 - Checksum (XOR 0xFF) + 1  


Inputs

7A 01 02 03

7A - Instruction for input  
01 - Mnemonic   
         31-33 is antenna selector  
         61, 62, is mode (auto, manual)  
02 - Input value (not used with 7A, always 0x00)  
03 - Checksum (same as above)  







02471a4f3291c5515bfc49c67d23119fe2f802c159ef097a3ff77d6737a74c3e
7d2d46cb8d3896ee696a175999081f22f30bdcb12c857e76170ff978171b5f2c
e9a1d2118c186a86d0fc6fc4226ec0302fe91e981d4a7effdf4fb694009a36aa
e027a3ea9142e66a4e6f73d4e805650e14a4f5d6a1a949f5d6cbaba391846153



