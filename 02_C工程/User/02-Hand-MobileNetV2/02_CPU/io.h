#ifndef __IO_H__
#define __IO_H__

#ifdef __cplusplus
extern "C" {
#endif

#include "stdint.h"

typedef unsigned long long		virtual_addr_t;

static inline uint8_t read8(virtual_addr_t addr)
{
	return( *((volatile uint8_t *)(addr)) );
}

static inline uint16_t read16(virtual_addr_t addr)
{
	return( *((volatile uint16_t *)(addr)) );
}

static inline uint32_t read32(virtual_addr_t addr)
{
	return( *((volatile uint32_t *)(addr)) );
}

static inline uint64_t read64(virtual_addr_t addr)
{
	return( *((volatile uint64_t *)(addr)) );
}

static inline void write8(virtual_addr_t addr, uint8_t value)
{
	*((volatile uint8_t *)(addr)) = value;
}

static inline void write16(virtual_addr_t addr, uint16_t value)
{
	*((volatile uint16_t *)(addr)) = value;
}

static inline void write32(virtual_addr_t addr, uint32_t value)
{
	*((volatile uint32_t *)(addr)) = value;
}

static inline void write64(virtual_addr_t addr, uint64_t value)
{
	*((volatile uint64_t *)(addr)) = value;
}

#ifdef __cplusplus
}
#endif

#endif /* __IO_H__ */
