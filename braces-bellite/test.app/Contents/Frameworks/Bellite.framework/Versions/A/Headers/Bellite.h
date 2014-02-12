/*
 * Bellite is a library for creating desktop applications on Mac OSX and Windows
 * using HTML5 platform technologies. Learn more at http://bellite.io
 *
 * Copyright (C) 2012 Bellite.io
 */
#pragma once

#if defined(SWIG)

#elif defined(_WIN32)
#include "_Bellite_Plat_Win32.h"

#elif defined(__APPLE__)
#include "_Bellite_Plat_Cocoa.h"
#endif

#ifndef BELLITE_API
#define BELLITE_API
typedef void* BelliteHost;
typedef void* BelliteWin;
typedef void* BelliteCtrl;
#endif

#ifndef JSON
#define JSON(...) "{" #__VA_ARGS__ "}"
#define JSON_OBJ(...) "{" #__VA_ARGS__ "}"
#define JSON_LIST(...) "[" #__VA_ARGS__ "]"
#endif

#if defined(__cplusplus)
extern "C" {
#endif

typedef int BelliteId;
typedef int intbool; /* an int sized boolean, for simple wrappers */
typedef const char* jsonstr; /* utf-8 encoded json source */

/* The JSON based command API */
BELLITE_API intbool     bellite_respondsTo(BelliteId selfId, const char* cmd);
BELLITE_API jsonstr     bellite_perform(BelliteId selfId, const char* cmd, jsonstr args);
BELLITE_API jsonstr     bellite_getErrors(BelliteId selfId, intbool clearErrors);

typedef int (*BelliteFn)(BelliteId selfId, const char* evtType, jsonstr evt, void* ctx);
BELLITE_API intbool     bellite_bindEvent(BelliteId selfId, const char* evtType, BelliteFn fnEvent, void* ctx);
BELLITE_API intbool     bellite_unbindEvent(BelliteId selfId, const char* evtType, BelliteFn fnEvent, void* ctx);

BELLITE_API intbool     bellite_isInstalled();
BELLITE_API intbool     bellite_requireInstall(jsonstr options);

/* The C API is available from both C and the JSON based command API */
BELLITE_API intbool     bellite_initApp(jsonstr options);
BELLITE_API intbool     bellite_msgLoop(intbool block, int yieldAfter);
BELLITE_API intbool     bellite_msgPending(); 
BELLITE_API intbool     bellite_msgRun();

BELLITE_API BelliteId   bellite_create(jsonstr options);
BELLITE_API BelliteId   bellite_navigateNew(const char* url, jsonstr options);
BELLITE_API BelliteId   bellite_navigate(BelliteId selfId, const char* url, jsonstr options);

/* Platform-tailored API not available from the JSON based API, including platform window and controll handles */
BELLITE_API BelliteId   bellite_createEx(BelliteHost host, jsonstr options);
BELLITE_API BelliteWin  bellite_window(BelliteId selfId);
BELLITE_API BelliteCtrl bellite_webview(BelliteId selfId);

/* Out-of-process application architecture */
BELLITE_API jsonstr     bellite_server(jsonstr options);
BELLITE_API int         bellite_subprocess(jsonstr options);
BELLITE_API intbool     bellite_killprocess(int pid, const char* signal_name);

#undef BELLITE_API
#if defined(__cplusplus)
} /* extern "C" */
#endif
