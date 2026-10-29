//======================================================================
//文件名称：Os_Self_API.h（RTOS函数自身接口头文件）
//框架提供：苏州大学嵌入式系统与物联网研究所（sumcu.suda.edu.cn）
//更新记录：20241216
//文件内容：（1）BIOS内驻留的RTOS函数名映射宏定义（即通过这个函数名可以
//              使用BIOS中的RTOS内核函数）
//          （2）RTOS的结构体类型
//例如：这里给出了rt_event_create的宏定义，可以通过它调用BIOS中该函数
//======================================================================
#ifndef Os_Self_API_H   //防止重复定义
#define Os_Self_API_H

#include "gec.h"
//（2）LiteOS相关函数声明===================================================

#define OS_start  ((void (*)(void (*func)(void)))(component_fun[34]))
#define osThreadNew  ((osThreadId_t (*)(osThreadFunc_t func, void *argument, const osThreadAttr_t *attr))(component_fun[35]))
#define osDelay  ((osStatus_t (*)(uint32_t millisec))(component_fun[36]))
#define osThreadGetId ((osThreadId_t (*)(void))(component_fun[37]))
#define osThreadSuspend ((uint32_t (*)(osThreadId_t thread_id))(component_fun[38]))
//事件
#define osEventFlagsNew  ((osEventFlagsId_t (*)(const osEventFlagsAttr_t *attr))(component_fun[41]))
#define osEventFlagsWait  ((uint32_t (*)(osEventFlagsId_t ef_id, uint32_t flags, uint32_t options, uint32_t timeout))(component_fun[42]))
#define osEventFlagsSet  ((uint32_t (*)(osEventFlagsId_t ef_id, uint32_t flags))(component_fun[43]))

//信号量
#define osSemaphoreNew  ((osSemaphoreId_t (*)(uint32_t max_count, uint32_t initial_count, const osSemaphoreAttr_t *attr))(component_fun[46]))
#define osSemaphoreAcquire  ((osStatus_t (*)(osSemaphoreId_t semaphore_id, uint32_t timeout))(component_fun[47]))
#define osSemaphoreRelease  ((osStatus_t (*)(osSemaphoreId_t semaphore_id))(component_fun[48]))
#define osSemaphoreGetCount  ((uint32_t (*)(osSemaphoreId_t semaphore_id))(component_fun[49]))
//互斥量
#define osMutexNew  ((osMutexId_t (*)(const osMutexAttr_t *attr))(component_fun[52]))
#define osMutexAcquire ((osStatus_t (*)(osMutexId_t mutex_id, uint32_t timeout))(component_fun[53]))
#define osMutexRelease  ((osStatus_t (*)(osMutexId_t mutex_id))(component_fun[54]))
//消息队列
#define osMessageQueueNew  ((osMessageQueueId_t (*)(uint32_t msg_count, uint32_t msg_size, const osMessageQueueAttr_t *attr))(component_fun[58]))
#define osMessageQueuePut  ((osStatus_t (*)(osMessageQueueId_t mq_id, const void *msg_ptr, uint8_t msg_prio, uint32_t timeout))(component_fun[59]))
#define osMessageQueueGet  ((osStatus_t (*)(osMessageQueueId_t mq_id, void *msg_ptr, uint8_t *msg_prio, uint32_t timeout))(component_fun[60]))
#define osMessageQueueGetCount ((uint32_t (*)(osMessageQueueId_t mq_id))(component_fun[61]))


//（3）LiteOS源文件相关

/* type definitions */
#ifndef UINT8
typedef unsigned char          UINT8;
#endif
#ifndef UINT16
typedef unsigned short         UINT16;
#endif
#ifndef UINT32
typedef unsigned int           UINT32;
#endif
#ifndef INT8
typedef signed char            INT8;
#endif
#ifndef INT16
typedef signed short           INT16;
#endif
#ifndef INT32
typedef signed int             INT32;
#endif
#ifndef FLOAT
typedef float                  FLOAT;
#endif
#ifndef DOUBLE
typedef double                 DOUBLE;
#endif
#ifndef CHAR
typedef char                   CHAR;
#endif

