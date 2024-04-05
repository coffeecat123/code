#include <bits/stdc++.h>
using namespace std;
int n;//一般是3 
vector <vector<int> > a,v,v2;
/*
a[x][0]==0 ->這格是空的 
0代表有可能 

數對唯餘法
唯一法
宮摒餘法
二餘法
三餘法
四餘法
數對摒除法
區塊(或單元)數對唯餘法
唯餘法
行列摒餘法
矩形摒除法
數偶摒除法
猜測
*/
/*
範例輸入
3
000503008
204060090
010000000
070000050
501006300
090010000
000200900
700000000
605040020
*/ 
int pr(int b)
{
	for(int i=0;i<n*n*n*n;i++)
	{
		for(int j=0;j<=0;j++)
			cout<<v2[b][i*(n*n+1)+j]<<" ";
		//cout<<"    ";
		if((i+1)%(n*n)==0)cout<<"\n";
	}
	cout<<"\n";
}
int de(int i,int b)
{
	for(int j=1;j<=n*n;j++)a[i][j]=1;
	int x=i%(n*n),y=i/(n*n),
		c=x/n*n+y/n*n*(n*n);
	for(int k=0;k<n;k++)
		for(int l=0;l<n;l++)
			a[c+l+k*(n*n)][b]=1;
	for(int k=0;k<n*n;k++)
	{
		a[x+k*(n*n)][b]=1;
		a[k+y*(n*n)][b]=1;
	}
}
int w1()//唯餘法
{
	for(int i=0;i<n*n*n*n;i++)
	{
		if(a[i][0]>0)continue;
		int b=0,c;
		for(int k=1;k<=n*n;k++)
		{
			b+=a[i][k];
			if(a[i][k]==0)c=k;
		}
		if(b==n*n-1)
		{
			//cout<<setw(2)<<t++<<":("<<i/(n*n)+1<<","<<i%(n*n)+1<<")="<<c<<" 唯餘法\n";
			a[i][0]=c;
			de(i,c);
		}
	}
}
int w2()//行列宮摒餘法 
{
	//行 
	for(int i=0;i<n*n;i++)//x
	{
		int c[n*n+1]={0},d[n*n+1];
		for(int j=0;j<n*n;j++)//y
		{
			for(int k=1;k<=n*n;k++)
			{
				c[k]+=(a[i+j*(n*n)][k]==0);
				if(a[i+j*(n*n)][k]==0)d[k]=j;
			}
		}
		for(int k=1;k<=n*n;k++)
		{
			if(c[k]==1)
			{
				//cout<<setw(2)<<t++<<":("<<d[k]+1<<","<<i+1<<")="<<k<<" 行摒餘法 \n";
				a[i+d[k]*(n*n)][0]=k;
				de(i+d[k]*(n*n),k);
			}
		}
	}
	//列 
	for(int i=0;i<n*n;i++)//y
	{
		int c[n*n+1]={0},d[n*n+1];
		for(int j=0;j<n*n;j++)//x
		{
			for(int k=1;k<=n*n;k++)
			{
				c[k]+=(a[j+i*(n*n)][k]==0);
				if(a[j+i*(n*n)][k]==0)d[k]=j;
			}
		}
		for(int k=1;k<=n*n;k++)
		{
			if(c[k]==1)
			{
				//cout<<setw(2)<<t++<<":("<<i+1<<","<<d[k]+1<<")="<<k<<" 列摒餘法 \n";
				a[d[k]+i*(n*n)][0]=k;
				de(d[k]+i*(n*n),k);
			}
		}
	}
	//宮 
	for(int i=0;i<n*n;i++)
	{
		int c[n*n+1]={0},d[n*n+1];
		for(int j=0;j<n;j++)//y
		{
			for(int k=0;k<n;k++)//x
			{
				for(int l=1;l<=n*n;l++)
				{
					int e=k+i%n*n+(i/n*n+j)*(n*n);
					if(a[e][0]>0)continue;
					c[l]+=(a[e][l]==0);
					if(a[e][l]==0)d[l]=e;
				}
			}
		}
		for(int k=1;k<=n*n;k++)
		{
			if(c[k]==1)
			{
				//cout<<setw(2)<<t++<<":("<<d[k]/(n*n)+1<<","<<d[k]%(n*n)+1<<")="<<k<<" 宮摒餘法 \n";
				a[d[k]][0]=k;
				de(d[k],k);
			}
		}
	}
}
int w3()//區塊宮摒餘法 
{
	for(int p=1;p<=n*n;p++)
	{
		//行 
		for(int i=0;i<n;i++)//x
		{
			for(int j=0;j<n;j++)//y
			{
				int b=0,e=0;
				for(int k=0;k<n;k++)//x
				{
					for(int l=0;l<n;l++)//y
					{
						if(a[i*n+j*n*(n*n)+k+l*(n*n)][p]==0)
						{
							e++;
							b=k;
							break;
						}
					}
				}
				if(e==1)
				{
					for(int l=0;l<n*n;l++)
					{
						if(l>=j*n&&l<(j+1)*n)continue;
						a[b+i*n+l*(n*n)][p]=1;
					}
				}
			}
		}
		//列 
		for(int i=0;i<n;i++)//y
		{
			for(int j=0;j<n;j++)//x
			{
				int b=0,e=0;
				for(int k=0;k<n;k++)//y
				{
					for(int l=0;l<n;l++)//x
					{
						if(a[j*n+i*n*(n*n)+l+k*(n*n)][p]==0)
						{
							e++;
							b=k;
							break;
						}
					}
				}
				if(e==1)
				{
					for(int l=0;l<n*n;l++)
					{
						if(l>=j*n&&l<(j+1)*n)continue;
						a[l+(b+i*n)*(n*n)][p]=1;
					}
				}
			}
		}
	}
}
int w4()//單元宮摒餘 
{
	for(int p=1;p<=n*n;p++)
	{
		//行  
		for(int i=0;i<n;i++)//x
		{
			int b[n]={0},d=-1,e;
			for(int j=0;j<n;j++)//y
			{
				for(int k=0;k<n;k++)//x
				{
					int e=0;
					for(int l=0;l<n;l++)//y
					{
						if(a[i*n+j*n*(n*n)+k+l*(n*n)][p]==0)
						{
							e=1;
							break;
						}
					}
					if(e)b[j]|=(1<<k);
				}
			}
			for(int h=0;h<n;h++)
			{
				int c=0;
				for(int j=0;j<n;j++)
				{
					if(((b[h]&(1<<j))!=(b[(h+1)%n]&(1<<j)))){c=0;break;}
					if((b[h]&(1<<j))>0)c++;
					else e=j;
				}
				if(c==2){d=h;break;}
			}
			
			if(d!=-1)
			{
				for(int k=0;k<n;k++)//x
				{	
					if(k==e)continue;
					for(int j=0;j<n;j++)//y
						a[i*n+k+j*(n*n)+(d+2)%n*n*(n*n)][p]=1;
				}
			}
		}
		//列 
		for(int i=0;i<n;i++)//y
		{
			int b[n]={0},d=-1,e;
			for(int j=0;j<n;j++)//x
			{
				for(int k=0;k<n;k++)//y
				{
					int e=0;
					for(int l=0;l<n;l++)//x
					{
						if(a[j*n+i*n*(n*n)+l+k*(n*n)][p]==0)
						{
							e=1;
							break;
						}
					}
					if(e)b[j]|=(1<<k);
				}
			}
			for(int h=0;h<n;h++)
			{
				int c=0;
				for(int j=0;j<n;j++)
				{
					if(((b[h]&(1<<j))!=(b[(h+1)%n]&(1<<j)))){c=0;break;}
					if((b[h]&(1<<j))>0)c++;
					else e=j;
				}
				if(c==2){d=h;break;}
			}
			if(d!=-1)
			{
				for(int k=0;k<n;k++)//y
				{	
					if(k==e)continue;
					for(int j=0;j<n;j++)//x
						a[(d+2)%n*n+j+k*(n*n)+i*n*(n*n)][p]=1;
				}
			}
		}
	}
}
int w5()//二餘法
{
	for(int i=0;i<n;i++)
	{
		for(int j=0;j<n;j++)
		{
			int e[(n*n+1)]={0},h=j*n+i*n*(n*n);
			for(int k=0;k<n*n-1;k++)
			{
				if(a[h+k%n+k/n*(n*n)][0]>0)continue;
				for(int m=k+1;m<n*n;m++)
				{
					if(a[h+m%n+m/n*(n*n)][0]>0)continue;
					int g=0,g2[(n*n+1)],f=0;
					for(int l=1;l<=n*n;l++)
						if(a[h+m%n+m/n*(n*n)][l]
							!=a[h+k%n+k/n*(n*n)][l]){f=1;break;}
					if(f)continue;
					for(int l=1;l<=n*n;l++)
						if(a[h+m%n+m/n*(n*n)][l]==0
							&&a[h+k%n+k/n*(n*n)][l]==0)g2[g++]=l;
					if(g==2)
					{
						for(int l=0;l<n*n;l++)
						{
							if(l==k||l==m)continue;
							a[h+l%n+l/n*(n*n)][g2[0]]=1;
							a[h+l%n+l/n*(n*n)][g2[1]]=1;
						}
						if(k%n==m%n)
						{
							for(int l=0;l<n*n;l++)
							{
								if(l==k/n+i*n||l==m/n+i*n)continue;
								a[j*n+k%n+l*(n*n)][g2[0]]=1;
								a[j*n+k%n+l*(n*n)][g2[1]]=1;
							}
						}
						if(k/n==m/n)
						{
							for(int l=0;l<n*n;l++)
							{
								if(l==k%n+j*n||l==m%n+j*n)continue;
								a[l+(k/n+i*n)*(n*n)][g2[0]]=1;
								a[l+(k/n+i*n)*(n*n)][g2[1]]=1;
							}
						}
						for(int l=1;l<=n*n;l++)
						{
							if(l==g2[0]||l==g2[1])continue;
							a[h+k%n+k/n*(n*n)][l]=1;
							a[h+m%n+m/n*(n*n)][l]=1;
						}
						break;
					}
				}
			}
		}
	}
}
int p(int b,int c,int d)
{
	int aa[n*n*n*n*(n*n+1)];
	for(int i=0;i<n*n*n*n*(n*n+1);i++)
		a[i/(n*n+1)][i%(n*n+1)]=v[b][i];
	if(c!=-1)
	{
		a[c][0]=d;
		de(c,d);
	}
	while(1)
	{
		int e=0;
		for(int i=0;i<n*n*n*n;i++)
			for(int j=0;j<=n*n;j++)
				aa[i*(n*n+1)+j]=a[i][j];
		
		w1();//唯餘法 
		w2();//行列宮摒餘法 
		//w3();//區塊宮摒餘法 
		//w4();//單元宮摒餘 
		//w5();//二餘法 
		for(int i=0;i<n*n*n*n;i++)
		{
			for(int j=0;j<=n*n;j++)
				if(aa[i*(n*n+1)+j]!=a[i][j]){e=1;break;}
			if(e)break;
		}
		if(e==0)break;
	}
	for(int i=0;i<n*n*n*n*(n*n+1);i++)
		v[b][i]=a[i/(n*n+1)][i%(n*n+1)];
	int g=0;
	for(int i=0;i<n*n*n*n;i++)
	{
		if(a[i][0]==0)
		{
			g=1;
			break;
		}
	}
	if(g)
	{
		int f;
		for(int i=0;i<n*n*n*n;i++)
		{
			if(a[i][0]==0)
			{
				f=i;
				break;
			}
		}
		for(int i=1;i<=n*n;i++)
		{
			v.push_back(vector <int>(n*n*n*n*(n*n+1),0));
			for(int i=0;i<n*n*n*n*(n*n+1);i++)
				v[v.size()-1][i]=v[b][i];
			if(v[b][f*(n*n+1)+i]==1)continue;
			p(v.size()-1,f,i);
		}
	}
	else
	{
		v2.push_back(vector <int>(n*n*n*n*(n*n+1),0));
		for(int i=0;i<n*n*n*n*(n*n+1);i++)
			v2[v2.size()-1][i]=v[b][i];
	}
}
int main()
{
	while(cin>>n)
	{
		a.clear();
		v.clear();
		v2.clear();
		for(int i=0;i<n*n*n*n;i++)
			a.push_back(vector <int>(n*n+1,0));
		for(int i=0;i<n*n;i++)
		{
			string s;
			cin>>s;
			for(int j=0;j<n*n;j++)
			{
				int idx=i*n*n+j;
				a[idx][0]=s[j]-'0';
				if(a[idx][0])
					de(idx,a[idx][0]);
			}
		}
		v.push_back(vector <int>(n*n*n*n*(n*n+1),0));
		for(int i=0;i<n*n*n*n*(n*n+1);i++)
			v[0][i]=a[i/(n*n+1)][i%(n*n+1)];
		p(0,-1,0);
		if(v2.size()==0)
			cout<<"NO SOLUTION\n";
		else
		{
			cout<<v2.size()<<"\n";
			for(int i=0;i<v2.size();i++)
				pr(i);
		}
	}
}
