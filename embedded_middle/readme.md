# 嵌入式中级题
RISC-V上的动态模块加载实现（以K210/D1/BL702为例）

## 题目描述
Python中封装了ctype可以方便地进行C与Python之间的交互。  
矽速科技的最新版MaixPy（micropython）中也加入了类似的接口，可以方便地实现mpy代码中调用c编译的obj文件里的函数。  
这其中包含了obj的动态加载，FFI等，简单起见，本赛题仅要求实现obj文件内函数的动态加载。  
主要考察参赛者对于 基础编译原理，RISC-V指令集的了解，基础的编码能力。  
资料可以参阅 linux内核源码 和 工具链的binutils相关源码，相当于在单片机上实现了链接器的核心功能，或者说仿linux的内核模块。  
本赛题的硬件平台可在以下平台选择其一：  
1. Sipeed RV debugger plus BL702调试小板
    [购买地址](https://item.taobao.com/item.htm?id=648095486021)  
    BL702为RV32内核单片机，不带MMU，重定位实现起来比较方便
2. Sipeed LicheeRV D1核心板
    [购买地址](https://item.taobao.com/item.htm?id=660478137105)  
    D1为RV64 C906内核处理器，矽速提供了debian固件方便本地编译
    在linux用户态实现的话，存在SV39虚拟地址的问题，会多增加构造跳桩函数的工作
3. Sipeed Maix系列K210开发板
    [购买地址](https://sipeed.taobao.com/category-1425471023.htm)  
    K210为RV64 内核处理器，矽速经典款板卡，适合已有该款板卡的用户调试

测试的待加载程序内容为以下的func.c
```
#include "stdint.h"

int add(int a, int b)   //无重定位的最简单情况
{
    return a+b;
}

int fib(int n)          //需要重定位，实现约三条内部跳转的重定位码
{
    if(n<=1) return 1;
    else return fib(n-1) + fib(n-2);
}

int hello(void)         //需要重定位，实现约三条重定位码，并需要能调用外部符号
{                       //注意在D1的debian系统下实现的话，需要额外的跳转工作量
    printf("Hello from obj!\n");
    return 0;
}
```

使用目标平台对应工具链编译得到 func.o 作为待测文件，指令为：
```
xxx-gcc -mno-relax -c func.c
```

参考加载方式为：
```
elf_init(...);
elf_t* elf = elf_load_file("func.o"); 
//elf_t* elf = elf_load_buf(buf); //BL702/K210可以只实现加载buf的形式
func_fib_t func_fib = (func_fib_t)elf_sym(elf,"fib"); 
int fib = func_fib(30);
printf("fib(30) is %d\n", fib); 
```

对于合格的中级嵌入式工程师，本赛题的参考用时为3～5天。


## 提交内容
参赛者请在2022.3.31前提交结果  
提交邮箱： support@sipeed.com  
邮件标题：[矽速挑战赛] 嵌入式中级组 参赛者名（可以是昵称）  
邮件内容：参赛者的基本信息（姓名，学校/公司，联系方式等），阐述基本的工作流程，优化点等
附件内容：源码工程压缩包，以及预编译固件或程序供测试  

## 评比方法
1. 本题主要从功能实现的 完善程度，优雅/简洁 程度评价  
2. 最低要求是实现上述 func.o 的动态加载运行，若未完成这基本功能则没有评奖资格
3. 如果实现的重定位码更全，我们会使用更多的典型函数来测试完善程度
4. 如果实现的完善程度接近，则会通过代码的 优雅/简洁 程度评判
5. 本赛题最终解释权归矽速科技所有。

## 成绩天梯
参赛者的测试结果会在比赛期间及时更新到本节

