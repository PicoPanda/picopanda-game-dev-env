class Note:
    """
    Python class for holding the data of a pico-8 note.
    """

    noteNames = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    def __init__(self):
        self.__noteNumber = 0
        self.instrument = 0
        self.volume = 0
        self.effect = 0

    def __str__(self):
        retString = "{:2s}".format(self.noteNames[self.note])
        retString += format(self.octave, "01x")
        retString += format(self.instrument, "01x")
        retString += format(self.volume, "01x")
        retString += format(self.effect, "01x")
        return retString

    def initFromHexString(self, hexString):
        if(type(hexString).__name__ == 'str'):
            if(len(hexString) == 5):
                self.__noteNumber = int(hexString[0:2], 16)
                self.instrument = int(hexString[2:3], 16)
                self.volume = int(hexString[3:4], 16)
                self.effect = int(hexString[4:5], 16)
            else:
                raise ValueError("hexString must be 5 characters long")
        else:
            raise TypeError("hexString must be a string type")

    @property
    def octave(self):
        return int(self.__noteNumber / 12)

    @property
    def note(self):
        return (self.__noteNumber % 12)


class Sfx:
    """
    Python class for holding the data of a pico-8 sound effect.
    """

    def __init__(self, index):
        self.index = index
        self.settings = 0
        self.speed = 16
        self.loopStart = 0
        self.loopEnd = 0
        self.notes = []

    def __str__(self):
        retString = "SFX {:02d}\tSPD {:03d}\tLOOP {:02d} {:02d}\n".format(self.index, self.speed, self.loopStart, self.loopEnd)
        retString += "\tN OIVE\tN OIVE\tN OIVE\tN OIVE\n"
        for n in range(int(len(self.notes) / 4)):
            retString += "\t" + str(self.notes[n]) + "\t" + str(self.notes[n+8]) + "\t" + str(self.notes[n + 16]) + "\t" + str(self.notes[n + 24]) + "\n"
        return retString

    def initFromHexString(self, hexString):
        self.settings = int(hexString[0:2], 16)
        self.speed = int(hexString[2:4], 16)
        self.loopStart = int(hexString[4:6], 16)
        self.loopEnd = int(hexString[6:8], 16)
        stringPos = 8
        for i in range(32):
            n = Note()
            n.initFromHexString(hexString[stringPos: (stringPos+5)])
            self.notes.append(n)
            stringPos = stringPos + 5

