#include <spl.h>

extern unsigned char __image_start[];
extern unsigned char __image_end[];
extern void sys_spi_init(void);
extern void sys_spi_exit(void);
extern void sys_spinor_read(int addr, void * buf, int count);
extern void sys_spinand_read(int addr, void * buf, int count);

int get_boot_device(void)
{
	uint8_t s = *((volatile uint8_t *)(0x00020000 + 0x28));

	if(s == 0x3)
		return 1; //SPINOR
	else if(s == 0x4)
		return 2; //SPINAND
	else if(s == 0x0)
		return 3;  //SDCARD
	return 1;      //SPINOR
}

void sys_copyself(void)
{
	int d = get_boot_device();
	void * mem = (void *)__image_start;
	uint32_t size = __image_end - __image_start;
	if(d == 1)
	{
		sys_spi_init();
		sys_spinor_read(0, mem, size);
		sys_spi_exit();
	}
	else if(d == 2)
	{
		sys_spi_init();
		sys_spinand_read(0, mem, size);
		sys_spi_exit();
	}
	else if(d == 3)
	{
	}
}
