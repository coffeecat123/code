#include <bits/stdc++.h>
using namespace std;
int z,q[10001][10001],x[100000],y[100000];
pair<int,int> p[10000];
int sa(int a,int b);
int wa(int a,int b)
{
	for(int i=-2;i<=2;i++)
		for(int j=-2;j<=2;j++)
			sa(a+i,b+j);
}
int sa(int a,int b)
{
	if(q[a][b]==1)
	{
		q[a][b]=0;
		p[z].first=a;
		p[z].second=b;
		z++;
		wa(a,b);
	}
}
int main()
{
	ios::sync_with_stdio(false);
	//cin.tie(0);
	int a,b,c,row,col,d,e;
	while(cin>>a>>b>>c)
	{
		memset(q,0,sizeof(q));
		z=0;
		while(c--)
		{
			cin>>row>>col;
			q[row][col]=1;
		}
		/*/
		for(int i=0;i<a;i++)
		{
			for(int k=0;k<b;k++)
			{
				cout<<q[i][k]<<" ";
			}
			cout<<"\n";
		}
		/*/
		cin>>d>>e;
		wa(d,e);
		sort(p,p+z);
		for(int i=0;i<z;i++)
			cout<<p[i].first<<" "<<p[i].second<<"\n";
	}
}
