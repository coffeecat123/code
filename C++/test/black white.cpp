#include <bits/stdc++.h>
using namespace std;
int n,k;//k:一次移動幾個 ,n黑(1)或白(2)有幾個 
int h=0,fd=0;
string s[100],x;//s存放每次移動後的樣子 
int draw()
{
	cout<<x<<endl;
	for(int i=0;i<n;i++)
		cout<<s[i]<<endl;
	cout<<endl;
}
int qw(int ts,int wt,string x1)//ts:次數,wt:空白
{
	if(h==1)return 0;
	if(ts==n)
	{
		int g=0,g1=0,g2=0,l=0;
		while(x1[l]=='0')l++;
		for(int i=l;i<n*2+l;i++)
			if(x1[i]==(i%2?'1':'2'))g1++;
		for(int i=l;i<n*2+l;i++)
			if(x1[i]==(i%2?'2':'1'))g2++;
		g=max(g1,g2);
		if(g==n*2)
		{
			h=1;
			cout<<n<<":done!"<<endl;
			string st;
			for(int i=0;i<n*2+k;i++)st+='^';
			for(int i=0;i<n;i++)
			{
				for(int j=0;j<n*2+k;j++)
				{
					if(x[j]!=s[i][j])st[j]='-';
				}
			}
			cout<<st<<"\n";
			draw();
		}
		fd++;
		return 0;
	}
	//----------------------?
	string x2=x1;
	for(int i=0;i<=n*2;i++)
	{
		x1=x2;
		int ha=0;
		for(int j=i;j<i+k;j++)
			if(x1[j]=='0'){ha=1;break;}
		if(ha)continue;
		for(int l=0;l<k;l++)
			swap(x1[i+l],x1[wt+l]);
		int ad=0,ad1=0;
		if(x1==x)ad=1;
		while(ad1<ts)
			if(x1==s[ad1++]){ad=1;break;}
		if(ad)continue;
		s[ts]=x1;
		qw(ts+1,i,x1);
	}
}
int main()
{;
	cout<<"n:";
	cin>>n;
	cout<<"k:";
	cin>>k;
	x="";
	for(int i=0;i<n;i++)x+='1';
	for(int i=n;i<n*2;i++)x+='2';
	for(int i=n*2;i<n*2+k;i++)x+='0';
	qw(0,n*2,x);
	if(h==0)
		cout<<n<<":didn't find"<<endl;
	cout<<fd<<endl;
	system("pause");
}
