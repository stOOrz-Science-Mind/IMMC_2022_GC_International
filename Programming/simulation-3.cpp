#include<bits/stdc++.h>
#define nega1 999
#define nega2 998
using namespace std;
int total_seated,n_people;
double dis[100009];//i����i+1�ŵľ��� 
struct passenger
{
	double x,y;//��ǰ���� 
	double seatx,seaty;//��λ 
	int status;//0=�ƶ� 1=������ 2=���� 
	int seated;//�Ƿ���� 
	int id;
	double luggage_timeleft;//������ʣ��ʱ��
	double luggage; 
	int status2_to;//��¼�Ƿ����ڸ�����������������ֵΪ�������� 
	int status2_from;//��¼�Ƿ����˸��������� 
	double velocity; 
}p[100009];
struct cell
{
	double xcell,ycell;
	int status_cell;//0=��λ 1=���� 
	bool occupied;//�������λ�Ļ� �Ƿ��Ѿ������� 
}cells[3005][3005];
bool blocked[3005][3005];
bool aisle_occ[3005];//����ռ����� 
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
int d=4;//�ܼ��� 
bool near(double a,double b)
{
	return abs(a-b)<=0.1;
}
void move(int num)
{
//	cout<<"sbsbsbsb "<<num<<endl;
	int xx=int(p[num].x);
	if(!blocked[xx+1][1000])//ǰ��û�ж�ס
	{
		int tot_people_in_d=0;
//		int tot_people_in_i=0;
		int i;
		for(i=1;i<=d&&!blocked[xx+i];i++)
		{
			if(aisle_occ[xx+i]) tot_people_in_d++;
			//i����ǰ��d�����ڵ�һ���ڷ�������˾���num�ŵ�λ��  
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
		time_tot++;//ö����С��Ԫʱ�� 
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
					if(p[i].luggage_timeleft<=0) {p[i].status=2;p[i].x=p[i].seatx;p[i].y=p[i].seaty;cells[int(p[i].x)][(int(p[i].y)>0)?int(p[i].y):int(p[i].y)+1000].occupied=1;blocked[int(p[i].x)][0]=0;total_seated++;}//ע�����������1��λ��ʱ������������������״̬�������� 
					p[i].luggage_timeleft-=1;
				}
//				else if(p[i].status==2)
//				{
//					int to=p[i].status2_to;
//				}
				else if(p[i].status==0)
				{
					if(near(p[i].x,p[i].seatx))//�Ѿ��ִ���λ��׼������ 
					{
//						cout<<"{}";
						double time_wait=1;
						p[i].status=1;
						if(p[i].seaty>1000)
						{
							if(cells[int(p[i].seatx)][1002].occupied&&p[i].seaty==1003) time_wait=2;//���ڲ���λ���м���λ���� 
							else if(cells[int(p[i].seatx)][1001].occupied) time_wait=1;
						}
						else
						{
							if(cells[int(p[i].seatx)][998].occupied&&p[i].seaty==997) time_wait=2;//-2=nega2 -1=-1 
							else if(cells[int(p[i].seatx)][999].occupied) time_wait=1;
						}
						p[i].luggage_timeleft=p[i].luggage+time_wait;//�����������+�����Ⱦ���ǰ׼����ʱ��
						blocked[int(p[i].x)][0]=1;//׼���������ǰ�����޷�ͨ�� 
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
			if(p[i].y==1000) aisle_occ[int(p[i].x)]=1;//���¹�������ռ����� 
		}
		for(int i=1;i<=n_people;i++) cout<<i<<" "<<p[i].id<<"�ų˿ͣ�����Ϊ"<<p[i].x<<" "<<p[i].y<<endl;
		cout<<"-----------------------------------------------------\n";
	}
	cout<<time_tot;
//	cout<<endl<<near(8,100);
}
