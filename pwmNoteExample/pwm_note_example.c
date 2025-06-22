#include <stdio.h>
#include "pico/stdlib.h"
#include "audio/pwm_note.h"

typedef struct{
    audio_instrument_e instrument;
    audio_note_e note;
    audio_octave_e octave;
    audio_volume_e volume;
    uint16_t duration;
} noteDetails;

noteDetails noteChartCh0[] = {
    {audio_instrument_SQUARE, audio_note_E, audio_octave_2, audio_volume_10, 14u},
    {audio_instrument_SQUARE, audio_note_Db, audio_octave_2, audio_volume_10, 14u},
    {audio_instrument_SQUARE, audio_note_Bb, audio_octave_1, audio_volume_10, 14u},
    {audio_instrument_SQUARE, audio_note_G, audio_octave_1, audio_volume_10, 14u},
    {audio_instrument_SQUARE, audio_note_E, audio_octave_1, audio_volume_10, 14u},
    {audio_instrument_SQUARE, audio_note_Db, audio_octave_1, audio_volume_10, 14u},
    {audio_instrument_SQUARE, audio_note_Bb, audio_octave_0, audio_volume_10, 14u},
    {audio_instrument_SQUARE, audio_note_G, audio_octave_0, audio_volume_10, 14u},
    {audio_instrument_SQUARE, audio_note_E, audio_octave_0, audio_volume_10, 56u},
    {audio_instrument_SILENCE, audio_note_A, audio_octave_4, audio_volume_0, 440u},
    {audio_instrument_NOISE_BIT, audio_note_A, audio_octave_6, audio_volume_8, 168u},
    {audio_instrument_SILENCE, audio_note_A, audio_octave_4, audio_volume_0, 440u}
};

noteDetails noteChartCh1[] = {
    {audio_instrument_SQUARE, audio_note_E, audio_octave_2, audio_volume_8, 816u},
    {audio_instrument_SILENCE, audio_note_A, audio_octave_4, audio_volume_0, 96u},
    {audio_instrument_SQUARE, audio_note_E, audio_octave_2, audio_volume_8, 304u},
    {audio_instrument_SQUARE, audio_note_G, audio_octave_2, audio_volume_8, 304u},
    {audio_instrument_SQUARE, audio_note_C, audio_octave_3, audio_volume_8, 304u},
    {audio_instrument_SQUARE, audio_note_D, audio_octave_3, audio_volume_8, 304u},
    {audio_instrument_SQUARE, audio_note_G, audio_octave_3, audio_volume_8, 304u},
    {audio_instrument_SQUARE, audio_note_E, audio_octave_3, audio_volume_8, 816u},
    {audio_instrument_SILENCE, audio_note_A, audio_octave_3, audio_volume_0, 96u},
    {audio_instrument_SQUARE, audio_note_E, audio_octave_2, audio_volume_8, 304u},
    {audio_instrument_SQUARE, audio_note_G, audio_octave_2, audio_volume_8, 304u},
    {audio_instrument_SQUARE, audio_note_C, audio_octave_3, audio_volume_8, 304u},
    {audio_instrument_SQUARE, audio_note_D, audio_octave_2, audio_volume_8, 512u},
    {audio_instrument_SILENCE, audio_note_A, audio_octave_3, audio_volume_0, 96u},
};

noteDetails noteChartCh2_progression0[] = {
    {audio_instrument_SILENCE, audio_note_A, audio_octave_5, audio_volume_0, 8512u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_10, 1216u}
};

