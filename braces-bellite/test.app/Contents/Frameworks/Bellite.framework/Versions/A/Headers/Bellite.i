%module bellite
%{/* Includes the header in the wrapper code */
#include <stdbool.h>
#include "./Bellite.h"
%}

/* Parse the header file to generate wrappers */
%include "./Bellite.h"

