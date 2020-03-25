from ctypes import (
    c_int, c_uint, c_ushort, c_short, c_ubyte, c_void_p, POINTER,
    c_ulonglong, c_longlong
)

# #if (defined(_WIN32)) //windows
#     #define NET_DVR_API  extern "C" __declspec(dllimport)
#     typedef  unsigned __int64   UINT64;
#     typedef  signed   __int64   INT64;
# #elif defined(__linux__) || defined(__APPLE__) //linux
#     #define  BOOL  int
#     typedef  unsigned int       DWORD;
#     typedef  unsigned short     WORD;
#     typedef  unsigned short     USHORT;
#     typedef  short              SHORT;
#     typedef  int                LONG;
#     typedef  unsigned char      BYTE;
#     typedef  unsigned int       UINT;
#     typedef  void*              LPVOID;
#     typedef  void*              HANDLE;
#     typedef  unsigned int*      LPDWORD; 
#     typedef  unsigned long long UINT64;
#     typedef  signed long long   INT64;

# Linux & APPLE define typedef
BOOL = c_int
DWORD = c_uint
WORD = c_ushort
USHORT = c_ushort
SHORT = c_short
LONG = c_int
BYTE = c_ubyte
UINT = c_uint
LPVOID = c_void_p
HANDLE = c_void_p
LPDWORD = POINTER(c_uint)
UINT64 = c_ulonglong
INT64 = c_longlong