noteDetails noteChartCh2_progression1[] = {
    {audio_instrument_SIN, audio_note_A, audio_octave_5, audio_volume_10, 304u},
    {audio_instrument_SIN, audio_note_Bb, audio_octave_5, audio_volume_10, 48u}, // Slide up to B
    {audio_instrument_SIN, audio_note_B, audio_octave_5, audio_volume_10, 560u},
    {audio_instrument_SIN, audio_note_B, audio_octave_5, audio_volume_10, 64u},  // Fade out.
    {audio_instrument_SIN, audio_note_B, audio_octave_5, audio_volume_8, 64u},
    {audio_instrument_SIN, audio_note_B, audio_octave_5, audio_volume_6, 64u},
    {audio_instrument_SIN, audio_note_B, audio_octave_5, audio_volume_4, 64u},
    {audio_instrument_SILENCE, audio_note_B, audio_octave_5, audio_volume_0, 48u}, // 1216
    {audio_instrument_SIN, audio_note_A, audio_octave_5, audio_volume_10, 304u},
    {audio_instrument_SIN, audio_note_G, audio_octave_5, audio_volume_10, 304u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_10, 304u},
    {audio_instrument_SIN, audio_note_D, audio_octave_5, audio_volume_10, 304u},  // 2432 Can fade here
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_10, 1216u}, // 3648
    {audio_instrument_SIN, audio_note_G, audio_octave_5, audio_volume_10, 304u},
    {audio_instrument_SIN, audio_note_C, audio_octave_5, audio_volume_10, 304u},
    {audio_instrument_SIN, audio_note_D, audio_octave_5, audio_volume_10, 64u},
    {audio_instrument_SIN, audio_note_D, audio_octave_5, audio_volume_8, 64u},
    {audio_instrument_SIN, audio_note_D, audio_octave_5, audio_volume_6, 64u},
    {audio_instrument_SIN, audio_note_D, audio_octave_5, audio_volume_4, 64u},
    {audio_instrument_SILENCE, audio_note_D, audio_octave_5, audio_volume_0, 48u},
    {audio_instrument_SIN, audio_note_D, audio_octave_5, audio_volume_10, 304u}, // 4864
    {audio_instrument_SIN, audio_note_A, audio_octave_5, audio_volume_10, 304u},
    {audio_instrument_SIN, audio_note_Bb, audio_octave_5, audio_volume_10, 48u}, // Slide up to B
    {audio_instrument_SIN, audio_note_B, audio_octave_5, audio_volume_10, 560u},
    {audio_instrument_SIN, audio_note_B, audio_octave_5, audio_volume_10, 64u},  // Fade out.
    {audio_instrument_SIN, audio_note_B, audio_octave_5, audio_volume_8, 64u},
    {audio_instrument_SIN, audio_note_B, audio_octave_5, audio_volume_6, 64u},
    {audio_instrument_SIN, audio_note_B, audio_octave_5, audio_volume_4, 64u},
    {audio_instrument_SILENCE, audio_note_B, audio_octave_5, audio_volume_0, 48u}, // 6080
    {audio_instrument_SIN, audio_note_A, audio_octave_5, audio_volume_10, 304u},
    {audio_instrument_SIN, audio_note_G, audio_octave_5, audio_volume_10, 304u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_10, 64u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_8, 64u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_6, 64u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_4, 64u},
    {audio_instrument_SILENCE, audio_note_E, audio_octave_5, audio_volume_0, 48u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_10, 304u},  // 7296
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_10, 912u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_10, 64u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_8, 64u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_6, 64u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_4, 64u},
    {audio_instrument_SILENCE, audio_note_E, audio_octave_5, audio_volume_0, 48u}, // 8512
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_10, 304u},
    {audio_instrument_SIN, audio_note_D, audio_octave_5, audio_volume_10, 304u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_10, 64u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_8, 64u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_6, 64u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_4, 64u},
    {audio_instrument_SILENCE, audio_note_E, audio_octave_5, audio_volume_0, 48u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_10, 64u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_8, 64u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_6, 64u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_4, 64u},
    {audio_instrument_SILENCE, audio_note_E, audio_octave_5, audio_volume_0, 48u}  // 9728
};

