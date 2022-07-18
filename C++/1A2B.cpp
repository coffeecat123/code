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
		cout<<"請輸入("<<n
			<<"個數字[0~9][數字不重複]):";
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
			cout<<"恭喜你猜對了\n你一共猜了"
				<<t-1<<"次\n要離開遊戲嗎?(y/n):";
			cin>>x;
			if(x=='y')break;
			a=ga();
			t=1;
		}
	}
} 
