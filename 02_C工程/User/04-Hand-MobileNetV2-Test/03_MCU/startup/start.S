/*
 * start.S
 *
 */

#include <linkage.h>
#include <riscv64.h>

	.global start
start:
	/* BROM 的引导头信息 
	   此处引导头信息会通过"../00_Spl/tools/mksunxi.exe"工具填充校验和
	*/
	.long 0x0300006f
	.byte 'e', 'G', 'O', 'N', '.', 'B', 'T', '0'
	.long 0x12345678				// 校验和 
	.long __spl_size				// spl程序
	.long 0x30						// 引导头大小 
	.long 0x30303033				// 引导头版本 
	.long 0x00020000				// 返回值 
	.long 0x00020000				// 运行地址 
	.long 0x0						// eGON版本 
	.byte 0x00, 0x00, 0x00, 0x00	// 平台信息 8字节 
	.byte 0x34, 0x2e, 0x30, 0x00
	
	/*【修改处】1 */
	.long __UserCode_Size
	
/*实际重启代码*/
handle_reset:
	/* 屏蔽所有中断 */
	csrw mideleg, zero  			//清零机器模式中断降级控制寄存器
	csrw medeleg, zero  			//清零机器模式异常降级控制寄存器
	csrw mie, zero      			//清零机器模式中断使能控制寄存器
	csrw mip, zero      			//清零机器模式中断等待状态寄存器

	/* 设置异常向量 */
	la t1, _image_start    			//加载_image_start地址到t1寄存器
	LREG t1, (t1)          			//加载t1地址中的值到t1寄存器中，即取出链接文件中__image_start的地址
	la t2, start          			//加载start地址到t2寄存器
	sub t0, t1, t2         			//t1寄存器减去t2寄存器中的值并存入t0寄存器
	la a0, vectors         			//加载vectors的地址到a0寄存器
	add a0, a0, t0         			//a0加上t0中的值重新赋值给a0寄存器
	csrw mtvec, a0         			//赋值向量基址到机器模式向量基址寄存器

	/* 启用 FPU 和加速器（如果存在） */
	li t0, MSTATUS_FS | MSTATUS_XS  //赋值(3<<13 | 3<<15)到t0寄存器
	csrs mstatus, t0                //t0中的值赋值到机器模式处理器状态寄存器中启用浮点单元和扩展单元

	/* 机器模式扩展状态寄存器启用 theadisaee，可正常执行C906扩展指令*/
	li t1, 0x1 << 22
	.word 0x7c032073				//0x7c0是mxstatus寄存器的基地址，0x7c032073这行代码相当于汇编指令csrs mxstatus, t1 

	/* 机器模式硬件操作寄存器使能cachesel/inv/btb/bht位*/
	li t1, 0x30013
	.word 0x7c232073				//0x7c2是mcor寄存器的基地址，0x7c232073这行代码相当于汇编指令csrs mcor, t1

	
	/* 检查PC值并初始化 */
	csrr t0, mhartid     			//读取机器模式逻辑内核编号寄存器中的值到t0寄存器
	bnez t0, _avoid      			//若t0寄存器中值不为0，则跳转到_avoid继续执行
	la t0, start        			//加载start地址到t0寄存器
	la t1, _image_start  			//加载_image_start地址到t1寄存器
	LREG t1, (t1)        			//加载t1地址中的值到t1寄存器中，即取出链接文件中__image_start的地址
	beq t0, t1, _avoid   			//判断t0与t1是否相等，相等则跳转到_avoid执行

	/* 初始化串口和时钟*/
	call sys_uart_init   			//跳转到初始化串口程序
	call sys_clock_init  			//跳转到初始化时钟程序

	/*【修改处】2 */
	/* 拷贝ddr初始化的bin文件到地址0x00030000 */
	/*
	la t1, _ddr_bin_start  			//加载_ddr_bin_start地址到t1寄存器
	LREG t1, (t1)         		 	//加载t1地址中的值到t1寄存器中，即取出链接文件中__ddr_bin_start的地址
	la t2, _ddr_bin_end    			//加载_ddr_bin_end地址到t2寄存器
	LREG t2, (t2)          			//加载t2地址中的值到t2寄存器中，即取出链接文件中__ddr_bin_end的地址
	sub a2, t2, t1         			//t2减去t1并存入到a2寄存器中
	la t1, _image_start    			//加载_image_start地址到t1寄存器
	LREG t1, (t1)          			//加载t1地址中的值到t1寄存器中，即取出链接文件中__image_start的地址
	la t2, _ddr_bin_start  			//加载_ddr_bin_start地址到t2
	LREG t2, (t2)          			//加载t2地址中的值到t2寄存器中，即取出链接文件中__ddr_bin_start的地址
	sub t0, t2, t1         			//记录_ddr_bin_start相对_image_start的偏移地址到t0寄存器中
	la a1, start          			//加载start地址到a1寄存器
	add a1, a1, t0         			//a1加上t0即start到_ddr_bin_start的地址
	li a0, 0x00030000      			//存入立即数ddr起始地址到a0寄存器
	call mymemcpy            		//跳转memcpy程序
	call sys_dram_init     			//跳转ddr初始化程序
	*/
