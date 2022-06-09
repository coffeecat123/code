#include <bits/stdc++.h>
using namespace std;
main()
{
	set<string> a;
	set<string>::iterator itch;
	string d;
	while(cin>>d)
	{
		if(d=="0")break;
		a.insert(d);
	}
	for(itch=a.begin();itch!=a.end();itch++)
		cout<<*itch<<endl;
}
