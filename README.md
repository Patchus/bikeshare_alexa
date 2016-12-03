# Bikeshare Alexa App

## Purpose
The goal is to call alexa and have it check to see if there are bikes in your approved list.
You need to complete two lists in the code for this to work. You need a pickup location and a drop off location

Ideally, I would create the app so that it could take an input to check the station. That requires what Alexa
calls "slots". You could put every station location in the slow and build some more logic. Since I did this
quickly, didnt want to go into that too much.

The station list needs to look like
`python pickup_stations = {'Station Name':Station Number} `

### Gotchya's
#### Python
Obviously you are limited to what stations you hard code into the python script.
There is another thing that is tricky with Alexa. You have to build compiled pythong and submit this as a zip.
If you are like me, and use Homebrew that is tricky. 

You need to do this
`vim ~/.pydistutils.cfg`
Insert this into that file
```[install]
prefix= ```

Once that file is created you can then run this
```pip install xmltodict -t ~/ ```

This will create a local version.
You then have to zip the files, not the folder.

#### Alexa
This was never mentioned, but you need to add sample Utterances. They follow the format 
DOTHIS WHEN THEY SAY THIS.

```PickUp PickUp
DropOff DropOff
PickUp if i can pick up
PickUp if I can pick up near by bikes
DropOff if i can drop off
DropOff if i can drop off a bike```