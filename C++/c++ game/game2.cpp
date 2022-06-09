#include <stdio.h>
#include <conio.h>
#include <string>
#include <windows.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <time.h>
using namespace std;
int ax,ay;
char a[30][30]={" ----- ----  -------       ",
				"#O##              | ...... ",
				"  ## ###### ------- ...... ",
				"!    ###### #   #   ...... ",
				"!#######    # #   #|...... ",
				"!#####   #### #####|...... ",
				"!##### ##   # #####|...... ",
				"!##       # #   ###|...... ",
				"!########## ### ###|...... ",
				"!#####      #      |...... ",
				"!##### ###### ####         ",
				"??????        -----|"};
char ch,ch1;
HANDLE hOut;
void gt(int x,int y)
{
	COORD pos={x,y};
	hOut=GetStdHandle(STD_OUTPUT_HANDLE);
	SetConsoleCursorPosition(hOut,pos);
}
void dw()
{
	for(int i=0;i<ay;i++)
		puts(a[i]);
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
	//cout<<sizeof(a)/sizeof(a[20])<<endl;
	string x=a[0];
	system("cls");
	printf("按任意鍵開始");
	printf("%d",x.length());
	int i=0;
	ax=x.length();
	for(;i<sizeof(a)/sizeof(a[0]);i++)
	{
		x=a[i];
		if(x.length()==0)break;
	}
	printf("%d",i);
	ay=i;
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
	time_t start, end;
	int i=0,x=1,y=1,fx=0,fy=0,z;
	stringstream aq;
	a[fy][fx]='@';
    ifstream ifs;
    ofstream ofs;
    fstream newFile;
    newFile.open("game2.txt");
    if(!newFile){
    	newFile.open("game2.txt", ios::out);//best score
    	newFile.close();
    }
    string br;
    ifs.open("game2.txt");
    getline(ifs,br);
    aq<<br;
    aq>>z;
	gt(0,ay+1);
	if(z==-1)
		cout<<"you are first player";
	else
    	cout<<"best time:"<<z<<"sec";
    ifs.close();
    
	start = time(NULL);
    while(1)
    {
    	gt(0,0);
    	dw();
    	gt(0,0);
		if(x==fx&&y==fy)
			break;
    	gt(0,12);
    	printf("                                                        ");
    	gt(0,12);
    	printf("x:%d\ty:%d",x,y);
    	ch=getch();
    	if(ch==-32)
    		ch1=getch();
    	if(ch>='A'&&ch<='Z')
    		ch+=32;
    	if(ch=='a'||ch1==75)
    	{
    		if(a[y][(x-1+ax)%ax]==' ')
    		{
    			swap(a[y][x],a[y][(x-1+ax)%ax]);
				x=(x-1+ax)%ax;
			}
			if(a[y][(x-1+ax)%ax]=='@')
			{
    			a[y][(x-1+ax)%ax]='0';
    			a[y][x]=' ';
				x=(x-1+ax)%ax;
			}
		}
    	if(ch=='d'||ch1==77)
    	{
    		if(a[y][(x+1+ax)%ax]==' ')
    		{
    			swap(a[y][x],a[y][(x+1+ax)%ax]);
    			x=(x+1+ax)%ax;
			}
			if(a[y][(x+1+ax)%ax]=='@')
			{
    			a[y][(x+1+ax)%ax]='0';
    			a[y][x]=' ';
				x=(x+1+ax)%ax;
			}
		}
    	if(ch=='s'||ch1==80)
    	{
    		if(a[(y+1+ay)%ay][x]==' ')
    		{
    			swap(a[y][x],a[(y+1+ay)%ay][x]);
    			y=(y+1+ay)%ay;
			}
			if(a[(y+1+ay)%ay][x]=='@')
			{
    			a[(y+1+ay)%ay][x]='0';
    			a[y][x]=' ';
    			y=(y+1+ay)%ay;
			}
		}
    	if(ch=='w'||ch1==72)
    	{
    		if(a[(y-1+ay)%ay][x]==' ')
    		{
    			swap(a[y][x],a[(y-1+ay)%ay][x]);
    			y=(y-1+ay)%ay;
			}
			if(a[(y-1+ay)%ay][x]=='@')
			{
    			a[(y-1+ay)%ay][x]='0';
    			a[y][x]=' ';
    			y=(y-1+ay)%ay;
			}
		}
	}
	end = time(NULL);
	system("cls");
	gt(16,8);
	printf("You Win!!");
	gt(16,10);
	if(end-start<z||z<0)
	{
		ofs.open("game2.txt", std::ios::out | std::ios::trunc);
	    ofs<<end-start;
    	ofs.close();
    	printf("you spend %d sec(you are the best)",end-start);
	}
	else
		printf("you spend %d sec(best time:%d)",end-start,z);
	Sleep(3000);
}
