#include "stdint.h"
#include "stdio.h"

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

static void* l_puts = (void*)puts;
typedef int (*puts_func_t)(const char *string);
int test_datarel(void)
{
    puts_func_t my_puts = (puts_func_t)l_puts;
    printf("get my_puts = 0x%lx\n", (uint64_t)my_puts);
    my_puts("test datarel ok!\n");
    return 0;
}

// gcc -Os -mno-relax -c func.c