noteDetails noteChartCh2_progression2[] = {
    {audio_instrument_SIN, audio_note_A, audio_octave_5, audio_volume_10, 304u},
    {audio_instrument_SIN, audio_note_B, audio_octave_5, audio_volume_10, 304u},
    {audio_instrument_SIN, audio_note_A, audio_octave_5, audio_volume_10, 304u},
    {audio_instrument_SIN, audio_note_B, audio_octave_5, audio_volume_10, 304u}, // 1216
    {audio_instrument_SIN, audio_note_B, audio_octave_5, audio_volume_10, 304u},
    {audio_instrument_SIN, audio_note_A, audio_octave_5, audio_volume_10, 64u},
    {audio_instrument_SIN, audio_note_A, audio_octave_5, audio_volume_8, 64u},
    {audio_instrument_SIN, audio_note_A, audio_octave_5, audio_volume_6, 64u},
    {audio_instrument_SIN, audio_note_A, audio_octave_5, audio_volume_4, 64u},
    {audio_instrument_SILENCE, audio_note_A, audio_octave_5, audio_volume_0, 48u},
    {audio_instrument_SIN, audio_note_A, audio_octave_5, audio_volume_10, 64u},
    {audio_instrument_SIN, audio_note_A, audio_octave_5, audio_volume_8, 64u},
    {audio_instrument_SIN, audio_note_A, audio_octave_5, audio_volume_6, 64u},
    {audio_instrument_SIN, audio_note_A, audio_octave_5, audio_volume_4, 64u},
    {audio_instrument_SILENCE, audio_note_A, audio_octave_5, audio_volume_0, 48u},
    {audio_instrument_SIN, audio_note_A, audio_octave_5, audio_volume_10, 304u}, // 2432
    {audio_instrument_SIN, audio_note_A, audio_octave_5, audio_volume_10, 608u},
    {audio_instrument_SIN, audio_note_A, audio_octave_5, audio_volume_10, 64u},
    {audio_instrument_SIN, audio_note_A, audio_octave_5, audio_volume_8, 64u},
    {audio_instrument_SIN, audio_note_A, audio_octave_5, audio_volume_6, 64u},
    {audio_instrument_SIN, audio_note_A, audio_octave_5, audio_volume_4, 64u},
    {audio_instrument_SILENCE, audio_note_A, audio_octave_5, audio_volume_0, 48u},
    {audio_instrument_SIN, audio_note_A, audio_octave_5, audio_volume_10, 64u},
    {audio_instrument_SIN, audio_note_A, audio_octave_5, audio_volume_8, 64u},
    {audio_instrument_SIN, audio_note_A, audio_octave_5, audio_volume_6, 64u},
    {audio_instrument_SIN, audio_note_A, audio_octave_5, audio_volume_4, 64u},
    {audio_instrument_SILENCE, audio_note_A, audio_octave_5, audio_volume_0, 48u}, // 3648
    {audio_instrument_SIN, audio_note_A, audio_octave_5, audio_volume_10, 304u},
    {audio_instrument_SIN, audio_note_G, audio_octave_5, audio_volume_10, 304u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_10, 608u}, // 4864
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_10, 608u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_10, 208u},
    {audio_instrument_SILENCE, audio_note_E, audio_octave_5, audio_volume_0, 96u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_10, 208u},
    {audio_instrument_SILENCE, audio_note_E, audio_octave_5, audio_volume_0, 96u}, // 6080
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_10, 208u},
    {audio_instrument_SILENCE, audio_note_E, audio_octave_5, audio_volume_0, 96u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_10, 208u},
    {audio_instrument_SILENCE, audio_note_E, audio_octave_5, audio_volume_0, 96u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_10, 304u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_10, 208u},
    {audio_instrument_SILENCE, audio_note_E, audio_octave_5, audio_volume_0, 96u},  // 7296
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_10, 272u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_9, 240u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_8, 240u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_7, 240u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_6, 240u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_5, 240u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_4, 240u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_3, 240u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_2, 240u},
    {audio_instrument_SIN, audio_note_E, audio_octave_5, audio_volume_1, 240u}   // 9728 
};

noteDetails *noteChartCh2_progressions[] = {
    noteChartCh2_progression0,
    noteChartCh2_progression1,
    noteChartCh2_progression2
};

uint8_t noteChartCh0_maxNoteIndex;
uint8_t noteChartCh1_maxNoteIndex;
uint8_t noteChartCh2_maxNoteIndex;
uint8_t noteChartCh2_maxProgressionIndex;

void noteCallback_ch0(audio_channel_e audioChannel);
void noteCallback_ch1(audio_channel_e audioChannel);
void noteCallback_ch2(audio_channel_e audioChannel);

void game_logic_init(void) {}

