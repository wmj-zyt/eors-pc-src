OUTPUT_FORMAT("elf64-littleriscv", "elf64-littleriscv", "elf64-littleriscv")
OUTPUT_ARCH(riscv)
ENTRY(start)


/* D1-H的程序是首先下载到flash中，然后在运行时拷贝到RAM中运行（DDR），
   FLASH的起始地址为：0x00000000
   总大小为256MB，结束地址为0x10000000
   RAM的起始地址为：0x40000000
   总大小为：256MB，结束地址为：0x10000000
   程序的存储按顺序存储，不再模拟划分RAM和FLASH
*/
MCU_SECTORSIZE = 2048;
MCU_DDR_ADDR_START = 0x40000000;     /* DDR的起始地址 */
/*User程序开始扇区号与结束扇区号*/
GEC_USER_SECTOR_START  =32768;       
GEC_USER_SECTOR_END =131072;   

MEMORY
{
	RAM(rx) : org = MCU_DDR_ADDR_START + MCU_SECTORSIZE * GEC_USER_SECTOR_START,       /*0x4400 0000*/
	          len = MCU_SECTORSIZE * (GEC_USER_SECTOR_END - GEC_USER_SECTOR_START + 1) /*0x0C00 0000*/
}

SECTIONS
{
	/* 程序代码段 */
	.text :
	{
		/* 提供符号以供启动文件start.S使用，以下PROVIDE同理 */
		PROVIDE(__image_start = .);
		PROVIDE(__text_start = .);
		PROVIDE(__spl_start = .);
		/* 代码段 */
		obj/start.o (.text*)
		obj/mymemcpy.o (.text*)
		obj/spl_uart.o (.text*)
		obj/spl_clock.o (.text*)
		obj/spl_dram.o (.text*)
		obj/spl_spiflash.o (.text*)
		obj/spl_copyself.o (.text*)
		. = ALIGN(8);
		PROVIDE(__ddr_bin_start = .);
		KEEP(*(.ddr.bin))
		PROVIDE(__ddr_bin_end = .);
		PROVIDE(__spl_end = .);
		*(.text*)
		*(.iplt)
		*(.note.gnu.build-id)
		PROVIDE(__text_end = .);
	} > RAM

	/* SPL拷贝程序大小 */	
	PROVIDE(__spl_size = __spl_end - __spl_start);

	/* 只读区，存放常量和字符串字面量 */
	.rodata ALIGN(8) :
	{
		PROVIDE(__rodata_start = .);
		*(.rodata*)
		*(.srodata*)
		PROVIDE(__rodata_end = .);
	} > RAM

	/* 数据段，存放已初始化的全局变量和静态变量 */
	.data ALIGN(8) :
	{
		PROVIDE(__data_start = .);
		/* 为全局指针GP提供定义符号，因为GP的寻址范围是+-2KB范围，所以地址+0x800 */
		PROVIDE(__global_pointer$ = . + 0x800);
		*(.sdata*)
		*(.data*)
		. = ALIGN(8);
  		PROVIDE(__data_end = .);
		PROVIDE(__image_end = .);
		PROVIDE( _edata = .);
	} > RAM
	/* 用户代码大小 */
	PROVIDE(__UserCode_Size = __image_end - __image_start);

	/* 未初始化的全局变量和静态变量（或者初始化为0） */
	.bss ALIGN(8) (NOLOAD) :
	{
		PROVIDE(__bss_start = .);
		*(.bss*)
		*(.sbss*)
		*(COMMON)
		. = ALIGN(8);
		PROVIDE(__bss_end = .);
	} > RAM

	PROVIDE( _end = __bss_end);

	.stack ALIGN(16) (NOLOAD) :
	{
		/* 栈的起始地址 */
		PROVIDE(__stack_start = .);
		. = ORIGIN(RAM) + LENGTH(RAM); 
		. = ALIGN(16);
		PROVIDE(__stack_end = .);
	} > RAM

	/DISCARD/ : { *(.dynsym) }
	/DISCARD/ : { *(.dynstr*) }
	/DISCARD/ : { *(.dynamic*) }
	/DISCARD/ : { *(.plt*) }
	/DISCARD/ : { *(.interp*) }
	/DISCARD/ : { *(.gnu*) }
}
