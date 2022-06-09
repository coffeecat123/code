#include <stdio.h>
#include <conio.h>
#include <string.h>
#include <windows.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <time.h>
#include <vector>
using namespace std;
HANDLE hOut;
int y=10,x=y*2;
vector<char> a(x*y);
vector<int> sm(x*y);
int ax=1,ay=1,b,c,d[4],fx,fy;
char ch,ch1,wl='#',p='0',key='$';
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
		MoveWindow(hwnd,0,0,700,700,TRUE);
}
void sdw()
{
	for(int i=0;i<y;i++)
	{
		for(int j=0;j<x;j++)
			printf("%c",a[i*x+j]);
		printf("\n");
	}
}
void dw()
{
	gt(ax,ay);
	printf("%c",a[ay*x+ax]);
	gt((ax+1+x)%x,(ay+0+y)%y);
	printf("%c",a[((ay+0+y)%y)*x+((ax+1+x)%x)]);
	gt((ax+0+x)%x,(ay+1+y)%y);
	printf("%c",a[((ay+1+y)%y)*x+((ax+0+x)%x)]);
	gt((ax-1+x)%x,(ay+0+y)%y);
	printf("%c",a[((ay+0+y)%y)*x+((ax-1+x)%x)]);
	gt((ax+0+x)%x,(ay-1+y)%y);
	printf("%c",a[((ay-1+y)%y)*x+((ax+0+x)%x)]);
	gt(0,y+4);
}
void map()
{
	a.resize(x*y);
	sm.resize(x*y);
	vector<int> bx,by,dd,qwx,qwy;
	int awx=rand()%x,awy=rand()%y;
	int xx=awx+(awx+1)%2,yy=awy+(awy+1)%2,
		dx[4]={0,2,0,-2},
		dy[4]={-2,0,2,0};
	sm[xx+yy*x]=1;
	bx.push_back(xx);
	by.push_back(yy);
	qwx.push_back(xx);
	qwy.push_back(yy);
	while(!bx.empty())
	{
		int ad=bx.size()-1;
		xx=bx[ad];
		yy=by[ad];
		int kh=0;
		dd.clear();
		for(int i=0;i<4;i++)
		{
			if(xx+dx[i]>=x||xx+dx[i]<0
			 ||yy+dy[i]>=y||yy+dy[i]<0)continue;
			if(sm[xx+dx[i]+(yy+dy[i])*x]==1)continue;
			dd.push_back(i);
			kh=1;
		}
		if(kh)
		{
			int ac=dd[rand()%dd.size()];
			sm[xx+dx[ac]/2+(yy+dy[ac]/2)*x]=1;
			sm[xx+dx[ac]+(yy+dy[ac])*x]=1;
			bx.push_back(xx+dx[ac]);
			by.push_back(yy+dy[ac]);
			qwx.push_back(xx+dx[ac]);
			qwy.push_back(yy+dy[ac]);
		}
		else
		{
			bx.erase(bx.begin()+ad);
			by.erase(by.begin()+ad);
		}
	}
	for(int i=0;i<y;i++)
		for(int j=0;j<x;j++)
		{
			if(sm[i*x+j]==0)a[i*x+j]=wl;
			else a[i*x+j]=' ';
		}
	ax=ay=1;
	a[ax+ay*x]=p;
	do
	{
		int ar=rand()%qwx.size();
		fx=qwx[ar];
		fy=qwy[ar];
	}while(ax==fx&&ay==fy);
	a[fx+fy*x]=key;
}
void play()
{
	map();
	gt(0,0);
	sdw();
    while(1)
    {
    	gt(0,0);
		if(ax==fx&&ay==fy)
			break;
    	dw();
    	gt(0,0);
    	gt(0,y+2);
    	printf("                                                        ");
    	gt(0,y+2);
    	printf("x:%d\ty:%d",ax,ay);
    	ch=getch();
    	if(ch==-32)
    		ch1=getch();
    	if(ch>='A'&&ch<='Z')
    		ch+=32;
    	if(ch=='a'||ch1==75)
    	{
    		if(a[(ay)*x+((ax-1+x)%x)]==' ')
    		{
    			swap(a[ay*x+ax],a[(ay)*x+((ax-1+x)%x)]);
				ax=(ax-1+x)%x;
			}
			else if(a[(ay)*x+((ax-1+x)%x)]==key)
			{
    			a[(ay)*x+((ax-1+x)%x)]=p;
    			a[ay*x+ax]=' ';
				ax=(ax-1+x)%x;
			}
		}
    	if(ch=='d'||ch1==77)
    	{
    		if(a[(ay)*x+((ax+1+x)%x)]==' ')
    		{
    			swap(a[ay*x+ax],a[(ay)*x+((ax+1+x)%x)]);
    			ax=(ax+1+x)%x;
			}
			else if(a[(ay)*x+((ax+1+x)%x)]==key)
			{
    			a[(ay)*x+((ax+1+x)%x)]=p;
    			a[ay*x+ax]=' ';
				ax=(ax+1+x)%x;
			}
		}
    	if(ch=='s'||ch1==80)
    	{
    		if(a[((ay+1+y)%y)*x+(ax)]==' ')
    		{
    			swap(a[ay*x+ax],a[((ay+1+y)%y)*x+(ax)]);
    			ay=(ay+1+y)%y;
			}
			else if(a[((ay+1+y)%y)*x+(ax)]==key)
			{
    			a[((ay+1+y)%y)*x+(ax)]=p;
    			a[ay*x+ax]=' ';
    			ay=(ay+1+y)%y;
			}
		}
    	if(ch=='w'||ch1==72)
    	{
    		if(a[((ay-1+y)%y)*x+(ax)]==' ')
    		{
    			swap(a[ay*x+ax],a[((ay-1+y)%y)*x+(ax)]);
    			ay=(ay-1+y)%y;
			}
			else if(a[((ay-1+y)%y)*x+(ax)]==key)
			{
    			a[((ay-1+y)%y)*x+(ax)]=p;
    			a[ay*x+ax]=' ';
    			ay=(ay-1+y)%y;
			}
		}
	}
}
void wel()
{
	system("cls");
	printf("Press any key to start(press:Y/y to change side length)");
	char df;
	cin>>df;
	int qp;
	if(df=='y'||df=='Y')
	{
		printf("side length(5~100):");
		cin>>qp;
		if(qp<5||qp>100)
		{
			system("cls");
			return;
		}
		y=qp+(qp+1)%2;
		x=y*2-1;
    	fstream newFile;
    	newFile.open("g3a.txt", std::ios::out | std::ios::trunc);
    	newFile<<y;
    	newFile.close();
	}
	system("cls");
}
void cls()
{
	for(int i=0;i<y+5;i++)
	{
		for(int j=0;j<x+5;j++)
			printf(" ");
		printf("\n");
	}
}
int main()
{
	set();
	hide();
	wel();
	srand(time(NULL));
	stringstream aq;
    string br;
    int z;
    ifstream ifs;
    ofstream ofs;
    fstream newFile;
    newFile.open("g3a.txt");
    if(!newFile){
    	newFile.open("g3a.txt", std::ios::out | std::ios::trunc);
    	newFile<<y;
		system("cls");
    }
    else
    {
    	getline(newFile,br);
	    aq<<br;
	    aq>>z;
	    y=z;
	    x=y*2-1;
	}
    newFile.close();
    newFile.open("g3.txt");
    getline(newFile,br);
    aq<<br;
    aq>>z;
    if(!newFile)
		z=-1;
	gt(0,y+1);
	if(z<0)
		cout<<"you are first player";
	else
    	cout<<"best time:"<<z<<"sec";
    newFile.close();
    
	time_t start, end;
	start = time(NULL);
    play();
	end = time(NULL);
	system("cls");
	gt(16,8);
	printf("You Win!!");
	gt(16,10);
	if(end-start<z||z<=0)
	{
		newFile.open("g3.txt", std::ios::out | std::ios::trunc);
	    newFile<<end-start;
    	newFile.close();
    	printf("you spend %d sec(you are the best)",end-start);
	}
	else
		printf("you spend %d sec(best time:%d)",end-start,z);
	Sleep(3000);
	system("cls");
}

