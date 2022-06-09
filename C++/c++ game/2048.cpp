//2048
#include <stdio.h>
#include <conio.h>
#include <windows.h>
#include <iostream>
#include <time.h>
#include <vector>
#include <math.h>
using namespace std;
HANDLE hOut;
int x=4,y=4,h,mv,qq,hqq;
vector<int> a(x*y),s(x*y),qscore(1),qh(1);
vector<int> qa(x*y);
unsigned long long b[64],score=0;
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
    system("TITLE 2048");
	system("cls");
	printf("Welcome to 2048!!(Press any key to start)\nPress Y/y to change side\n");
	char q=getch();
	if(q=='Y'||q=='y')
	{
		printf("side x:");
		cin>>x;
		printf("side y:");
		cin>>y;
		a.resize(x*y);
		s.resize(x*y);
	}
	for(int i=1;i<64;i++)
		b[i]=pow(2,i);
	fill (a.begin(),a.begin()+x*y,0);
	system("cls");
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
				printf("%llu",b[a[i*x+j]]);
			printf("\t");
			//printf("%d\t",a[i*x+j]);
		}
		printf("\n\n");
	}
}
void up()
{
	for(int i=0;i<=x-1;i++)
	{
		int d=0,c;
		for(int k=y-1;k>=0;k--)
			if(a[k*x+i]!=0){d++;c=k;}
		if(d==0)continue;
		if(d==1)
			{swap(a[0*x+i],a[c*x+i]);continue;}
		for(int p=c;p<y-1;p++)
		{
			if(a[p*x+i]==0)continue;
			for(int q=p+1;q<=y-1;q++)
			{
				if(a[q*x+i]==0)continue;
				if(a[p*x+i]==a[q*x+i])
				{
					a[p*x+i]++;
					a[q*x+i]=0;
					score+=b[a[p*x+i]];
					h=a[p*x+i]>h?a[p*x+i]:h;
					p=q;
				}
				break;
			}
		}
		for(int q1=0;q1<y-1;q1++)
		{
			if(a[q1*x+i]!=0)continue;
			for(int q2=q1+1;q2<=y-1;q2++)
				if(a[q2*x+i]!=0)
					{swap(a[q1*x+i],a[q2*x+i]);break;}
		}
	}
}
void lt()
{
	for(int i=0;i<=y-1;i++)
	{
		int d=0,c;
		for(int k=x-1;k>=0;k--)
			if(a[i*x+k]!=0){d++;c=k;}
		if(d==0)continue;
		if(d==1)
			{swap(a[i*x+0],a[i*x+c]);continue;}
		for(int p=c;p<x-1;p++)
		{
			if(a[i*x+p]==0)continue;
			for(int q=p+1;q<=x-1;q++)
			{
				if(a[i*x+q]==0)continue;
				if(a[i*x+p]==a[i*x+q])
				{
					a[i*x+p]++;
					a[i*x+q]=0;
					score+=b[a[i*x+p]];
					h=a[i*x+p]>h?a[i*x+p]:h;
					p=q;
				}
				break;
			}
		}
		for(int q1=0;q1<x-1;q1++)
		{
			if(a[i*x+q1]!=0)continue;
			for(int q2=q1+1;q2<=x-1;q2++)
				if(a[i*x+q2]!=0)
					{swap(a[i*x+q1],a[i*x+q2]);break;}
		}
	}
}
void dw()
{
	for(int i=0;i<=x-1;i++)
	{
		int d=0,c;
		for(int k=0;k<=y-1;k++)
			if(a[k*x+i]!=0){d++;c=k;}
		if(d==0)continue;
		if(d==1)
			{swap(a[(x-1)*x+i],a[c*x+i]);continue;}
		for(int p=c;p>0;p--)
		{
			if(a[p*x+i]==0)continue;
			for(int q=p-1;q>=0;q--)
			{
				if(a[q*x+i]==0)continue;
				if(a[p*x+i]==a[q*x+i])
				{
					a[p*x+i]++;
					a[q*x+i]=0;
					score+=b[a[p*x+i]];
					h=a[p*x+i]>h?a[p*x+i]:h;
					p=q;
				}
				break;
			}
		}
		for(int q1=y-1;q1>0;q1--)
		{
			if(a[q1*x+i]!=0)continue;
			for(int q2=q1-1;q2>=0;q2--)
				if(a[q2*x+i]!=0)
					{swap(a[q1*x+i],a[q2*x+i]);break;}
		}
	}
}
void rt()
{
	for(int i=0;i<=y-1;i++)
	{
		int d=0,c;
		for(int k=0;k<=x-1;k++)
			if(a[i*x+k]!=0){d++;c=k;}
		if(d==0)continue;
		if(d==1)
			{swap(a[i*x+x-1],a[i*x+c]);continue;}
		for(int p=c;p>0;p--)
		{
			if(a[i*x+p]==0)continue;
			for(int q=p-1;q>=0;q--)
			{
				if(a[i*x+q]==0)continue;
				if(a[i*x+p]==a[i*x+q])
				{
					a[i*x+p]++;
					a[i*x+q]=0;
					score+=b[a[i*x+p]];
					h=a[i*x+p]>h?a[i*x+p]:h;
					p=q;
				}
				break;
			}
		}
		for(int q1=x-1;q1>0;q1--)
		{
			if(a[i*x+q1]!=0)continue;
			for(int q2=q1-1;q2>=0;q2--)
				if(a[i*x+q2]!=0)
					{swap(a[i*x+q1],a[i*x+q2]);break;}
		}
	}
}
int upc()
{
	for(int i=0;i<=x-1;i++)
	{
		int d=0,c;
		for(int k=0;k<=y-1;k++)
			if(a[k*x+i]!=0){d++;c=k;}
		if(d==0)continue;
		if(d==1)
		{
			if(c!=0)return 1;
			continue;
		}
		for(int q1=c;q1>0;q1--)
		{
			int q2=q1-1;
			if(a[q2*x+i]==0||a[q1*x+i]==a[q2*x+i])return 1;
		}
	}
	return 0;
}
int ltc()
{
	for(int i=0;i<=y-1;i++)
	{
		int d=0,c;
		for(int k=0;k<=x-1;k++)
			if(a[i*x+k]!=0){d++;c=k;}
		if(d==0)continue;
		if(d==1)
		{
			if(c!=0)return 1;
			continue;
		}
		for(int q1=c;q1>0;q1--)
		{
			int q2=q1-1;
			if(a[i*x+q2]==0||a[i*x+q1]==a[i*x+q2])return 1;
		}
	}
	return 0;
}
int dwc()
{
	for(int i=0;i<=x-1;i++)
	{
		int d=0,c;
		for(int k=y-1;k>=0;k--)
			if(a[k*x+i]!=0){d++;c=k;}
		if(d==0)continue;
		if(d==1)
		{
			if(c!=y-1)return 1;
			continue;
		}
		for(int q1=c;q1<y-1;q1++)
		{
			int q2=q1+1;
			if(a[q2*x+i]==0||a[q1*x+i]==a[q2*x+i])return 1;
		}
	}
	return 0;
}
int rtc()
{
	for(int i=0;i<=y-1;i++)
	{
		int d=0,c;
		for(int k=x-1;k>=0;k--)
			if(a[i*x+k]!=0){d++;c=k;}
		if(d==0)continue;
		if(d==1)
		{
			if(c!=x-1)return 1;
			continue;
		}
		for(int q1=c;q1<x-1;q1++)
		{
			int q2=q1+1;
			if(a[i*x+q2]==0||a[i*x+q1]==a[i*x+q2])return 1;
		}
	}
	return 0;
}
int rd()
{
	int b,c=0;
	fill (s.begin(),s.begin()+x*y,0);
	for(int i=0;i<x*y;i++)
	{
		if(a[i]==0)s[c++]=i;
	}
	b=rand()%c;
	return s[b];
}
void q_q()
{
	qa.resize((qq+2)*x*y);
	qscore.resize(qq+2);
	qh.resize(qq+2);
	qscore[qq]=score;
	qh[qq]=h;
	for(int i=0;i<x*y;i++)
		qa[qq*x*y+i]=a[i];
	qq++;
}
void play()
{
	a[rd()]=rand()%5>0?1:2;
	int sqa=1;
	while(1)
	{
		if(sqa)
		{
			q_q();
			gt(0,0);
			draw();
			printf("score:%llu\n",score);
			printf("move:%lld\n",mv++);
		}
    	if(upc()==0&&ltc()==0&&rtc()==0&&dwc()==0)
    		break;
    	do
    	{
    		ch=getch();
	    	if(ch==-32)
	    		ch1=getch();
	    	if(ch>='A'&&ch<='Z')
	    		ch+=32;
		}while(!(ch==-32||ch=='w'||ch=='a'||ch=='s'||ch=='d'||ch=='q'||ch=='z'));
    	if(ch!=-32)ch1=0;
		if(ch=='w'||ch1==72)
    	{
    		if(upc()==0){sqa=0;continue;}
    		sqa=1;
    		up();
		}
    	if(ch=='a'||ch1==75)
    	{
    		if(ltc()==0){sqa=0;continue;}
    		sqa=1;
    		lt();
		}
    	if(ch=='d'||ch1==77)
    	{
    		if(rtc()==0){sqa=0;continue;}
    		sqa=1;
    		rt();
		}
    	if(ch=='s'||ch1==80)
    	{
    		if(dwc()==0){sqa=0;continue;}
    		sqa=1;
    		dw();
		}
    	if(ch=='z')
    	{
			sqa=0;
    		if(qq<=1)continue;
    		qq--;
    		h=qh[qq-1];
    		score=qscore[qq-1];
			for(int i=0;i<x*y;i++)
				a[i]=qa[(qq-1)*x*y+i];
			gt(0,y*2);
			for(int i=0;i<4;i++)
				printf("                      \n");
			gt(0,0);
			draw();
			printf("score:%llu\n",score);
			printf("move:%lld\n",mv-2);
			mv--;
			continue;
		}
    	if(ch=='q')
    	{
			sqa=0;
    		while(1)
    		{
    			if(dwc()==0&&ltc()==0)break;
    			if(dwc()==1)
    			{
    				dw();
    				a[rd()]=rand()%5>0?1:2;
					q_q();
					gt(0,0);
					draw();
					printf("score:%llu\n",score);
					printf("move:%lld\n",mv++);
				}
    			if(ltc()==1)
    			{
    				lt();
    				a[rd()]=rand()%5>0?1:2;
					q_q();
					gt(0,0);
					draw();
					printf("score:%llu\n",score);
					printf("move:%lld\n",mv++);
				}
			}
			continue;
		}
		a[rd()]=rand()%5>0?1:2;
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
	if(h>=11)
		printf("You Win!!\n");
	else
		printf("Game Over!!\n");
	Sleep(3000);
    system("pause");
	system("cls");
}

