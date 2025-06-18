# Generated Cmake Pico project file

cmake_minimum_required(VERSION 3.13)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Initialise pico_sdk from installed location
# (note this can come from environment, CMake cache etc)

# == DO NOT EDIT THE FOLLOWING LINES for the Raspberry Pi Pico VS Code Extension to work ==
if(WIN32)
    set(USERHOME $ENV{USERPROFILE})
else()
    set(USERHOME $ENV{HOME})
endif()
set(sdkVersion 2.1.0)
set(toolchainVersion 13_3_Rel1)
set(picotoolVersion 2.1.0)
set(picoVscode ${USERHOME}/.pico-sdk/cmake/pico-vscode.cmake)
if (EXISTS ${picoVscode})
    include(${picoVscode})
endif()
# ====================================================================================
set(PICO_BOARD pico CACHE STRING "Board type")

# Pull in Raspberry Pi Pico SDK (must be before project)
include(pico_sdk_import.cmake)

project(pwmNoteExample C CXX ASM)

# Initialise the Raspberry Pi Pico SDK
pico_sdk_init()

# Add more source files to the project.
set(LIBS_DIR ../../libs)
set(SOURCES_LIBS
    ${LIBS_DIR}/audio/wavetable.c
    ${LIBS_DIR}/audio/noise_bit.c
    ${LIBS_DIR}/audio/pwm_note.c
)

# Add executable. Default name is the project name, version 0.1
add_executable( pwmNoteExample pwmNoteExample.c
                ${SOURCES_LIBS}
)


pico_set_program_name(pwmNoteExample "pwmNoteExample")
pico_set_program_version(pwmNoteExample "0.1")

# Modify the below lines to enable/disable output over UART/USB
pico_enable_stdio_uart(pwmNoteExample 1)
pico_enable_stdio_usb(pwmNoteExample 0)

# Add the standard library to the build
target_link_libraries(pwmNoteExample
        pico_stdlib
        hardware_clocks
        hardware_irq
        hardware_pwm)

# Add the standard include files to the build
target_include_directories(pwmNoteExample PRIVATE
        ${CMAKE_CURRENT_LIST_DIR}
        ${LIBS_DIR}
)

pico_add_extra_outputs(pwmNoteExample)

