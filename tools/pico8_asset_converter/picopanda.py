import struct

class Note:
    """
    Python class for holding the data of a PicoPanda note.
    """

    noteNames = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    '''
    Instrument Mapping
    PICO-8                  PicoPanda                           Mapping ( P8 - PP)
    0 - Triangle            0 - Square                          0 - 2
    1 - Tilted Saw          1 - Pulse                           1 - 3
    2 - Straight Saw        2 - Triangle                        2 - 4
    3 - Square              3 - Tilted Saw                      3 - 0
    4 - Pulse               4 - Straight Saw                    4 - 1
    5 - Organ               5 - Sin                             5 - 6
    6 - Noise               6 - Organ                           6 - 9
    7 - Phaser              7 - White Noise Table Linear        7 - 5
                            8 - White Noise Table Hyperbolic    
                            9 - Random Bit Noise                
    '''
    p8ToPpMap_instrument = [2, 3, 4, 0, 1, 6, 9, 5]
    '''
    Effect Mapping
    PICO-8                  PicoPanda                           Mapping ( P8 - PP)
    0 - None                0 - None                            0 - 0
    1 - Slide               1 - Fade In                         1 - 0
    2 - Vibrato             2 - Fade Out                        2 - 0
    3 - Drop                3 - TBD                             3 - 0
    4 - Fade In             4 - TBD                             4 - 1
    5 - Fade Out            5 - TBD                             5 - 2
    6 - Arpeggio Fast       6 - TBD                             6 - 0
    7 - Arpeggio Slow       7 - TBD                             7 - 0
    '''
    p8ToPpMap_effect = [0, 0, 0, 0, 1, 2, 0, 0]

    def __init__(self):
        self.note = 0
        self.octave = 4
        self.instrument = 10 # Silence
        self.volumeLeft = 0
        self.volumeRight = 0
        self.effect = 0

    def __str__(self):
        retString = "{:2s}".format(self.noteNames[self.note])
        retString += format(self.octave, "01x")
        retString += format(self.instrument, "01x")
        retString += format(self.volumeLeft, "01x")
        retString += format(self.volumeRight, "01x")
        retString += format(self.effect, "01x")
        return retString

    def initFromPico8Params(self, note, octave, instrument, volume, effect):
        if(volume != 0):
            self.note = note
            self.octave = octave + 2
            self.instrument = self.p8ToPpMap_instrument[instrument]
            self.volumeLeft = volume
            self.volumeRight = volume
            self.effect = self.p8ToPpMap_effect[effect]

    def toByteArray(self):
        noteInt = ((self.note & 0xFF) << 28)
        noteInt = noteInt | ((self.octave & 0xFF) << 24)
        noteInt = noteInt | ((self.instrument & 0xFF) << 20)
        noteInt = noteInt | ((self.volumeLeft & 0xFF) << 16)
        noteInt = noteInt | ((self.volumeRight & 0xFF) << 12)
        noteInt = noteInt | ((self.effect & 0xFF) << 8)
        ba = bytearray(noteInt.to_bytes(4, "little"))
        return ba


class Phrase:
    """
    Python class for holding the data of a PicoPanda sound effect.
    """

    def __init__(self, index, ticksPerNote=16, loopStart=0, loopEnd=0):
        self.index = index
        self.ticksPerNote = ticksPerNote
        self.loopStart = loopStart
        self.loopEnd = loopEnd
        self.notes = []

    def __str__(self):
        retString = "SFX {:02d}\tTPN {:03d}\tLOOP {:02d} {:02d}\n".format(self.index, self.ticksPerNote, self.loopStart, self.loopEnd)
        retString += "\tN OILRE\tN OILRE\tN OILRE\tN OILRE\n"
        for n in range(int(len(self.notes) / 4)):
            retString += "\t" + str(self.notes[n]) + "\t" + str(self.notes[n+8]) + "\t" + str(self.notes[n + 16]) + "\t" + str(self.notes[n + 24]) + "\n"
        return retString

    def addEmptyNotes(self, numNotes=32):
        for i in range(numNotes):
            emptyNote = Note()
            self.notes.append(emptyNote)

    def phraseDataToByteArray(self):
        ba = bytearray(struct.pack("BBB", self.ticksPerNote, self.loopStart, self.loopEnd))
        return ba

    def noteDataToByteArray(self):
        ba = bytearray()
        for note in self.notes:
            ba += note.toByteArray()
        return ba

class SpriteSheet:
    """
    Python class for holding the data of a pico-8 sprite sheet.
    """

    PIXEL_AMOUNT = 16384

    def __init__(self):
        self.paletteMap = [15, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        self.pixelArray = []

    def __str__(self):
        retString = ""
        for n in range(0, len(self.pixelArray), 2):
            if((n != 0) and ((n % 32) == 0)):
                retString += "\n"
            retString += "{:01X}{:01X} ".format(self.pixelArray[n], self.pixelArray[n+1])
        
        retString += "\n"
        return retString

    def initFromPico8PixelArray(self, pixelArray: list[int]):
        for pixel in pixelArray:
            p = pixel & 0x0F
            self.pixelArray.append(self.paletteMap[p])

        # Make sure the pixel array is a multiple of 2.
        if((len(self.pixelArray) % 2) != 0):
            self.pixelArray.append(self.paletteMap[0])

    def pixelArrayToByteArray(self, fill=True):
        ba = bytearray()
        for n in range(0, len(self.pixelArray), 2):
            pixelPair = self.pixelArray[n] + (self.pixelArray[n+1] << 4)
            ba += bytearray(pixelPair.to_bytes(1, "little"))
        
        if(fill):
            for n in range(len(self.pixelArray), self.PIXEL_AMOUNT, 2):
                pixelPair = self.paletteMap[0] + (self.paletteMap[0]  << 4)
                ba += bytearray(pixelPair.to_bytes(1, "little"))

        return ba
