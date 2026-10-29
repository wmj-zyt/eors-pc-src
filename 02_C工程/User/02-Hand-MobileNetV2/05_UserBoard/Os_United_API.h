//======================================================================
//文件名称：Os_United_API.h（RTOS函数通用接口头文件）
//框架提供：苏州大学嵌入式系统与物联网研究所（sumcu.suda.edu.cn）
//更新记录：20241216
//文件内容：宏定义RTOS的通用接口
//======================================================================
#ifndef Os_United_API_H   //防止重复定义
#define Os_United_API_H 


#include "stdint.h"
#include "Os_Self_API.h"

#define thread_block()               //RT中为空

//（1）LiteOS相关宏常数声明===================================================
//优先级，数字越小优先级越高
#define THREAD_PRIO_0                osPriorityRealtime
#define THREAD_PRIO_1                osPriorityHigh
#define THREAD_PRIO_2                osPriorityAboveNormal
#define THREAD_PRIO_3                osPriorityNormal2
#define THREAD_PRIO_4                osPriorityNormal1
#define THREAD_PRIO_5                osPriorityNormal
#define THREAD_PRIO_6                osPriorityBelowNormal2
#define THREAD_PRIO_7                osPriorityBelowNormal1
#define THREAD_PRIO_8                osPriorityBelowNormal
#define THREAD_PRIO_9                osPriorityLow
//事件
#define EVENT_FLAG_AND               1 
#define EVENT_FLAG_OR                2
#define EVENT_FLAG_CLEAR             4
//IPC相关标志
#define IPC_FLAG_FIFO                0
#define IPC_FLAG_PRIO                0
#define IPC_CMD_UNKNOWN              0
#define IPC_CMD_RESET                0
#define WAITING_FOREVER              osWaitForever
#define WAITING_NO                   0
#define EOK                          0


//（2）LiteOS相关函数声明===================================================
#define delay_ms                     osDelay
#define thread_func                  osThreadFunc_t
#define thread_create(n,f,a,s,p,t)   osThreadNew((thread_func )f, NULL, &((osThreadAttr_t){n, 0, NULL, 0, NULL, s, p, 0, 0}))
#define thread_startup               thread_startup_api
#define thread_self                  osThreadGetId
#define thread_suspend               osThreadSuspend
#define thread_block()
//事件
#define event_create(name,flag)      osEventFlagsNew(&((osEventFlagsAttr_t){name, 0, 0, 0}))
#define event_recv                   event_recv_api
#define event_send                   osEventFlagsSet
//信号量
#define sem_create(n,s,f)            osSemaphoreNew(s, s, &((osSemaphoreAttr_t){n}))
#define sem_get_count                osSemaphoreGetCount
#define sem_take                     osSemaphoreAcquire
#define sem_release                  osSemaphoreRelease
//互斥量
#define mutex_create(n,f)            osMutexNew(&((osMutexAttr_t){n}))
#define mutex_take                   osMutexAcquire
#define mutex_release                osMutexRelease
//消息队列
#define mq_create(n,msgS,queS,f)     osMessageQueueNew(queS, msgS, &((osMessageQueueAttr_t){n}))
#define mq_send(q,buff,size)         osMessageQueuePut(q,(void*)buff,0,WAITING_NO)
#define mq_recv(q,buff,size,time)    osMessageQueueGet(q,(void*)buff,0,time)
#define mq_getCount                  osMessageQueueGetCount


//（3）LiteOS源文件相关===================================================
typedef struct LOS_DL_LIST {
    struct LOS_DL_LIST *pstPrev; /**< Current node's pointer to the previous node */
    struct LOS_DL_LIST *pstNext; /**< Current node's pointer to the next node */
} LOS_DL_LIST;

/**
 * @ingroup los_list
 * Structure of a node in a doubly linked list.
 */
typedef struct {
    LOS_DL_LIST sortLinkNode;
    UINT64      responseTime;
} SortLinkList;

/**
 * @ingroup los_task
 * Define the type of the task entry function.
 *
 */
typedef VOID *(*TSK_ENTRY_FUNC)(UINT32 arg);

/**
 * @ingroup los_event
 * Event control structure
 */
typedef struct tagEvent {
    UINT32 uwEventID;        /**< Event mask in the event control block,
                                  indicating the event that has been logically processed. */
    LOS_DL_LIST stEventList; /**< Event control block linked list */
} EVENT_CB_S, *PEVENT_CB_S;

//（4）相关结构体的宏定义===================================================
#define thread_t osThreadId_t
#define sem_t    osSemaphoreId_t
#define mutex_t  osMutexId_t 
#define event_t  osEventFlagsId_t
#define mq_t     osMessageQueueId_t
#define status_t osStatus_t
#define err_t    uint32_t



//（5）相关桥接函数的定义===================================================
//======================================================================
//函数名称：event_recv_api
//函数返回：事件字的标志
//参数说明：event，事件id，
//          set，查询的标记，
//          option，EVENT_FLAG_AND|EVENT_FLAG_OR|EVENT_FLAG_CLEAR
//          timeout，WAITING_FOREVER|WAITING_NO
//          recved，事件字的标志
//功能概要：事件创建的桥接函数，让07文件夹可移植
//内部调用：无
//更改记录：WYH,20250116，消除警告错误
//======================================================================
void event_recv_api(event_t event, uint32_t set, uint8_t option, int32_t timeout, uint32_t *recved);

//======================================================================
//函数名称：thread_startup_api
//函数返回：void
//参数说明：         thread，线程id，
//                  set，查询的标记
//功能概要：线程创建的替代函数，让07文件夹可移植
//内部调用：无
//======================================================================
void thread_startup_api(thread_t thread);

//（6）结构体定义

/**
 * @ingroup los_task
 * Define the task control block structure.
 */
typedef struct {
    VOID                        *stackPointer;      /**< Task stack pointer */
    UINT16                      taskStatus;
    UINT16                      priority;
    INT32                       timeSlice;
    UINT32                      waitTimes;
    SortLinkList                sortList;
    UINT64                      startTime;
    UINT32                      stackSize;          /**< Task stack size */
    UINT32                      topOfStack;         /**< Task stack top */
    UINT32                      taskID;             /**< Task ID */
    TSK_ENTRY_FUNC              entry;              /**< Task entrance function */
    VOID                        *taskSem;           /**< Task-held semaphore */
    VOID                        *taskMux;           /**< Task-held mutex */
    UINT32                      arg;                /**< Parameter */
    CHAR                        *taskName;          /**< Task name */
    LOS_DL_LIST                 pendList;
    LOS_DL_LIST                 timerList;
    EVENT_CB_S                  event;
    UINT32                      eventMask;          /**< Event mask */
    UINT32                      eventMode;          /**< Event mode */
    VOID                        *msg;               /**< Memory allocated to queues */
    INT32                       errorNo;
} tcb_t;


#endif    