_avoid:
	nop                    			//空指令

.option push                 		//压栈
.option norelax              
	/*初始化全局指针寄存器*/
	la t0, _global_pointer$  		//将ld文件值的_global_pointer$地址赋值给t0寄存器
	LREG gp, (t0)            		//将这个地址加载到全局指针寄存器中
.option pop                  		//出栈

	/* 初始化栈 */
	la t1, _stack_start   	   		//加载_stack_start地址到t1寄存器中
	LREG t1, (t1)            		//加载t1地址中的值到t1寄存器中，即取出链接文件中__stack_start的地址
	la t2, _stack_end        		//加载_stack_end地址到t2寄存器中
	LREG t2, (t2)            		//加载t2地址中的值到t2寄存器中，即取出链接文件中__stack_end的地址
	sub t0, t2, t1           		//获取栈长度到t0寄存器中
	csrr t3, mhartid         		//读取机器模式逻辑内核编号寄存器中的值到t3寄存器,此寄存器的值为0
	li t4, 1                 		//存入立即数1到t4寄存器中
	div t0, t0, t4           		//t0除以t4并存入t0寄存器中，t0=stack_len
	mul t0, t0, t3           		//t0乘以t3并存入t0寄存器中,t0 = 0
	sub sp, t2, t0           		//t2减去t0的值存入堆栈指针中,sp = stack_end

	/* 检查hart */
	csrr a0, mhartid         		//读取机器模式逻辑内核编号寄存器中的值到a0寄存器
	beqz a0, 2f              		//a0等于0时跳转到2执行
1:	nop
	j 1b                     		//跳回1
2:	nop
	/*【修改处】3 */
	/* 拷贝自身到链接地址 */
	/*
	la t0, _start            		//加载_start地址到t0寄存器
	la t1, _image_start      		//加载_image_start地址到t1寄存器
	LREG t1, (t1)            		//加载t1地址中的值到t1寄存器中，即取出链接文件中__image_start的地址
	beq t0, t1, 1f           		//判断t0与t1地址是否相等，相等则跳转1f
	call sys_copyself        		//调用sys_copyself程序
	*/
1:	nop

	/* 清bss段 */
	jal clear_bss
	
clear_bss:
	la	t0, _bss_start
	LREG t0, (t0)
	la	t1, _bss_end
	LREG t1, (t1)

clbss_1:
	sw zero, 0(t0)
	addi t0, t0, 4
	blt t0, t1, clbss_1

	/*开全局中断*/
	li t0,0x800              		//存入立即数0x800到t0寄存器中
	csrs mie,t0              		//机器模式中断使能控制寄存器使能外部中断

	/* 开机器模式中断*/
	li t0, 0x88              		//存入立即数0x88到t0寄存器
	csrs mstatus, t0         		//机器模式处理器状态寄存器使能机器模式中断以及保留中断

	/* 调用主函数 */
	la t1, _image_start      		//加载_image_start地址到t1寄存器
	LREG t1, (t1)            		//加载t1地址中的值到t1寄存器中，即取出链接文件中__image_start的地址
	la t2, start            		//加载start地址到t2寄存器，由于start是直接定义在汇编文件中额，此时pc就是指向这个地址
	sub t0, t1, t2           		//_image_start相对于start的偏移地址存入t0寄存器中
	la a0, _main             		//加载_main地址到a0寄存器中
	add a0, a0, t0           		//a0加上t0存到a0寄存器中，如果pc此时指向外接ddr地址，
	                                //那么start地址和__image_start一样，此时a0就是_main地址
									//如果此时pc指向的还是片内SRAM那么a0此时就是外接ddr的地址
	jr a0                    		//pc指向a0寄存器
_main:
	call Componentfun_Init          //调用Componentfun_Init函数
	call int_init                   //【CC-220102】
	call register_irqhandler        //【CC-220103】
	call uart_relate   
	call main                		//跳转到main程序中执行
	j _main                  		//跳到_main


/*中断向量*/
	.align 4                     	//4字节对齐
	.globl vectors               	//全局标明vectors地址