#ifndef BOOL
typedef unsigned int           BOOL;
#endif
#ifndef UINT64
typedef unsigned long long     UINT64;
#endif
#ifndef INT64
typedef signed long long       INT64;
#endif
#ifndef UINTPTR
typedef unsigned int           UINTPTR;
#endif
#ifndef INTPTR
typedef signed int             INTPTR;
#endif

#ifndef  VOID
#define VOID          void
#endif

#ifndef LOS_OK
#define LOS_OK        0U
#endif



// Timeout value.
#define osWaitForever         0xFFFFFFFFU ///< Wait forever timeout value.
// Flags options (\ref osThreadFlagsWait and \ref osEventFlagsWait).
#define osFlagsWaitAny        0x00000000U ///< Wait for any flag (default).
#define osFlagsWaitAll        0x00000001U ///< Wait for all flags.
#define osFlagsNoClear        0x00000002U ///< Do not clear flags which have been specified to wait for.
 
// Flags errors (returned by osThreadFlagsXxxx and osEventFlagsXxxx).
#define osFlagsError          0x80000000U ///< Error indicator.
#define osFlagsErrorUnknown   0xFFFFFFFFU ///< osError (-1).
#define osFlagsErrorTimeout   0xFFFFFFFEU ///< osErrorTimeout (-2).
#define osFlagsErrorResource  0xFFFFFFFDU ///< osErrorResource (-3).
#define osFlagsErrorParameter 0xFFFFFFFCU ///< osErrorParameter (-4).
#define osFlagsErrorISR       0xFFFFFFFAU ///< osErrorISR (-6).
 
// Thread attributes (attr_bits in \ref osThreadAttr_t).
#define osThreadDetached      0x00000000U ///< Thread created in detached mode (default)
#define osThreadJoinable      0x00000001U ///< Thread created in joinable mode
 
// Mutex attributes (attr_bits in \ref osMutexAttr_t).
#define osMutexRecursive      0x00000001U ///< Recursive mutex.
#define osMutexPrioInherit    0x00000002U ///< Priority inherit protocol.
#define osMutexRobust         0x00000008U ///< Robust mutex.


/// Entry point of a thread.
typedef void(*osThreadFunc_t)(void *argument);
typedef void(* osTimerFunc_t)(void *argument);
/// \details Thread ID identifies the thread.
typedef void * osThreadId_t;
typedef void * osTimerId_t;
/// \details Event Flags ID identifies the event flags.
typedef void * osEventFlagsId_t;
/// \details Mutex ID identifies the mutex.
typedef void * osMutexId_t;
 /// \details Semaphore ID identifies the semaphore.
typedef void * osSemaphoreId_t;
typedef void * osMemoryPoolId_t;
/// \details Message Queue ID identifies the message queue.
typedef void * osMessageQueueId_t;
typedef uint32_t 	TZ_ModuleId_t;

 
typedef enum {
  osKernelInactive = 0,
  osKernelReady = 1,
  osKernelRunning = 2,
  osKernelLocked = 3,
  osKernelSuspended = 4,
  osKernelError = -1,
  osKernelReserved = 0x7FFFFFFFU
}osKernelState_t;

typedef enum {
  osThreadInactive = 0,
  osThreadReady = 1,
  osThreadRunning = 2,
  osThreadBlocked = 3,
  osThreadTerminated = 4,
  osThreadError = -1,
  osThreadReserved = 0x7FFFFFFF
}osThreadState_t;

