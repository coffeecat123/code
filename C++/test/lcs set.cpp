#include <iostream>
#include <cstring>
#include <set>
using namespace std;
string s1,s2,s3;
set<string> a;
set<string>::iterator itch;
int lcs[51][51],map[51][51],qw;
void pr(int x,int y)
{
	//cout<<"x:"<<x<<" y:"<<y<<"\t"<<map[x][y]<<endl;
	if(x==0||y==0)return;
	if(map[x][y]==3){s3+=s1[x-1];pr(x-1,y-1);}
	else if(map[x][y]==1)pr(x-1,y);
	else if(map[x][y]==2)pr(x,y-1);
}
void aw(int x,int y,int h,string sa)
{
	if(h==qw)
	{
		string dz="";
		for(int i=sa.length()-1;i>=0;i--)
			dz+=sa[i];
		a.insert(dz);
		return;
	}
	if(x==0||y==0)return;
	if(map[x][y]==3)
		aw(x-1,y-1,h+1,sa+s1[x-1]);
	else if(map[x][y]!=0)
	{
		aw(x-1,y,h,sa);
		aw(x,y-1,h,sa);
	}
}
main()
{
	ios::sync_with_stdio(0);
	cin.tie(0);
	int m,n,i,j;
	while(getline(cin,s1))
	{
		getline(cin,s2);
		m=s1.length();
		n=s2.length();
		s3="";
		memset(lcs,0,sizeof(lcs));
		memset(map,0,sizeof(map));
		for(i=1;i<=m;i++)
		{
			for(j=1;j<=n;j++)
			{
				if(s1[i-1]==s2[j-1])
					{lcs[i][j]=lcs[i-1][j-1]+1;map[i][j]=3;}
				else
				{
					if(lcs[i-1][j]>lcs[i][j-1])
						{lcs[i][j]=lcs[i-1][j];map[i][j]=1;}
					else
						{lcs[i][j]=lcs[i][j-1];map[i][j]=2;}
				}
				/*
				for(int p=0;p<=n;p++)
				{
					for(int l=0;l<=m;l++)
						cout<<lcs[l][p]<<" ";
					cout<<endl;
				}
				cout<<endl;
				*/
			}
		}
		pr(m,n);
		qw=s3.length();
		a.clear();
		aw(m,n,0,"");
		for(itch=a.begin();itch!=a.end();itch++)
			cout<<*itch<<" ";
		cout<<"\n";
	}
}
