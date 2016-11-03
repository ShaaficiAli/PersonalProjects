#include <iostream>
using namespace std; 
int binary_search(int list[],int size,int number)
{
	/*
	(list,int,int)-->int
	This program finds out if a number is inside a list
	Precondition: The list has to already be sorted
	
	O(log2(n))
	*/
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
	int sortedlist[]={1,2,3,4,5,6,7,14,16,18,21,24,36,37};
	int number_being_searchedfor;
	int size=sizeof(sortedlist)/4;
	cout<<"Which number are You looking for from our list:";
	cin>> number_being_searchedfor;
	int answer=binary_search(sortedlist,size,number_being_searchedfor);
	
	if(answer!=-1)
	{
		cout<<"The number in the "<<answer<<"th positition"<<endl;
	}
	else
	{
		cout<<"It is not in the list"<<endl;
	}
	
	
	
}

















