#ifndef __STRING_H__
#define __STRING_H__

#ifdef __cplusplus
extern "C" {
#endif

#include <spl.h>

void * mymemcpy(void * dest, const void * src, uint64_t len);

#ifdef __cplusplus
}
#endif

#endif /* __STRING_H__ */
