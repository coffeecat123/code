#include <stack>
#include <iostream>
using namespace std;
main()
{
	stack <int> a;
	for(int i=0;i<10;i++)
		a.push(i);
	a.push(1);
	a.push(2);
	a.pop();
	cout<<a.size()<<endl;
	while(!a.empty())
	{
		cout<<a.top()<<endl;
		a.pop();
	}
}
