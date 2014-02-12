/* Copyright (C) 2012 Bellite.io */
#pragma once
#include <unistd.h>
#include <objc/objc.h>

typedef id BelliteHost;
typedef id BelliteWin;
typedef id BelliteCtrl;

#if defined(BELLITE_EXPORTS)
    #define BELLITE_API __attribute__((visibility("default")))
#else
    #define BELLITE_API
#endif
