#include <stdio.h>
#include <conio.h>
#include <string.h>
#include <windows.h>
char a;
HANDLE hIn,hOut;
void gt(int x,int y)
{
	COORD pos={x,y};
	hOut=GetStdHandle(STD_OUTPUT_HANDLE);
	SetConsoleCursorPosition(hOut,pos);
}
void hide()
{
	CONSOLE_CURSOR_INFO curInfo;
	hOut=GetStdHandle(STD_OUTPUT_HANDLE);
	curInfo.dwSize=1;
	curInfo.bVisible=0;
	SetConsoleCursorInfo(hOut,&curInfo);
}
void wel()
{
	printf("按任意鍵開始");
	getch();
	system("cls");
}
void set()
{
	HWND hwnd = GetConsoleWindow();
	if(hwnd!=NULL)
		MoveWindow(hwnd,0,0,600,600,TRUE);
}
main()
{
	set();
	hide();
	wel();
	int i=0;
	char b[]="◎",c[]="█";
	for(int i=0;i<20;i++)
	{
		for(int j=0;j<50;j++)
			printf("　");
		printf("\n");
	}
	gt(0,6);
	int x=12,y=6;
	printf("\
　　　　　　　██████████　\n\
　　　　　　█　　　　　　　　　　█\n\
　　　　　　█　　　　　　　　　　█\n\
　　　　　　█　　　　　　　　　　█\n\
　　　　　　█　　　　　　　　　　█\n\
　　　　　　█　　　　　　　　　　█\n\
　　　　　　█　　　　　　　　　　█\n\
　　　　　　█　　　　　　　　　　█\n\
　　　　　　█　　　　　　　　　　█\n\
　　　　　　█　　　　　　　　　　█\n\
　　　　　　█　　　　　　　　　　█\n\
　　　　　　　██████████　\n");//+"%s%s%s%s\n%s%s%s%s%s",c,c,c,c,b,b,b,b,c
    while(1)
    {
    	a=getch();
    	gt(a,a);
    	printf("%c",a);
    	//draw(a,a,a);
    	//printf("%d:%c\n",++i,);
    	/*
    	if(a>='A'&&a<='Z')
    		a+=32;
    	if(a=='w')
    	{
    		printf("12edasklac");
		}
		*/
	}
}

//!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
////
//◎┌─┐│└┘
