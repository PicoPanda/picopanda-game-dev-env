import pico8
import picopanda
import re
from pathlib import Path

FILE_NAME = "testp8.p8"
SFX_LINE_LENGTH = 168
SFX_NOTE_AMOUNT = 32
AUDIO_CONFIG_SIZE = 256

def stringIsHexOnly(s: str) -> bool:
    return bool((re.fullmatch(r"[0-9a-fA-F]+", s)))


if __name__ == "__main__":
    print("PICO-8 Asset Converter")

    # Check that the file exists.
    pico8_filePath = Path(FILE_NAME)
    if(pico8_filePath.is_file()) :
        # Extract the pico8 sfx.
        pico8_sfx = []
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            readingSfx = False
            currentLineNum = 0
            sfxLineNum = 0
            sfxNum = 0

            for line in f:
                currentLineNum += 1
                # Strip leading/trailing whitespace
                stripped = line.strip()

                if(not readingSfx):
                    # Check if the line starts with "__sfx__"
                    if stripped.startswith("__sfx__"):
                        sfxLineNum = currentLineNum
                        print("Found {:s} at line {:d}".format(stripped, sfxLineNum))
                        readingSfx = True
                else:
                    # Parsing sound effects.
                    lineLength = len(stripped)
                    if((lineLength == SFX_LINE_LENGTH) and stringIsHexOnly(stripped)):
                        s = pico8.Sfx(sfxNum)
                        sfxNum += 1
                        s.initFromHexString(stripped)
                        pico8_sfx.append(s)
                    else:
                        print("Finished parsing SFX at line {:d}".format(currentLineNum))
                        break

        # Create the picopanda sfx
        picopanda_phrases = []
        for p8s in pico8_sfx:
            pps = picopanda.Phrase(index = p8s.index, ticksPerNote = p8s.speed, loopStart = p8s.loopStart, loopEnd = p8s.loopEnd)
            for p8n in p8s.notes:
                ppn = picopanda.Note()
                ppn.initFromPico8Params(note= p8n.note, octave = p8n.octave, instrument = p8n.instrument, volume = p8n.volume, effect = p8n.effect)
                pps.notes.append(ppn)
            picopanda_phrases.append(pps)

        # Create the binary data.
        phraseNumber = 0
        configData = bytearray(AUDIO_CONFIG_SIZE) # For future use.
        phraseData = bytearray()
        noteData = bytearray()
        # Insert the converted phrases.
        for phrase in picopanda_phrases:
            phraseData += phrase.phraseDataToByteArray()
            noteData += phrase.noteDataToByteArray()
            phraseNumber += 1
        # Fill the rest of the data with empty phrases.
        emptyPhrase = picopanda.Phrase(phraseNumber)
        emptyPhrase.addEmptyNotes(SFX_NOTE_AMOUNT)
        for i in range(phraseNumber, 256):
            phraseData += emptyPhrase.phraseDataToByteArray()
        for i in range(phraseNumber, 64):
            noteData += emptyPhrase.noteDataToByteArray()

        # Create the binary file with the audio data.
        picopanda_audioFile = pico8_filePath.stem + "_picoPanda_audio.bin"
        with open(picopanda_audioFile, "wb") as f:
            f.write(noteData)
            #f.write(configData)
            f.write(phraseData)
    else:
        raise Exception("Cannot find a file named {:s}".format(FILE_NAME))
