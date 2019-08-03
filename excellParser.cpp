#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <Windows.h>
#include <vector>
#include <stdexcept>

#include <memory>
#include <array>

using namespace std;

std::string exec(const char* cmd)
{
	std::string files;
	array<char,128> buffer;
	auto pipe = popen(cmd,"r");
	if(!pipe) throw std::runtime_error("popen() failed!");
	
	while(!feof(pipe))
	{
		if(fgets(buffer.data(),128,pipe) !=nullptr)
		{
			files+= buffer.data();
		}
	}
	pclose(pipe);
	return files;
}

int main()
{
	std::string folder;
	vector<string> files;
	system("cd test");
	std::string s;
	s = exec("dir");
	std::cout<<s;
	
}
