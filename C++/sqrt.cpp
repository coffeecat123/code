#include <iostream>
#include <cmath>
#include <cstdio>
using namespace std;
int main()
{
	long long int a,b,c,i,d,e;
	while(cin>>a)
	{
		cout<<sqrt(a)<<"\n";
		c=d=0;
		for(b=1;a/b>0;)b*=100;
		b/=100;
		for(int j=0;j<19;j++,b/=100)
		{
			if(b<1)
			{
				a*=100;
				b=1;
			}
			for(i=9;i>0;i--)
				if((10*c+i)*i<=a/b)
					break;
			e=(10*c+i)*i;
			if(b>0)e*=b;
			cout<<i;
			a-=e;
			c*=10;
			c+=2*i;
			if(a==0 and b<=1)break;
			if(b<=1 and d==0)
			{
				cout<<".";
				d=1;
			}
		}
		cout<<endl;
	}
}
