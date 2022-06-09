#include <iostream>
using namespace std;
struct s{
	int a;
	char w;
};
struct s x,y[4];
main()
{
	y[0].a=123;
	x.w='s';
	cout<<y[1].a<<endl;
	cout<<sizeof(x)<<endl;
}
