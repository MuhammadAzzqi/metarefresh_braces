/* Copyright (C) 2012 Bellite.io */
#pragma once
#define WIN32_LEAN_AND_MEAN
#include <windows.h>

typedef HWND BelliteHost;
typedef HWND BelliteWin;
typedef HWND BelliteCtrl;


/* DLL linking */
#if defined(BELLITE_EXPORTS)
    #define BELLITE_API __declspec(dllexport)
#else
    #define BELLITE_API __declspec(dllimport)

    #if defined(BELLITE_EXPLICIT_LINK)
        #pragma comment(user, "Bellite Link Explict")
    #else
        #pragma message("Linking with Bellite library")
        #pragma comment(lib, "Bellite.lib")
    #endif
#endif
