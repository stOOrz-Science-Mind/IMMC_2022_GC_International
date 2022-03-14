#include<bits/stdc++.h>
using namespace std;
double sum,fc,y[1009];
int main()
{
	srand((unsigned)time(NULL));
	freopen("disobey.txt","w",stdout);
	for(int i=1;i<=189;i++)
	{
		int x=rand()%6001;
		y[i]=(double)x/1000.0;
		if(i<189)cout<<y[i]<<",";
		else cout<<y[i];
		sum+=y[i];
	}
	cout<<endl;
	sum/=189.0;
	for(int i=1;i<=189;i++)
	{
		fc+=(y[i]-sum)*(y[i]-sum);
	}
	cout<<fc/189;
}
