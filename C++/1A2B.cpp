#include <bits/stdc++.h>
using namespace std;
int n=3;
string ga(){
	vector<int> q;
	for(int i=0;i<10;i++)q.push_back(i);
	string a="";
	for(int i=0;i<n;i++){
		int l=rand()%q.size(),w=q[l];
		q.erase(q.begin()+l);
		a+=w+'0';
	}
	return a;
}
bool iw(string b){
	if(b.length()>n)return 1;
	for(int i=0;i<n-1;i++)
		for(int j=i+1;j<n;j++)
			if(b[i]==b[j])return 1;
	return 0;
}
int main(){
	srand(time(NULL));
	string a,b;
	int t=1;
	a=ga();
	//cout<<a<<"\n";
	while(1){
		cout<<"�п�J("<<n
			<<"�ӼƦr[0~9][�Ʀr������]):";
		cin>>b;
		if(iw(b))continue;
		int A=0,B=0;
		for(int i=0;i<n;i++)
			for(int j=0;j<n;j++)
				if(a[i]==b[j])i==j?A++:B++;
		cout<<t<<"."<<b<<" "<<A<<"A"<<B<<"B\n";
		t++;
		if(A==n){
			char x;
			cout<<"���ߧA�q��F\n�A�@�@�q�F"
				<<t-1<<"��\n�n���}�C����?(y/n):";
			cin>>x;
			if(x=='y')break;
			a=ga();
			t=1;
		}
	}
} 
