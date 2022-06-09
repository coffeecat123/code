//#include <bits/stdc++.h>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <cstring>
#include <cstdio>
#include <cmath>
#include <set>
#include <vector>
#include <stack>
#include <map>
#include <utility>
#include <algorithm>
using namespace std;
int w=0,s[10]={0},sw[]={1,2,3,4},l[4][10],f[20];
long int w2;
long long int w3;
unsigned long long w4;
char ch='a',chr[100]="asscdse\0";
bool bl;
float fl;
double dl=pow(2,100);
string str="123";
stringstream ss;
set<int> q;
set<int>::iterator itch;
vector<int> v(4);
vector<vector<int> > vect;
vector<int>::iterator itr;
stack<int> z;
map<string,string> mp;
map<string,string>::iterator mtr;
pair<string,int> p[5];
struct stu{
	int a;
	string w;
	char q;
};
struct stu qwe;
void qws(int qwa);//先宣告此函數 
int find(int x)
{
	if(f[x]==x)return x;//回傳 x 
	return f[x]=find(f[x]);//壓縮路徑 
}
main()
{
	//ios::sync_with_stdio(false);
	//cin.tie(0);
	qwe.a=0;
	qwe.q='a';
	qwe.w=123;
	ss<<str;
	ss>>w;
	sizeof(w);//記憶體大小 
	str.length();//字串長度 
	pow(2,10);//2的10次方 
	sqrt(16);//根號16 
	swap(sw[0],sw[1]);//交換 
	sort(sw,sw+4);//排序 
	fill(sw,sw+3,5);//填滿 
	reverse(sw+1,sw+2);//翻轉 
	memset(l,1,sizeof(l));//只能填1byte的 
	v.begin();
	v.end();
	v.push_back(1);
	v.resize(10);//重設大小 
	v.size();
	v.back();
	q.insert(25);
	q.insert(34);
	q.insert(21);
	q.begin();
	q.end();
	z.empty();//bool是否是空的 
	z.push(3);
	z.push(2);
	z.push(4);
	z.pop();//刪掉頂端的 
	z.top();//頂端的 
	z.size();
	mp["a"]="e";
	cout<<mp["a"]<<endl;
	mtr=mp.find("a");
	mp.erase(mtr);
	int n = mp.erase("1");//如果刪除了會返回1，否則返回0
	mp.end();
	mp.begin();
	mp.clear();
	p[0].first="ac";
	p[0].second=123;
	p[1].first="ac";
	p[1].second=122;
	p[2].first="acb";
	p[2].second=123;
	sort(p,p+5);//二維排序 
	for(int i=0;i<5;i++)
		cout<<p[i].first<<" "<<p[i].second<<"\n";
	w++;//w+=1 w=w+1
	w+=1*2%3/2;//+-*/加減乘除%取餘數 
	w>0?1:0;//判斷 
	w=2^3&4|5;//
	w=~3;//反 
	w>>=2;//
	w<<=2;//
	cout<<chr;
	cin>>w;
	cout<<setbase(16)<<setfill('*')<<setw(14)<<w<<endl;
	cout<<setfill('*')<<setw(10)<<"\n";
	cout<<fixed<<setprecision(3)<<fl<<"\n";
    for(itr=v.begin();itr!=v.end();itr++)
        cout<<*itr<<" ";
    for(itch=q.begin();itch!=q.end();itch++)
        cout<<*itch<<" ";
    while(!z.empty())
    {
    	cout<<z.top()<<" ";
    	z.pop();
	}
	cout<<setbase(10);
    while(cin>>w)//(ctrl+z) to break
    	cout<<setfill('#')<<setw(w)<<"\0";
    cout<<scanf("%d %c",&w,&ch)<<endl;//2
	while(scanf("%d %c",&w,&ch)!=EOF)
	{//                        (ctrl+z)
		printf("\t%s %c %d %lld %llu\n",chr,ch,w,w3,w4);
	}//      \t定位%s字元陣列%c=char%d=int 
	qws(2);//2是參數 
	while(1)//無限迴圈
	{
		break;//出迴圈 
		continue;//重新判斷 
	}
	for(int i=0;i<10;i++)
	{// 初始值;條件式;
		if(i==5)break; 
	}
	int hg=0;
	do
	{
		hg++;
	}while(hg<1);//判斷式成立，do 
}
void qws(int qwa)//無回傳值 
{//參數(qwa)只有在此函數中有效 
	cout<<qwa;
	return;//直接跳出函數 
}
