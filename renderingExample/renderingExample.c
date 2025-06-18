#include "renderingExample.h"

#include "display/display_api.h"
#include "system_manager/global_system_variables.h"
#include "pico/util/queue.h"

uint32_t frameCount = 0;

void game_logic_init(void)
{
    // Initialize the PicoPanda board
    // This function is called once at the start of the program
    // Add any necessary initialization code here

}


void game_logic_loop(void)
{
    // Main loop of the PicoPanda program
    // This function is called repeatedly after initialization
    // Add your main program logic here

    if(frameCount < 10)
    {
        display_api_draw_sprite(&test_128x128[0], PIXELS_32x32, 0, 32, 32, 2, 2, false, false);

        display_api_draw_line(0, 0, 127, 127, 0x0F);

        display_api_draw_circle(63, 63, 15, false, 0x0F);

        display_api_draw_rectangle(0, 0, 10, 10, false, 0x0F);

        if(true == button_input_status.up)
        {
            frameCount++;
        }
    } 
    else if(frameCount < 20) 
    {
        //display_api_draw_sprite(&test_128x128[0], PIXELS_32x32, 0, 32, 32, 2, 2, true, true);

        // display_api_draw_line(0, 0, 127, 61, 0x08);
        // display_api_draw_line(0, 1, 127, 62, 0x08);
        // display_api_draw_line(0, 2, 127, 63, 0x08);
        // display_api_draw_string(0, 6, "Hello World!", FONT_SIZE_ORG_01, 0x0F);
        display_api_draw_string(0, 10, "My Name is Tom", FONT_4X5_FIXED, 1, 0x0F);
        display_api_draw_string(0, 20, "My Name is Tom", FONT_4X5_FIXED, 1, 0x0F);
        display_api_draw_string(0, 30, "PICOPANDA", FONT_4X5_FIXED, 2, 0x0F);
        display_api_draw_string(0, 50, "Waar bly jy?", FONT_4X5_FIXED, 2, 0x0F);
        display_api_draw_string(0, 60, "Eerste keer in die stad?", FONT_4X5_FIXED, 1, 0x0F);
        display_api_draw_string(0, 80, "JY BLY STIL!", FONT_4X5_FIXED, 2, 0x0F);
        display_api_draw_string(0, 120, "!! CHAMP !!", FONT_4X5_FIXED, 3, 0x0F);
        // display_api_draw_string(0, 21, "PICOPANDA", FONT_SIZE_PICOPIXEL, 0x0F);
        // display_api_draw_string(0, 30, "PICOPANDA", FONT_SIZE_5X7_FIXED, 0x0F);

        // display_api_draw_string(0, 60, "PICOPANDA", FONT_SIZE_9PT, 0x0F);
        // display_api_draw_string(0, 90, "PICOPANDA", FONT_SIZE_FREE_SERIF_9PT_7B, 0x0F);
        // display_api_draw_circle(63, 63, 15, true, 0x0F);

        // display_api_draw_rectangle(0, 0, 10, 10, true, 0x0F);

        if(true == button_input_status.up)
        {
            frameCount++;
        }

        if(frameCount >= 20)
        {
            frameCount = 0;
        } 
    }
}