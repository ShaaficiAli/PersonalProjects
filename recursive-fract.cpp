#include <iostream>
using namespace std;
int fract(int n)
{
	if (n==1)
	{
		return 1;
	}
	
	return n*fract(n-1);
}
int main()
{
	cout<<fract(6);
}