/// Priority values.
typedef enum {
  osPriorityNone          =  0,         ///< No priority (not initialized).
  osPriorityIdle          =  1,         ///< Reserved for Idle thread.
  osPriorityLow           =  8,         ///< Priority: low
  osPriorityLow1          =  8+1,       ///< Priority: low + 1
  osPriorityLow2          =  8+2,       ///< Priority: low + 2
  osPriorityLow3          =  8+3,       ///< Priority: low + 3
  osPriorityLow4          =  8+4,       ///< Priority: low + 4
  osPriorityLow5          =  8+5,       ///< Priority: low + 5
  osPriorityLow6          =  8+6,       ///< Priority: low + 6
  osPriorityLow7          =  8+7,       ///< Priority: low + 7
  osPriorityBelowNormal   = 16,         ///< Priority: below normal
  osPriorityBelowNormal1  = 16+1,       ///< Priority: below normal + 1
  osPriorityBelowNormal2  = 16+2,       ///< Priority: below normal + 2
  osPriorityBelowNormal3  = 16+3,       ///< Priority: below normal + 3
  osPriorityBelowNormal4  = 16+4,       ///< Priority: below normal + 4
  osPriorityBelowNormal5  = 16+5,       ///< Priority: below normal + 5
  osPriorityBelowNormal6  = 16+6,       ///< Priority: below normal + 6
  osPriorityBelowNormal7  = 16+7,       ///< Priority: below normal + 7
  osPriorityNormal        = 24,         ///< Priority: normal
  osPriorityNormal1       = 24+1,       ///< Priority: normal + 1
  osPriorityNormal2       = 24+2,       ///< Priority: normal + 2
  osPriorityNormal3       = 24+3,       ///< Priority: normal + 3
  osPriorityNormal4       = 24+4,       ///< Priority: normal + 4
  osPriorityNormal5       = 24+5,       ///< Priority: normal + 5
  osPriorityNormal6       = 24+6,       ///< Priority: normal + 6
  osPriorityNormal7       = 24+7,       ///< Priority: normal + 7
  osPriorityAboveNormal   = 32,         ///< Priority: above normal
  osPriorityAboveNormal1  = 32+1,       ///< Priority: above normal + 1
  osPriorityAboveNormal2  = 32+2,       ///< Priority: above normal + 2
  osPriorityAboveNormal3  = 32+3,       ///< Priority: above normal + 3
  osPriorityAboveNormal4  = 32+4,       ///< Priority: above normal + 4
  osPriorityAboveNormal5  = 32+5,       ///< Priority: above normal + 5
  osPriorityAboveNormal6  = 32+6,       ///< Priority: above normal + 6
  osPriorityAboveNormal7  = 32+7,       ///< Priority: above normal + 7
  osPriorityHigh          = 40,         ///< Priority: high
  osPriorityHigh1         = 40+1,       ///< Priority: high + 1
  osPriorityHigh2         = 40+2,       ///< Priority: high + 2
  osPriorityHigh3         = 40+3,       ///< Priority: high + 3
  osPriorityHigh4         = 40+4,       ///< Priority: high + 4
  osPriorityHigh5         = 40+5,       ///< Priority: high + 5
  osPriorityHigh6         = 40+6,       ///< Priority: high + 6
  osPriorityHigh7         = 40+7,       ///< Priority: high + 7
  osPriorityRealtime      = 48,         ///< Priority: realtime
  osPriorityRealtime1     = 48+1,       ///< Priority: realtime + 1
  osPriorityRealtime2     = 48+2,       ///< Priority: realtime + 2
  osPriorityRealtime3     = 48+3,       ///< Priority: realtime + 3
  osPriorityRealtime4     = 48+4,       ///< Priority: realtime + 4
  osPriorityRealtime5     = 48+5,       ///< Priority: realtime + 5
  osPriorityRealtime6     = 48+6,       ///< Priority: realtime + 6
  osPriorityRealtime7     = 48+7,       ///< Priority: realtime + 7
  osPriorityISR           = 56,         ///< Reserved for ISR deferred thread.
  osPriorityError         = -1,         ///< System cannot determine priority or illegal priority.
  osPriorityReserved      = 0x7FFFFFFF  ///< Prevents enum down-size compiler optimization.
} osPriority_t;