void game_logic_loop(void)
{
    stdio_init_all();
    noteChartCh0_maxNoteIndex = sizeof(noteChartCh0) / sizeof(noteChartCh0[0]);
    noteChartCh1_maxNoteIndex = sizeof(noteChartCh1) / sizeof(noteChartCh1[0]);
    noteChartCh2_maxNoteIndex = sizeof(noteChartCh2_progression0) / sizeof(noteChartCh2_progression0[0]);
    noteChartCh2_maxProgressionIndex = sizeof(noteChartCh2_progressions) / sizeof(noteChartCh2_progressions[0]);

    pwmNote_initNote(   audio_channel_0, audio_instrument_SILENCE,
                        audio_note_A, audio_octave_4,
                        audio_volume_0, audio_volume_0,
                        1000u, noteCallback_ch0);
    pwmNote_initNote(   audio_channel_1, audio_instrument_SILENCE,
                        audio_note_A, audio_octave_4,
                        audio_volume_0, audio_volume_0,
                        1000u, noteCallback_ch1);
    pwmNote_initNote(   audio_channel_2, audio_instrument_SILENCE,
                        audio_note_A, audio_octave_4,
                        audio_volume_0, audio_volume_0,
                        1000u, noteCallback_ch2);
    pwmNote_playChannels(audio_MASK_CHANNEL_2 | audio_MASK_CHANNEL_1 | audio_MASK_CHANNEL_0);

    while (true) {

    }
}

void noteCallback_ch0(audio_channel_e audioChannel)
{
    static uint8_t noteIndex = 0u;
    pwmNote_initNote(   audioChannel, noteChartCh0[noteIndex].instrument,
                        noteChartCh0[noteIndex].note, noteChartCh0[noteIndex].octave,
                        noteChartCh0[noteIndex].volume, noteChartCh0[noteIndex].volume,
                        noteChartCh0[noteIndex].duration, noteCallback_ch0);
    noteIndex++;
    if(noteChartCh0_maxNoteIndex <= noteIndex)
    {
        noteIndex = 0u;
    }
}

void noteCallback_ch1(audio_channel_e audioChannel)
{
    static uint8_t noteIndex = 0u;
    pwmNote_initNote(   audioChannel, noteChartCh1[noteIndex].instrument,
                        noteChartCh1[noteIndex].note, noteChartCh1[noteIndex].octave,
                        noteChartCh1[noteIndex].volume, noteChartCh1[noteIndex].volume,
                        noteChartCh1[noteIndex].duration, noteCallback_ch1);
    noteIndex++;
    if(noteChartCh1_maxNoteIndex <= noteIndex)
    {
        noteIndex = 0u;
    }
}

void noteCallback_ch2(audio_channel_e audioChannel)
{
    static uint8_t noteIndex = 0u;
    static uint8_t progressionIndex = 0u;
    static noteDetails* progressionNoteChart = noteChartCh2_progression0;

    pwmNote_initNote(   audioChannel, progressionNoteChart[noteIndex].instrument,
                        progressionNoteChart[noteIndex].note, progressionNoteChart[noteIndex].octave,
                        progressionNoteChart[noteIndex].volume, progressionNoteChart[noteIndex].volume,
                        progressionNoteChart[noteIndex].duration, noteCallback_ch2);
    noteIndex++;
    if(noteChartCh2_maxNoteIndex <= noteIndex)
    {
        progressionIndex++;
        if(noteChartCh2_maxProgressionIndex <= progressionIndex)
    {
            progressionIndex = 0u;
        }
        switch(progressionIndex)
        {
            case 0:
            {
                progressionNoteChart = noteChartCh2_progression0;
                noteChartCh2_maxNoteIndex = sizeof(noteChartCh2_progression0) / sizeof(noteChartCh2_progression0[0]);
            } break;
            case 1:
            {
                progressionNoteChart = noteChartCh2_progression1;
                noteChartCh2_maxNoteIndex = sizeof(noteChartCh2_progression1) / sizeof(noteChartCh2_progression1[0]);
            } break;
            case 2:
            {
                progressionNoteChart = noteChartCh2_progression2;
                noteChartCh2_maxNoteIndex = sizeof(noteChartCh2_progression2) / sizeof(noteChartCh2_progression2[0]);
            } break;
            default:
            {
                progressionNoteChart = noteChartCh2_progression0;
                noteChartCh2_maxNoteIndex = sizeof(noteChartCh2_progression0) / sizeof(noteChartCh2_progression0[0]);
            } break;
        }
        
        noteIndex = 0u;
    }
}