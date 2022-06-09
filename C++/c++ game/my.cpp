//?
#include <stdio.h>
#include <conio.h>
#include <windows.h>
#include <iostream>
#include <time.h>
#include <vector>
#include <math.h>
using namespace std;
HANDLE hOut;
int x=2,y=2,m,ax,ay,fx,fy;
vector<int> a(x*y),gl(x*y);
char ch,ch1;
void gt(int sx,int sy)
{
	COORD pos={sx,sy};
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
void set()
{
	HWND hwnd = GetConsoleWindow();
	if(hwnd!=NULL)
		MoveWindow(hwnd,0,0,800,600,TRUE);
}
void wel()
{
    system("COLOR 0f");
    system("TITLE ???");
	system("cls");
	printf("Press any key to start\nPress Y/y to change side\n");
	char q=getch();
	if(q=='Y'||q=='y')
	{
		printf("side(x):");
		int w;
		cin>>w;
		x=w;
		printf("side(y):");
		cin>>w;
		y=w;
		a.resize(x*y);
		gl.resize(x*y);
	}
	system("cls");
}
int ck()
{
	int g=1;
	if(ax!=fx||ay!=fy)return 0;
	for(int i=0;i<x*y;i++)
	{
		if(a[i]!=gl[i])
		{
			g=0;
			break;
		}
	}
	return g;
}
void draw()
{
	for(int i=0;i<y*2;i++)
	{
		for(int j=0;j<x;j++)
		{
			printf("            ");
		}
		printf("\n");
	}
	gt(0,0);
	for(int i=0;i<y;i++)
	{
		for(int j=0;j<x;j++)
		{
			if(a[i*x+j]!=0)
				printf("%d",a[i*x+j]);
			printf("\t");
		}
	}
}
void qwas(int ls)
{
	if(ls==0)return;
	printf("%d",ls);
}
void drw()
{
	for(int i=-2;i<=2;i++)
	{
		for(int j=-2;j<=2;j++)
		{
			if(i*j==4||i*j==-4)continue;
			gt((ax+i+x)%x*4,(ay+j+y)%y*2);
			printf("    ");
			gt((ax+i+x)%x*4,(ay+j+y)%y*2);
			qwas(a[((ay+j+y)%y)*x+((ax+i+x)%x)]);
		}
	}
}
void up()
{
	int sy=ay;
	ay=(ay-1+y)%y;
	swap(a[ay*x+ax],a[sy*x+ax]);
}
void lt()
{
	int sx=ax;
	ax=(ax-1+x)%x;
	swap(a[ay*x+ax],a[ay*x+sx]);
}
void dw()
{
	int sy=ay;
	ay=(ay+1+y)%y;
	swap(a[ay*x+ax],a[sy*x+ax]);
}
void rt()
{
	int sx=ax;
	ax=(ax+1+x)%x;
	swap(a[ay*x+ax],a[ay*x+sx]);
}
//-------------------
void upa()
{
	int sy=fy;
	fy=(fy-1+y)%y;
	swap(gl[fy*x+fx],gl[sy*x+fx]);
}
void lta()
{
	int sx=fx;
	fx=(fx-1+x)%x;
	swap(gl[fy*x+fx],gl[fy*x+sx]);
}
void dwa()
{
	int sy=fy;
	fy=(fy+1+y)%y;
	swap(gl[fy*x+fx],gl[sy*x+fx]);
}
void rta()
{
	int sx=fx;
	fx=(fx+1+x)%x;
	swap(gl[fy*x+fx],gl[fy*x+sx]);
}
void sw()
{
	for(int i=0;i<x*y;i++)
	{
		int was=rand()%4;
		if(was==0)upa();
		if(was==1)lta();
		if(was==2)rta();
		if(was==3)dwa();
	}
	if(ck())sw();
}
void play()
{
	m=0;
	gt(0,0);
	for(int i=0;i<x*y;i++)
	{
		a[i]=i;
		gl[i]=i;
	}
	ax=ay=fx=fy=0;
	sw();
	for(int i=0;i<y*2-1;i++)
	{
		gt(x*4+2,i);
		printf("|");
	}
	for(int i=0;i<y;i++)
	{
		for(int j=0;j<x;j++)
		{
			gt(j*4,i*2);
			qwas(a[i*x+j]);
		}
	}
	for(int i=0;i<y;i++)
	{
		for(int j=0;j<x;j++)
		{
			gt(j*4+x*4+4,i*2);
			qwas(gl[i*x+j]);
		}
	}
	while(1)
	{
		drw();
		gt(0,y*2+1);
		printf("%d",m);
    	if(ck())
    		break;
    	do
    	{
    		ch=getch();
	    	if(ch==-32)
	    		ch1=getch();
	    	if(ch>='A'&&ch<='Z')
	    		ch+=32;
		}while(!(ch==-32));
    	if(ch=='w'||ch1==72)up();
    	if(ch=='a'||ch1==75)lt();
    	if(ch=='d'||ch1==77)rt();
    	if(ch=='s'||ch1==80)dw();
    	m++;
	}
}
int main()
{
	set();
	hide();
	wel();
	srand(time(NULL));
    play();
	gt(0,y*2+2);
	printf("You Win!!\n");
	Sleep(3000);
    system("pause");
	system("cls");
}

