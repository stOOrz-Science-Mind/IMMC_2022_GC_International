#include <iostream>
#include <algorithm>
#include <cmath>
#include <cstdio>
#include <map>
#include <vector>
#include <cstring>
#include <istream>
#include <complex>
#include <ctime>

using namespace std;
int tgx[5][333],tgy[5][333];
int cnt[5],tot;
int seqx[333],seqy[333];
const int should[5]={0,75,84,84,75};
int main()
{
	int x4[333]={0,14,14,14,12,12,12,10,10,10,8,8,8,6,6,6,4,4,4,2,2,2,14,14,14,12,12,12,10,10,10,8,8,8,6,6,6,4,4,4,13,13,13,11,11,11,9,9,9,7,7,7,5,5,5,3,3,3,1,1,1,13,13,13,11,11,11,9,9,9,7,7,7,5,5,5};
	int y4[333]={0,23,24,25,23,24,25,23,24,25,23,24,25,23,24,25,23,24,25,23,24,25,29,28,27,29,28,27,29,28,27,29,28,27,29,28,27,29,28,27,23,24,25,23,24,25,23,24,25,23,24,25,23,24,25,23,24,25,23,24,25,29,28,27,29,28,27,29,28,27,29,28,27,29,28,27,29,28,27};
	for(int i=1;i<=75;i++) y4[i]--;
	for(int i=1;i<=75;i++)
	{
		tgx[4][i]=x4[i];
		tgy[4][i]=y4[i];
	}
	for(int i=1;i<=75;i++)
	{
		tgx[1][i]=tgx[4][i];
		tgy[1][i]=29-tgy[4][i];
	}
	int x3[333]={0,14,14,14,12,12,12,10,10,10,8,8,8,6,6,6,4,4,4,2,2,2,14,14,14,12,12,12,10,10,10,8,8,8,6,6,6,4,4,4,2,2,2,13,13,13,11,11,11,9,9,9,7,7,7,5,5,5,3,3,3,1,1,1,13,13,13,11,11,11,9,9,9,7,7,7,5,5,5,3,3,3,1,1,1};
	int y3[333]={0,15,16,17,15,16,17,15,16,17,15,16,17,15,16,17,15,16,17,15,16,17,21,20,19,21,20,19,21,20,19,21,20,19,21,20,19,21,20,19,21,20,19,15,16,17,15,16,17,15,16,17,15,16,17,15,16,17,15,16,17,15,16,17,21,20,19,21,20,19,21,20,19,21,20,19,21,20,19,21,20,19,21,20,19};
	for(int i=1;i<=84;i++)
	{
		tgx[3][i]=x3[i];
		tgy[3][i]=y3[i];
	}
	for(int i=1;i<=75;i++)
	{
		tgx[2][i]=tgx[3][i];
		tgy[2][i]=29-tgy[3][i];
	}
	for(;cnt[4]<=20;)
	{
		cout<<4;
		seqx[++tot]=tgx[4][++cnt[4]];
		seqy[tot]=tgy[4][cnt[4]];
	}
	for(;cnt[3]<=14;)
	{
		cout<<3;
		seqx[++tot]=tgx[3][++cnt[3]];
		seqy[tot]=tgy[3][cnt[3]];
	}
	for(;cnt[4]<=23;)
	{
		cout<<4;
		seqx[++tot]=tgx[4][++cnt[4]];
		seqy[tot]=tgy[4][cnt[4]];
	}
	for(;cnt[3]<=17;)
	{
		cout<<3;
		seqx[++tot]=tgx[3][++cnt[3]];
		seqy[tot]=tgy[3][cnt[3]];
	}
	for(;cnt[2]<=17;)
	{
		cout<<2;
		seqx[++tot]=tgx[2][++cnt[2]];
		seqy[tot]=tgy[2][cnt[2]];
	}
	for(;cnt[3]<=19;)
	{
		cout<<3;
		seqx[++tot]=tgx[3][++cnt[3]];
		seqy[tot]=tgy[3][cnt[3]];
	}
	for(;cnt[4]<=24;)
	{
		cout<<4;
		seqx[++tot]=tgx[4][++cnt[4]];
		seqy[tot]=tgy[4][cnt[4]];
	}
	for(;cnt[1]<=14;)
	{
		cout<<1;
		seqx[++tot]=tgx[1][++cnt[1]];
		seqy[tot]=tgy[1][cnt[1]];
	}
	while(1)
	{
		bool flag=0;
		for(int i=1;i<=4;i++)
			if(cnt[i]<should[i]) flag=1;
		if(!flag) break;
		for(int i=1;i<=4;i++)
		{
			if(cnt[i]<should[i])
			{
				cout<<i;
				seqx[++tot]=tgx[i][++cnt[i]];
				seqy[tot]=tgy[i][cnt[i]];
			}
		}
	}
	cout<<endl<<tot<<endl;
	for(int i=1;i<=318;i++) cout<<seqx[i]<<" ";
	cout<<endl;
	for(int i=1;i<=318;i++) cout<<seqy[i]<<" ";
}
