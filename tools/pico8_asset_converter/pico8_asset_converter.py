import pico8
import picopanda
import argparse
import re
from pathlib import Path


def stringIsHexOnly(s: str) -> bool:
    return bool((re.fullmatch(r"[0-9a-fA-F]+", s)))


def extractPico8Sfx(filePathObject: Path) -> list[pico8.Sfx]:
    # Extract the pico8 sfx.
    pico8_sfx = []
    with open(filePathObject.name, "r", encoding="utf-8") as f:
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
                if((lineLength == pico8.Sfx.LINE_LENGTH) and stringIsHexOnly(stripped)):
                    s = pico8.Sfx(sfxNum)
                    sfxNum += 1
                    s.initFromHexString(stripped)
                    pico8_sfx.append(s)
                else:
                    print("Finished parsing SFX at line {:d}".format(currentLineNum))
                    break
    
    return pico8_sfx

def createPicoPandaPhrases(pico8_sfx: list[pico8.Sfx]) -> list[picopanda.Phrase]:
    # Create the picopanda sfx
    picopanda_phrases = []
    for p8s in pico8_sfx:
        pps = picopanda.Phrase(index = p8s.index, ticksPerNote = p8s.speed, loopStart = p8s.loopStart, loopEnd = p8s.loopEnd)
        for p8n in p8s.notes:
            ppn = picopanda.Note()
            ppn.initFromPico8Params(note = p8n.note, octave = p8n.octave, instrument = p8n.instrument, volume = p8n.volume, effect = p8n.effect)
            pps.notes.append(ppn)
        picopanda_phrases.append(pps)

    return picopanda_phrases

def convertPicoPandaPhrasesToByteArray(picopanda_phrases: list[picopanda.Phrase]) -> bytearray:
    # Create the binary data.
    phraseNumber = 0
    phraseData = bytearray()
    noteData = bytearray()
    # Insert the converted phrases.
    for phrase in picopanda_phrases:
        phraseData += phrase.phraseDataToByteArray()
        noteData += phrase.noteDataToByteArray()
        phraseNumber += 1
    # Fill the rest of the data with empty phrases.
    emptyPhrase = picopanda.Phrase(phraseNumber)
    emptyPhrase.addEmptyNotes(pico8.Sfx.NOTE_AMOUNT)
    for i in range(phraseNumber, 256):
        phraseData += emptyPhrase.phraseDataToByteArray()
    for i in range(phraseNumber, 64):
        noteData += emptyPhrase.noteDataToByteArray()

    # Combine the noteData and the phraseData in the expected order.
    noteAndPhraseData = noteData + phraseData
    return noteAndPhraseData

def extractPico8SpriteSheet(filePathObject: Path):
    # Extract the pico8 sfx.
    pico8_spriteSheet = pico8.SpriteSheet()
    with open(filePathObject.name, "r", encoding="utf-8") as f:
        readingGfx = False
        currentLineNum = 0
        gfxLineNum = 0
    
        for line in f:
            currentLineNum += 1
            # Strip leading/trailing whitespace
            stripped = line.strip()

            if(not readingGfx):
                # Check if the line starts with "__gfx__"
                if stripped.startswith("__gfx__"):
                    gfxLineNum = currentLineNum
                    print("Found {:s} at line {:d}".format(stripped, gfxLineNum))
                    readingGfx = True
            else:
                # Parsing sound sprite sheet lines.
                lineLength = len(stripped)
                if((lineLength == pico8.SpriteSheet.LINE_LENGTH) and stringIsHexOnly(stripped)):
                    pico8_spriteSheet.addLine(stripped)
                else:
                    print("Finished parsing GFX at line {:d}".format(currentLineNum))
                    break
    
    return pico8_spriteSheet

def createPicoPandaSpriteSheet(pico8_spriteSheet: pico8.SpriteSheet) -> picopanda.SpriteSheet:
    picopanda_spriteSheet = picopanda.SpriteSheet()
    picopanda_spriteSheet.initFromPico8PixelArray(pico8_spriteSheet.pixelArray)
    return picopanda_spriteSheet

def extractPico8SpriteFlags(filePathObject):
    # Extract the pico8 sfx.
    pico8_spriteFlags = pico8.SpriteFlags()
    with open(filePathObject.name, "r", encoding="utf-8") as f:
        readingGff = False
        currentLineNum = 0
        gffLineNum = 0
    
        for line in f:
            currentLineNum += 1
            # Strip leading/trailing whitespace
            stripped = line.strip()

            if(not readingGff):
                # Check if the line starts with "__gff__"
                if stripped.startswith("__gff__"):
                    gffLineNum = currentLineNum
                    print("Found {:s} at line {:d}".format(stripped, gffLineNum))
                    readingGff = True
            else:
                # Parsing sound sprite flag lines.
                lineLength = len(stripped)
                if((lineLength == pico8.SpriteFlags.LINE_LENGTH) and stringIsHexOnly(stripped)):
                    pico8_spriteFlags.addLine(stripped)
                else:
                    print("Finished parsing GFF at line {:d}".format(currentLineNum))
                    break
    
    return pico8_spriteFlags

