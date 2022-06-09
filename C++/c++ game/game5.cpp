//test kbhit() 
#include <stdio.h>
#include <conio.h>
#include <windows.h>
#include <iostream>
#include <time.h>
#include <vector>
#include <set>
#include <math.h>
using namespace std;
main()
{
	int a,b;
	while(1)
	{
		a=kbhit();
		if(a)
		{
			a=getch();
			if(a==224)
			{
				a=getch();
				cout<<a<<endl;
			}
		}
	}
}

