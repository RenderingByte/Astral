# Astral - A VSRG (Vertical Scrolling Rhythm Game) developed in Python3.
# This program can be found on GitHub: https://github.com/RenderingByte/Astral
# This file serves as a way to provide a conventional keymap for the program.

# Imports
import Globals
import pygame.key

# Initialization
pygame.init()

# Keymap Object (read-only)
keymap = {
    "left" : pygame.K_LEFT,
    "right" : pygame.K_RIGHT,
    "up" : pygame.K_UP,
    "down" : pygame.K_DOWN,
    "a" : pygame.K_a,
    "b" : pygame.K_b,
    "c" : pygame.K_c,
    "d" : pygame.K_d,
    "e" : pygame.K_e,
    "f" : pygame.K_f,
    "g" : pygame.K_g,
    "h" : pygame.K_h,
    "i" : pygame.K_i,
    "j" : pygame.K_j,
    "k" : pygame.K_k,
    "l" : pygame.K_l,
    "m" : pygame.K_m,
    "n" : pygame.K_n,
    "o" : pygame.K_o,
    "p" : pygame.K_p,
    "q" : pygame.K_q,
    "r" : pygame.K_r,
    "s" : pygame.K_s,
    "t" : pygame.K_t,
    "u" : pygame.K_u,
    "v" : pygame.K_v,
    "w" : pygame.K_w,
    "x" : pygame.K_x,
    "y" : pygame.K_y,
    "z" : pygame.K_z,
    "0" : pygame.K_0,
    "1" : pygame.K_1,
    "2" : pygame.K_2,
    "3" : pygame.K_3,
    "4" : pygame.K_4,
    "5" : pygame.K_5,
    "6" : pygame.K_6,
    "7" : pygame.K_7,
    "8" : pygame.K_8,
    "9" : pygame.K_9,
    "+" : pygame.K_PLUS,
    "-" : pygame.K_MINUS,
    "." : pygame.K_PERIOD,
    "," : pygame.K_COMMA,
    "/" : pygame.K_SLASH,
    ";" : pygame.K_SEMICOLON,
    "'" : pygame.K_QUOTE,
    "[" : pygame.K_LEFTBRACKET,
    "]" : pygame.K_RIGHTBRACKET,
    " " : pygame.K_SPACE,
    "backspace" : pygame.K_BACKSPACE,
    "tab" : pygame.K_TAB,
    "capslock" : pygame.K_CAPSLOCK,
    "shift" : pygame.K_LSHIFT,
    "ctrl" : pygame.K_LCTRL,
    "alt" : pygame.K_LALT,
    "pause" : pygame.K_PAUSE,
    "insert" : pygame.K_INSERT,
    "home" : pygame.K_HOME,
    "pageup" : pygame.K_PAGEUP,
    "pagedown" : pygame.K_PAGEDOWN,
    "end" : pygame.K_END,
    "del" : pygame.K_DELETE,
    "menu" : pygame.K_MENU,
    "numlock" : pygame.K_NUMLOCK,
    "scrolllock" : pygame.K_SCROLLOCK,
    "printscreen" : pygame.K_PRINT,
    "f1" : pygame.K_F1,
    "f2" : pygame.K_F2,
    "f3" : pygame.K_F3,
    "f4" : pygame.K_F4,
    "f5" : pygame.K_F5,
    "f6" : pygame.K_F6,
    "f7" : pygame.K_F7,
    "f8" : pygame.K_F8,
    "f9" : pygame.K_F9,
    "f10" : pygame.K_F10,
    "f11" : pygame.K_F11,
    "f12" : pygame.K_F12,
}

def GetKey(key):
    """
        Looks up a given character in the keymap and returns the corresponding object.
        That object will be in a Pygame Key object format. (e.g. pygame.K_a)
        
        ';' will return pygame.K_SEMICOLON.
        
        Mainly used for setting keybinds.

    """
    
    if key in keymap: return keymap[key]
    
    else:
        
        print("\033[91mSorry, but your key: '", key, "' is currently not an available keybind. Please choose something else!")
        Globals.program.isRunning = False