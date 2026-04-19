---
layout: page
title: API reference
permalink: /api/
---

This page describes the **PicoPanda** Lua game API: types, constants, drawing and map helpers, audio phrases, and the lifecycle callbacks your cart defines.

Coordinates use the **128×128** screen unless noted otherwise. Color **values** are **4-bit** (0–15): `0` is darkest, `15` is lightest on the handheld display.

---

## Types

### ButtonStatus

Returned by `get_button_status()`. Each `*_pressed` field is true only for the frame when that button **newly** went down.

| Field | Type | Meaning |
|--------|------|--------|
| `up`, `down`, `left`, `right` | boolean | Held this frame |
| `start`, `select` | boolean | Held this frame |
| `a`, `b` | boolean | Held this frame |
| `up_pressed`, … `b_pressed` | boolean | Pressed **this** frame (edge) |

### SpriteSize

Constants used with `draw_sprite` for how sprites are laid out in the sheet:

| Constant | Value | Use |
|----------|------|-----|
| `PIXELS_8x8` | `8` | 8×8 sprites |
| `PIXELS_16x16` | `16` | 16×16 sprites |
| `PIXELS_32x32` | `32` | 32×32 sprites |

---

## Constants

### Sprite sheet layout

```lua
PIXELS_8x8 = 8
PIXELS_16x16 = 16
PIXELS_32x32 = 32
```

### Font indices (draw_string)

| Name | Value |
|------|--------|
| `FONT_ORG_01` | `0` |
| `FONT_FREE_MONO_9PT_7B` | `1` |
| `FONT_PICOPIXEL` | `2` |
| `FONT_5X7_FIXED` | `3` |
| `FONT_FREE_SERIF_9PT_7B` | `4` |
| `FONT_4X5_FIXED` | `5` |

The API stub uses **font index `5`** as a common default in examples.

---

## Input

### get_button_status()

Returns a **`ButtonStatus`** table: current holds plus one-frame “pressed” edges for every face button.

---

## Drawing

### draw_pixel(x, y, value)

| Parameter | Description |
|-----------|-------------|
| `x`, `y` | Pixel coordinates **0–127** |
| `value` | Grey **0–15** |

### draw_sprite(sprite_size, index, coord_x, coord_y, width, height, flip_x, flip_y)

Blits from the sprite sheet.

| Parameter | Description |
|-----------|-------------|
| `sprite_size` | `PIXELS_8x8`, `PIXELS_16x16`, or `PIXELS_32x32` |
| `index` | Sprite index in the sheet |
| `coord_x`, `coord_y` | Destination (screen space; camera applies) |
| `width`, `height` | Size to draw in **pixels** |
| `flip_x`, `flip_y` | Horizontal / vertical flip |

### draw_line(x1, y1, x2, y2, value)

Line from (`x1`,`y1`) to (`x2`,`y2`) in grey **0–15**.

### draw_circle(x_center, y_center, radius, filled, value)

Circle at center with given **radius**; **`filled`** selects solid vs outline; **`value`** is **0–15**.

### draw_rectangle(x1, y1, width, height, filled, value)

Axis-aligned rectangle with top-left (`x1`,`y1`), size `width`×`height`; **`filled`** solid or outline; **`value`** **0–15**.

### draw_string(x, y, str, font_index, scale_factor, value)

Draws **`str`** at (`x`,`y`) using **`font_index`** (see font constants), **`scale_factor`** scale, and grey **`value`** **0–15**.

---

## Map and camera

### draw_map(celx, cely, sx, sy, celw, celh, layer)

Draws a region of the tile map using the sprite sheet and sprite flags.

| Parameter | Description |
|-----------|-------------|
| `celx`, `cely` | Map cell for the **upper-left** corner (column / row; `0` = top or left) |
| `sx`, `sy` | Screen position for that corner |
| `celw`, `celh` | Region size in **cells** |
| `layer` | Optional. If set, only tiles whose flags include **every** bit in this mask are drawn. Default **`0`** draws all. |

### get_map_sprite_index(celx, cely)

Returns the **sprite index** (0–255) stored in cell (`celx`,`cely`), or **`255`** if out of bounds.

### get_sprite_flags(n, f)

| Parameter | Description |
|-----------|-------------|
| `n` | Sprite index **0–255** |
| `f` | Optional. **`0`** or omitted: return the full **flag byte**. **`1`–`8`**: return **`1`** if that flag bit is set, else **`0`**. |

### set_camera_offset(x, y)

Subtracts (`x`,`y`) from subsequent draw calls (scroll / camera).

### get_camera_offset()

Returns **two numbers**: current camera **`x`** and **`y`** offsets.

---

## Audio (phrases)

### phrase_play(index, channel)

Starts playback for a phrase.

| Parameter | Description |
|-----------|-------------|
| `index` | Phrase index to play |
| `channel` | Channel to use; if **omitted** or **negative**, the engine may pick a free channel |

### phrase_stop(index, channel)

Stops phrase playback.

| Parameter | Description |
|-----------|-------------|
| `index` | Phrase to stop; if **negative**, phrase index may be ignored and only channels are affected |
| `channel` | Channel to clear; if **omitted** or **negative**, **all** channels may be stopped |

*(Exact behaviour matches your firmware build; the stub file uses these names for tooling and autocomplete.)*

---

## Game lifecycle (you implement these)

### game_logic_init()

Called **once** when the cart starts. Set up state, load defaults, etc.

### game_logic_loop()

Called **every frame** at **60 FPS**. Read input, update simulation, and issue draw calls here.

---

## Example loop

```lua
function game_logic_init()
    player_x = 64
    player_y = 64
end

function game_logic_loop()
    local buttons = get_button_status()

    if buttons.left then
        player_x = player_x - 1
    end
    if buttons.right then
        player_x = player_x + 1
    end

    draw_rectangle(0, 0, 128, 128, true, 0x00)
    draw_sprite(PIXELS_16x16, 0, player_x, player_y, 16, 16, false, false)
    draw_string(0, 0, "Score: 100", 5, 1, 0x0F)
end
```

Use **`get_button_status()`** each frame for input, **`draw_rectangle`** to clear or fill the framebuffer, **`draw_sprite`** / **`draw_string`** for visuals, and keep **`game_logic_loop`** bounded so you stay near **60 FPS**.
