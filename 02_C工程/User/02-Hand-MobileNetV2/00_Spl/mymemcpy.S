#include <linkage.h>

	.global mymemcpy                      //全局声明mymemcoy
	.type mymemcpy, %function             //标明是函数
	.align 3                            //3字节对齐
	/*a0——目的地址，a1——源地址，a2——拷贝长度*/
mymemcpy: 
	move t6, a0                         //将a0中的值，也就是目的地址存入t6寄存器中
	sltiu a3, a2, 128                   //判断a2中的值，也就是待拷贝字节数是否超过128，a2小于128，则a3赋值为1，否则赋值为0
	bnez a3, 4f                         //如果a3不等于0，则跳转到4f执行
	andi a3, t6, REGSZ - 1              //目的地址与7（REGSZ为8）相与并存入a3
	andi a4, a1, REGSZ - 1              //a1即源地址与7相与存入a4
	bne a3, a4, 4f                      //如果a3与a4不相等则跳转到4
	beqz a3, 2f                         //如果a3中的值为0，则跳转到2f
	andi a3, a1, ~(REGSZ - 1)           //将0x7取反并和源地址相与存入a3寄存器中
	addi a3, a3, REGSZ                  //将a3加上0x8并存入a3中
	sub a4, a3, a1                      //将a3与源地址的差值存入a4寄存器中 
1:	lb a5, 0(a1)                        //取出源地址中的数据存入a5寄存器中
	addi a1, a1, 1                      //将a1加上1并存入a1寄存器中，也就是源地址往后偏移一位
	sb a5, 0(t6)                        //将a5中的值存入t6对应地址中，也就是目的地址中
	addi t6, t6, 1                      //将目的地址加1并存入t6中，也就是目的地址往后偏移一位
	bltu a1, a3, 1b                     //如果源地址小于a3，跳回到1b
	sub a2, a2, a4                      //a2减a4中的值并存入a2中
2:	andi a4, a2, ~((16 * REGSZ) - 1)    //a2与上~(127)（除非a2等于128，否则都为0）赋值给a4
	beqz a4, 4f                         //判断a4是否为0，为0则跳转4f
	add a3, a1, a4                      //a1加上a4赋值给a3
3:	LREG a4,          0(a1)             //加载a1中地址所存储的值到a4中           
	LREG a5,      REGSZ(a1)             //加载a1中地址+8所存储的值到a4中
	LREG a6,  2 * REGSZ(a1)
	LREG a7,  3 * REGSZ(a1)
	LREG t0,  4 * REGSZ(a1)
	LREG t1,  5 * REGSZ(a1)
	LREG t2,  6 * REGSZ(a1)
	LREG t3,  7 * REGSZ(a1)
	LREG t4,  8 * REGSZ(a1)
	LREG t5,  9 * REGSZ(a1)
	SREG a4,          0(t6)
	SREG a5,      REGSZ(t6)
	SREG a6,  2 * REGSZ(t6)
	SREG a7,  3 * REGSZ(t6)
	SREG t0,  4 * REGSZ(t6)
	SREG t1,  5 * REGSZ(t6)
	SREG t2,  6 * REGSZ(t6)
	SREG t3,  7 * REGSZ(t6)
	SREG t4,  8 * REGSZ(t6)
	SREG t5,  9 * REGSZ(t6)
	LREG a4, 10 * REGSZ(a1)
	LREG a5, 11 * REGSZ(a1)
	LREG a6, 12 * REGSZ(a1)
	LREG a7, 13 * REGSZ(a1)
	LREG t0, 14 * REGSZ(a1)
	LREG t1, 15 * REGSZ(a1)
	addi a1, a1, 16 * REGSZ             //源地址偏移16*8
	SREG a4, 10 * REGSZ(t6)
	SREG a5, 11 * REGSZ(t6)
	SREG a6, 12 * REGSZ(t6)
	SREG a7, 13 * REGSZ(t6)
	SREG t0, 14 * REGSZ(t6)
	SREG t1, 15 * REGSZ(t6)
	addi t6, t6, 16 * REGSZ             //目的地址偏移16*8
	bltu a1, a3, 3b                     //判断源地址是否到截止地址，没到就跳回3
	andi a2, a2, (16 * REGSZ) - 1       //a2与上(16*8-1)并存入a2中
4:	beqz a2, 6f                         //判断a2是否为0，为0则跳转到6f               
	add a3, a1, a2                      //a1加上a2中的值赋值到a3
	or a5, a1, t6                       //a1或上t6填入a5
	or a5, a5, a3                       //a5或上a3填入a5
	andi a5, a5, 3                      //a5与上3填入a5
	bnez a5, 5f                         //a5不等于0跳转到5
7:	lw a4, 0(a1)                        //加载源地址的数据到a4寄存器中
	addi a1, a1, 4                      //源地址加4
	sw a4, 0(t6)                        //将a4中的值写到目的地址中
	addi t6, t6, 4                      //目的地址加4
	bltu a1, a3, 7b                     //源地址小于a3，即截止地址时继续拷贝
	ret                                 //返回
5:	lb a4, 0(a1)                        //加载源地址的数据到a4寄存器中
	addi a1, a1, 1                      //源地址加1
	sb a4, 0(t6)                        //将a4中的值写到目的地址中
	addi t6, t6, 1                      //目的地址加1
	bltu a1, a3, 5b                     //源地址小于a3，即截止地址时继续拷贝
6:	ret                                 //返回                         
