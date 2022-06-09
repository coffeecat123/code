#include <bits/stdc++.h>
using namespace std;
int add(int a, int b) {
    while(b){
        int ta = a^b, tb = (a&b)<<1;
        a = ta, b =tb;
    }
    return a;
}
main()
{
    ios::sync_with_stdio(false);
    cout<<add(15,1);
}

