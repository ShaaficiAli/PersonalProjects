#include <iostream>
using namespace std; 
int binary_search(int list[],int size,int number)
{
	int b=0;
	int e=size-1;
	int mid;
	while (b<=e)
	{
		
		mid=(b+e)/2;
		if(list[mid]==number)
		{
			return mid+1;
		}
		else if(list[mid]<number)
		{
			b=mid+1;
		}
		else if(list[mid]>number)
		{
			e=mid-1;
		}
	}
	return -1;
}
int main()
{
	int sortedlist[15]={1,2,3,4,5,6,7,14,16,18,21,24,36,37};
	int answer=binary_search(sortedlist,14,21);
	if(answer!=-1){
		cout<<"The number in the "<<answer<<"th positition"<<endl;
	}
	else
	{
		cout<<"It is not in the list"<<endl;
	}
	
	
	
}

















