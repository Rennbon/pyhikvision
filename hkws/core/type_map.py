from ctypes import *

# 类型含义 https://docs.microsoft.com/en-us/windows/win32/winprog/windows-data-types#word
h_BOOL = c_bool
h_CHAR = c_char
h_BYTE = c_byte
h_INT = c_int
h_WORD = c_uint16
h_LONG = c_long
h_FLOAT = c_float
h_DWORD = c_ulong  # 64bit:c_ulong    32bit:c_uint32

h_VOID_P = c_void_p
h_HWND = c_void_p  # handle of window
h_CHAR_P = c_ubyte
h_BYTE_P = c_ubyte