typedef enum {
  osTimerOnce = 0,
  osTimerPeriodic = 1
}osTimerType_t;

/// Status code values returned by CMSIS-RTOS functions.
typedef enum {
  osOK                      =  0,         ///< Operation completed successfully.
  osError                   = -1,         ///< Unspecified RTOS error: run-time error but no other error message fits.
  osErrorTimeout            = -2,         ///< Operation not completed within the timeout period.
  osErrorResource           = -3,         ///< Resource not available.
  osErrorParameter          = -4,         ///< Parameter error.
  osErrorNoMemory           = -5,         ///< System is out of memory: it was impossible to allocate or reserve memory for the operation.
  osErrorISR                = -6,         ///< Not allowed in ISR context: the function cannot be called from interrupt service routines.
  osStatusReserved          = 0x7FFFFFFF  ///< Prevents enum down-size compiler optimization.
} osStatus_t;


#ifndef TZ_MODULEID_T
#define TZ_MODULEID_T
///  Data type that identifies secure software modules called by a process.
typedef uint32_t TZ_ModuleId_t;
#endif

typedef struct {
  uint32_t api;                         ///< API version (major.minor.rev: mmnnnrrrr dec).
  uint32_t kernel;                      ///< Kernel version (major.minor.rev: mmnnnrrrr dec).
} osVersion_t;

typedef struct {
  const char                   *name;   ///< name of the thread
  uint32_t                 attr_bits;   ///< attribute bits
  void                      *cb_mem;    ///< memory for control block
  uint32_t                   cb_size;   ///< size of provided memory for control block
  void                   *stack_mem;    ///< memory for stack
  uint32_t                stack_size;   ///< size of stack
  osPriority_t              priority;   ///< initial thread priority (default: osPriorityNormal)
  TZ_ModuleId_t            tz_module;   ///< TrustZone module identifier
  uint32_t                  reserved;   ///< reserved (must be 0)
} osThreadAttr_t;

typedef struct {
  const char* name;                     ///< name of the timer
  uint32_t attr_bits;                   ///< attribute bits
  void* cb_mem;                         ///< memory for control block
  uint32_t cb_size;                     ///< size of provided memory for control block
} osTimerAttr_t;

/// Attributes structure for event flags.
typedef struct {
  const char                   *name;   ///< name of the event flags
  uint32_t                 attr_bits;   ///< attribute bits
  void                      *cb_mem;    ///< memory for control block
  uint32_t                   cb_size;   ///< size of provided memory for control block
} osEventFlagsAttr_t;

/// Attributes structure for mutex.
typedef struct {
  const char                   *name;   ///< name of the mutex
  uint32_t                 attr_bits;   ///< attribute bits
  void                      *cb_mem;    ///< memory for control block
  uint32_t                   cb_size;   ///< size of provided memory for control block
} osMutexAttr_t;
 
/// Attributes structure for semaphore.
typedef struct {
  const char                   *name;   ///< name of the semaphore
  uint32_t                 attr_bits;   ///< attribute bits
  void                      *cb_mem;    ///< memory for control block
  uint32_t                   cb_size;   ///< size of provided memory for control block
} osSemaphoreAttr_t;

typedef struct{
  const char* name;
  uint32_t attr_bits;
  void* cb_mem;
  uint32_t cb_size;
  void* mp_mem;
  uint32_t mp_size;
}osMemoryPoolAttr_t;

/// Attributes structure for message queue.
typedef struct {
  const char                   *name;   ///< name of the message queue
  uint32_t                 attr_bits;   ///< attribute bits
  void                      *cb_mem;    ///< memory for control block
  uint32_t                   cb_size;   ///< size of provided memory for control block
  void                      *mq_mem;    ///< memory for data storage
  uint32_t                   mq_size;   ///< size of provided memory for data storage 
} osMessageQueueAttr_t;


#endif    
