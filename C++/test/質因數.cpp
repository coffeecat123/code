#include <iostream> 
using namespace std;
int main()
{
	ios::sync_with_stdio(false);
	//cin.tie(0);
	int a,b;
	while(cin>>b)
	{
		a=2;
		while(b>1)
		{
			if(b%a==0)
			{
				cout<<a<<" ";
				b/=a;
			}
			else a++;
		}
		cout<<"\n";
	}
}
