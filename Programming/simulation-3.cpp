#include<bits/stdc++.h>
#define nega1 999
#define nega2 998
using namespace std;
int total_seated,n_people;
double dis[100009];//i号与i+1号的距离 
struct passenger
{
	double x,y;//当前坐标 
	double seatx,seaty;//座位 
	int status;//0=移动 1=放行李 2=就座 
	int seated;//是否就座 
	int id;
	double luggage_timeleft;//放行李剩余时间
	double luggage; 
	int status2_to;//记录是否正在给别人让座，变量的值为让座对象 
	int status2_from;//记录是否有人给此人让座 
	double velocity; 
}p[100009];
struct cell
{
	double xcell,ycell;
	int status_cell;//0=座位 1=过道 
	bool occupied;//如果是座位的话 是否已经有人了 
}cells[3005][3005];
bool blocked[3005][3005];
bool aisle_occ[3005];//过道占据情况 
int time_tot;
double v0=1;
string rev(string b)
{
	string a=b;
	for(int i=0;i<=a.size()/2;i++)
	{
		char t=a[i];
		a[i]=a[a.size()-i];
		a[a.size()-i]=t;
	}
	return a;
}
string str(int a)
{
	int j=0;
	string s1,s2;
	s1=s2="000";
	while(a)
	{
		s1[j++]=a%10+'0';
		a/=10;
	}
	cout<<s1;
	return rev(s1)+s1[0];
}
int d=4;//能见度 
bool near(double a,double b)
{
	return abs(a-b)<=0.1;
}
void move(int num)
{
//	cout<<"sbsbsbsb "<<num<<endl;
	int xx=int(p[num].x);
	if(!blocked[xx+1][1000])//前方没有堵住
	{
		int tot_people_in_d=0;
//		int tot_people_in_i=0;
		int i;
		for(i=1;i<=d&&!blocked[xx+i];i++)
		{
			if(aisle_occ[xx+i]) tot_people_in_d++;
			//i代表前方d距离内第一个在放行李的人距离num号的位置  
		}
//		for(int j=1;j<i;j++)
//		{
//			if(aisle_occ[xx+j]) tot_people_in_i++;
//		}
//		cout<<"^^"<<i<<endl;
		p[num].velocity=v0*(d-tot_people_in_d)/d;
//		cout<<v0<<"::\n";
//		cout<<"&&\n";
////		if(num>1&&!p[num-1].seated) p[num].velocity=min(p[num].velocity,p[num-1].x-p[num].x);
////		cout<<p[num-1].x<<"~~\n";
//		cout<<"()"<<p[num].velocity<<endl;
//		cout<<"---==="<<p[1].velocity<<endl;
	}
	else p[num].velocity=0;
	p[num].x+=p[num].velocity;
//	cout<<num<<" "<<p[num].x<<" "<<p[num].y<<"[][][][][][][]\n"; 
}
int main()
{
//	freopen("passenger_data.txt","w",stdout);
//	for(int i=1;i<=1000;i++) cout<<blocked[i][0];
	freopen("random3.txt","r",stdin);
	n_people=189;
	for(int i=1;i<=n_people;i++)
	{
		cin>>p[i].id>>p[i].seatx>>p[i].seaty>>p[i].x>>p[i].y;
		p[i].seatx+=1000;
		p[i].x+=1000;
		p[i].seaty+=1000;
		p[i].y+=1000;
//		cout<<i<<" "<<p[i].x<<" "<<p[i].y<<" "<<p[i].seatx<<" "<<p[i].seaty<<"[][][][][][][]\n"; 
	}
	freopen("time_l.txt","r",stdin);
	for(int i=1;i<=n_people;i++) cin>>p[i].luggage;
	while(total_seated!=n_people)
	{
//		cout<<"**";
		time_tot++;//枚举最小单元时间 
		string s=str(time_tot)+".txt";
		cout<<s<<endl;
		freopen(s,"w",stdout);
		for(int i=1;i<=n_people;i++)
		{
//			cout<<"]]";
//			cout<<"-"<<i<<"-"<<endl;
//			if(!p[i].seated)
//			{
//				cout<<"fuck ccf "<<i<<endl;
				if(p[i].status==1)
				{
					if(p[i].luggage_timeleft<=0) {p[i].status=2;p[i].x=p[i].seatx;p[i].y=p[i].seaty;cells[int(p[i].x)][(int(p[i].y)>0)?int(p[i].y):int(p[i].y)+1000].occupied=1;blocked[int(p[i].x)][0]=0;total_seated++;}//注：放完行李后1单位的时间后完成入座，就座后状态变量更新 
					p[i].luggage_timeleft-=1;
				}
//				else if(p[i].status==2)
//				{
//					int to=p[i].status2_to;
//				}
				else if(p[i].status==0)
				{
					if(near(p[i].x,p[i].seatx))//已经抵达座位，准备就座 
					{
//						cout<<"{}";
						double time_wait=1;
						p[i].status=1;
						if(p[i].seaty>1000)
						{
							if(cells[int(p[i].seatx)][1002].occupied&&p[i].seaty==1003) time_wait=2;//最内侧座位且中间座位有人 
							else if(cells[int(p[i].seatx)][1001].occupied) time_wait=1;
						}
						else
						{
							if(cells[int(p[i].seatx)][998].occupied&&p[i].seaty==997) time_wait=2;//-2=nega2 -1=-1 
							else if(cells[int(p[i].seatx)][999].occupied) time_wait=1;
						}
						p[i].luggage_timeleft=p[i].luggage+time_wait;//计算出放行李+让座等就座前准备的时间
						blocked[int(p[i].x)][0]=1;//准备放行李，当前方格无法通过 
					}
					else
					{
//						cout<<"---------------------------------------------\n";
						move(i);
					}
				}
//			}
//			cout<<total_seated<<" !!!!!!!!!!!!!!!!!!!!!!!\n";
//			for(int i=1;i<=n_people;i++) cout<<p[i].status<<" ";
//			else cout<<"ccf fuck "<<i<<endl;
		}
		memset(aisle_occ,0,sizeof(aisle_occ));
		for(int i=1;i<=n_people;i++)
		{
			if(p[i].y==1000) aisle_occ[int(p[i].x)]=1;//更新过道中人占的情况 
		}
		for(int i=1;i<=n_people;i++) cout<<i<<" "<<p[i].id<<"号乘客，坐标为"<<p[i].x<<" "<<p[i].y<<endl;
		cout<<"-----------------------------------------------------\n";
	}
	cout<<time_tot;
//	cout<<endl<<near(8,100);
}