def createPicoPandaSpriteFlags(pico8_spriteFlags: pico8.SpriteFlags) -> picopanda.SpriteFlags:
    picopanda_spriteFlags = picopanda.SpriteFlags()
    picopanda_spriteFlags.initFromPico8FlagsArray(pico8_spriteFlags.flagsArray)
    return picopanda_spriteFlags

def extractPico8TileMap(filePathObject):
    # Extract the pico8 sfx.
    pico8_tileMap = pico8.TileMap()
    with open(filePathObject.name, "r", encoding="utf-8") as f:
        readingMap = False
        currentLineNum = 0
        mapLineNum = 0
    
        for line in f:
            currentLineNum += 1
            # Strip leading/trailing whitespace
            stripped = line.strip()

            if(not readingMap):
                # Check if the line starts with "__gff__"
                if stripped.startswith("__map__"):
                    mapLineNum = currentLineNum
                    print("Found {:s} at line {:d}".format(stripped, mapLineNum))
                    readingMap = True
            else:
                # Parsing sound tile map lines.
                lineLength = len(stripped)
                if((lineLength == pico8.TileMap.LINE_LENGTH) and stringIsHexOnly(stripped)):
                    pico8_tileMap.addLine(stripped)
                else:
                    print("Finished parsing MAP at line {:d}".format(currentLineNum))
                    break
    
    return pico8_tileMap

def createPicoPandaTileMap(pico8_tileMap: pico8.TileMap) -> picopanda.TileMap:
    picopanda_tileMap = picopanda.TileMap()
    picopanda_tileMap.initFromPico8TileArray(pico8_tileMap.tileArray)
    return picopanda_tileMap


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Extract PICO-8 assets to binary format expected by PicoPanda.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Examples:
            %(prog)s --input my_pico8_file.p8 --sprites
            %(prog)s --input my_pico8_file.p8 --sfx
            %(prog)s --i my_pico8_file.p8 -s -x
        """
    )

    # Required arguments
    parser.add_argument("-i", "--input", required=True, help="Input PICO-8 file with .p8 extension.")
    
    # Optional arguments
    # Each option below is optional, but at least one must be given.
    parser.add_argument("-g", "--graphics", action="store_true", help="Extract and convert the sprite sheet, sprite flags and tile map.")
    parser.add_argument("-x", "--sfx",  action="store_true", help="Extract and convert sound effects.")

    args = parser.parse_args()

    if(args.graphics or args.sfx):

        pico8_filePath = Path(args.input)

        # Check the file extension.
        if(pico8_filePath.suffix == '.p8'):

            # Check that the file exists.
            if(pico8_filePath.is_file()) :

                print("PICO-8 Asset Converter")

                # Extract and convert the graphics if selected.
                if(args.graphics):
                    pico8_spriteSheet = extractPico8SpriteSheet(pico8_filePath)
                    pico8_spriteFlags = extractPico8SpriteFlags(pico8_filePath)
                    pico8_tileMap = extractPico8TileMap(pico8_filePath)

                    picopanda_spriteSheet = createPicoPandaSpriteSheet(pico8_spriteSheet)
                    picopanda_spriteFlags = createPicoPandaSpriteFlags(pico8_spriteFlags)
                    picopanda_tileMap = createPicoPandaTileMap(pico8_tileMap)

                    # Create the binary file with the graphics data.
                    picopanda_graphicsFile = pico8_filePath.stem + "_pp_graphics.bin"
                    with open(picopanda_graphicsFile, "wb") as f:
                        f.write(picopanda_spriteSheet.toByteArray())
                        f.write(picopanda_tileMap.toByteArray())
                        f.write(picopanda_spriteFlags.toByteArray())
                    
                    print("Created {:s}".format(picopanda_graphicsFile))

                # Extract and convert the sound effects if selected.
                if(args.sfx):
                    pico8_sfx = extractPico8Sfx(pico8_filePath)
                    picopanda_phrases = createPicoPandaPhrases(pico8_sfx)
                    noteAndPhraseData = convertPicoPandaPhrasesToByteArray(picopanda_phrases)

                    # Create the binary file with the audio data.
                    picopanda_audioFile = pico8_filePath.stem + "_pp_audio.bin"
                    with open(picopanda_audioFile, "wb") as f:
                        f.write(noteAndPhraseData)

                    print("Created {:s}".format(picopanda_audioFile))

            else:
                parser.error("Cannot find a file named {:s}".format(args.input))

        else:
            parser.error("Input file must have the .p8 extension.") 

    else:
        parser.error("At least one asset type must be specified for extraction.")
        parser.print_usage()
