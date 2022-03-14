#include<bits/stdc++.h>
using namespace std;
struct node
{
	int x,y,sx,sy,id;
}p[1099];
int newid[1099],cnt;
bool used[1099];
bool cmp(node a,node b)
{
	return a.id<b.id;
}
int main()
{
	srand((unsigned)time(NULL));
	freopen("random2.txt","r",stdin);
	freopen("discompliance_random.txt","w",stdout);
	for(int i=1;i<=189;i++) scanf("%d%d%d%d",&p[i].sx,&p[i].sy,&p[i].x,&p[i].y);
	while(cnt<189)
	{
		int x=rand()%189+1;
//		cout<<x<<endl;
		if(!used[x])
		{
			used[x]=1;
			p[++cnt].id=x;
		}
	}
	cnt=0;
	memset(used,0,sizeof(used));
	sort(p+1,p+190,cmp);
	while(cnt<189)
	{
		int x=rand()%189+1;
		cout<<x<<endl;
		if(!used[x])
		{
			used[x]=1;
			p[++cnt].id=x;
		}
	}
	for(int i=1;i<=189;i++) printf("%d %d %d %d %d\n",p[i].id,p[i].sx,p[i].sy,p[i].x,p[i].y);
	return 0;
}