vectors:
	addi sp, sp, -(32 * REGSZ)   	//sp寄存器偏移-(32*8)
	/*保护现场，将32个通用寄存器的值存到某个地方*/
 	SREG x1, 1 * REGSZ(sp)                
	SREG x2, 2 * REGSZ(sp)          
	SREG x3, 3 * REGSZ(sp)          
	SREG x4, 4 * REGSZ(sp)			
	SREG x5, 5 * REGSZ(sp)
	SREG x6, 6 * REGSZ(sp)
	SREG x7, 7 * REGSZ(sp)
	SREG x8, 8 * REGSZ(sp)
	SREG x9, 9 * REGSZ(sp)
	SREG x10, 10 * REGSZ(sp)		
	SREG x11, 11 * REGSZ(sp)
	SREG x12, 12 * REGSZ(sp)
	SREG x13, 13 * REGSZ(sp)
	SREG x14, 14 * REGSZ(sp)
	SREG x15, 15 * REGSZ(sp)
	SREG x16, 16 * REGSZ(sp)
	SREG x17, 17 * REGSZ(sp)
	SREG x18, 18 * REGSZ(sp)
	SREG x19, 19 * REGSZ(sp)
	SREG x20, 20 * REGSZ(sp)
	SREG x21, 21 * REGSZ(sp)
	SREG x22, 22 * REGSZ(sp)
	SREG x23, 23 * REGSZ(sp)
	SREG x24, 24 * REGSZ(sp)
	SREG x25, 25 * REGSZ(sp)
	SREG x26, 26 * REGSZ(sp)
	SREG x27, 27 * REGSZ(sp)
	SREG x28, 28 * REGSZ(sp)
	SREG x29, 29 * REGSZ(sp)
	SREG x30, 30 * REGSZ(sp)
	SREG x31, 31 * REGSZ(sp)		
    /*存好一些特殊的寄存器值，并跳转至handle_trap函数中*/
	csrr a0, mcause       			//读取机器模式异常事件向量寄存器值到a0寄存器中
    csrr a1, mepc               	//读取机器模式异常事件向量寄存器值到a1寄存器中
    mv a2, sp                   	//传送sp中的值到a2寄存器中
	call handle_trap            	//调用handle_trap函数
    csrw mepc, a0               	//将返回值写入机器模式异常事件向量寄存器中
    /*恢复现场，将之前保存的32个通用寄存器的值返回*/
	LREG x1, 1 * REGSZ(sp)
	LREG x2, 2 * REGSZ(sp)
	LREG x3, 3 * REGSZ(sp)
	LREG x4, 4 * REGSZ(sp)
	LREG x5, 5 * REGSZ(sp)
	LREG x6, 6 * REGSZ(sp)
	LREG x7, 7 * REGSZ(sp)
	LREG x8, 8 * REGSZ(sp)
	LREG x9, 9 * REGSZ(sp)
	LREG x10, 10 * REGSZ(sp)		
	LREG x11, 11 * REGSZ(sp)
	LREG x12, 12 * REGSZ(sp)
	LREG x13, 13 * REGSZ(sp)
	LREG x14, 14 * REGSZ(sp)
	LREG x15, 15 * REGSZ(sp)
	LREG x16, 16 * REGSZ(sp)
	LREG x17, 17 * REGSZ(sp)
	LREG x18, 18 * REGSZ(sp)
	LREG x19, 19 * REGSZ(sp)
	LREG x20, 20 * REGSZ(sp)
	LREG x21, 21 * REGSZ(sp)
	LREG x22, 22 * REGSZ(sp)
	LREG x23, 23 * REGSZ(sp)
	LREG x24, 24 * REGSZ(sp)
	LREG x25, 25 * REGSZ(sp)
	LREG x26, 26 * REGSZ(sp)
	LREG x27, 27 * REGSZ(sp)
	LREG x28, 28 * REGSZ(sp)
	LREG x29, 29 * REGSZ(sp)
	LREG x30, 30 * REGSZ(sp)
	LREG x31, 31 * REGSZ(sp)		
	
	addi sp, sp, (32 * REGSZ)   	//sp寄存器恢复
	mret                        	//机器模式异常返回指令

/*将handle_trap弱定义为死循环*/
.weak handle_trap  
handle_trap:
1:
  j 1b


/*地址声明*/
	.align 3                   		//3字节对齐
_image_start:
	RVPTR __image_start             //链接文件中地址，以下也是
_image_end:
	RVPTR __image_end
_global_pointer$:
	RVPTR __global_pointer$
_data_start:
	RVPTR __data_start
_data_end:
	RVPTR __data_end
_bss_start:
	RVPTR __bss_start
_bss_end:
	RVPTR __bss_end
_stack_start:
	RVPTR __stack_start
_stack_end:
	RVPTR __stack_end
_ddr_bin_start:
	RVPTR __ddr_bin_start
_ddr_bin_end:
	RVPTR __ddr_bin_end
