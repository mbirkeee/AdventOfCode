//---------------------------------------------------------------------------
// clsTypes.h
//---------------------------------------------------------------------------
//
//---------------------------------------------------------------------------

#ifndef CLS_TYPES_H
#define CLS_TYPES_H

//---------------------------------------------------------------------------
// Constants
//---------------------------------------------------------------------------

#ifndef NIL
#   define NIL  ( (void *)0 )
#endif /* NIL */

// Conflicts with vxWorks
#ifndef ERROR
#   define ERROR    ( 0 )
#endif

#ifndef OK
#   define OK       ( 1 )
#endif

#undef  FALSE
#define FALSE       ( 0 )

#undef  TRUE
#define TRUE        ( 1 )

#define RUN_MODE_UNKNOWN    (0)
#define RUN_MODE_PRODUCTION (1)
#define RUN_MODE_TEST       (2)
#define RUN_MODE_EXISTING   (3)
//---------------------------------------------------------------------------
// General Types
//---------------------------------------------------------------------------

#undef External
#ifdef __cplusplus
    #define External extern "C"
#else
    #define External extern
#endif // __cplusplus

#define Static              static
#define Register            register
#define Enumerated          enum

typedef void                Void;
typedef void                Void_t;
typedef void               *Void_p;

typedef int                 Ints;
typedef int                 Ints_t;
typedef int                *Ints_p;

typedef unsigned int        Intu;
typedef unsigned int        Intu_t;
typedef unsigned int       *Intu_p;

typedef unsigned char       Int8u;
typedef unsigned char       Int8u_t;
typedef unsigned char      *Int8u_p;

typedef signed char         Int8s;
typedef signed char         Int8s_t;
typedef signed char        *Int8s_p;

typedef char                Char;
typedef char                Char_t;
typedef char               *Char_p;
typedef const char         *CChar_p;

typedef unsigned short      Int16u;
typedef unsigned short      Int16u_t;
typedef unsigned short     *Int16u_p;

typedef signed short        Int16s;
typedef signed short        Int16s_t;
typedef signed short       *Int16s_p;

typedef unsigned int        Int32u;
typedef unsigned int        Int32u_t;
typedef unsigned int       *Int32u_p;

typedef signed int          Int32s;
typedef signed int          Int32s_t;
typedef signed int         *Int32s_p;

typedef unsigned char       Boolean_t;
typedef unsigned char      *Boolean_p;

typedef unsigned long long  Int64u;
typedef unsigned long long  Int64u_t;
typedef unsigned long long *Int64u_p;

typedef signed long long    Int64s;
typedef signed long long    Int64s_t;
typedef signed long long   *Int64s_p;

typedef float               Float_t;
typedef float              *Float_p;

typedef float               Float32_t;
typedef float              *Float32_p;

typedef double              Float64_t;
typedef double             *Float64_p;

#endif // CLS_TYPES_H
