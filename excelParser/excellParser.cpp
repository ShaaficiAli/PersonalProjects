#include <string>
#include <Windows.h>
#include <vector>
#include <string>
#include <stdexcept>
#include <fstream>
#include <unistd.h>
#include <array>
#include <stdio.h>
#include <iostream>
#include <sstream>
#include <stdlib.h>
using namespace std;
/*
isFileinLine returns a boolean and checks if a file with a certain type passed to it is present in the line.
@param std::string line is the line to check
@param std::string filetype is the type of file to check for ie:.txt,.csv,.lxml
*/
bool isFileinLine(std::string line,std::string filetype)
{
	size_t pos  = line.find(filetype);
	return pos != std::string::npos;
	
}
/*
getFileinLine returns the name of the file that is present withing the line of a cmd dir command.
@param std:string line is the line that is being passed
@param std::string filetype is the type of file ie: .txt, .csv, .lxml
*/
std::string getFileFromLine(std::string line, std::string filetype)
{
	std::stringstream ss(line);
	std::string buffer;
	std::string results;
	while(getline(ss,buffer,' '))
	{
		if(buffer.find(filetype) != std::string::npos)
		{
			results=buffer;
			results.erase(results.find_last_not_of(' '));
		}
	}
	return results;
}
/*
getAllFiles returns a vector all the files with a certain file type that is present withing the same directory
as this program.
@param std::string filetype the type of file you want to retrieve.
*/
std::vector<std::string> getAllFiles(std::string filetype)
{
	auto pipe = popen("dir","r");
	std::array<char,256> buffer;
	int total = 0;
	std::vector<std::string> filenames;
	if(pipe)
	{
		while(fgets(buffer.data(),256,pipe) != NULL)
		{
			if(isFileinLine(buffer.data(),filetype))
			{
				std::string results = getFileFromLine(buffer.data(),filetype);
				filenames.push_back(results);
				
			}
		}
	}

	return filenames;

}
/*
transferContents appends the contents of one file to another and skips the first line.
@param const char* transfer is the name of the file to tranfer.
@param const char* transfee is the name of the file to receive the new content.
*/
void transferContents(const char* transfer,const char* transfee)
{
	ifstream in(transfer);
	ofstream out(transfee,ios::app);
	std::string currentline;
	if(getline(in,currentline))
	{
		while(getline(in,currentline))
		{
			out<<currentline<<std::endl;
		}
	}
	else{
		cerr<<"failed to open file"<<endl;
	}
	in.close();
	out.close();
}
/*
transferVectorFilesToOne transfers all the file names inside a vector into one file.
@param std::vector<std:string> files is a vector containing all the names of files to transfer
@param const char* transfee is the file that will receive the content.
*/
void transferVectorFilesToOne(std::vector<std::string> files,  const char* transfee)
{
	for(std::string fileName : files)
	{
		char file[fileName.size()+1];
		strcpy(file,fileName.c_str());
		if(strcmp(file,transfee)!=0)
		{
			cout<<"transfering contents from "<<file<<" to "<<transfee<<endl;
			transferContents(file,transfee);
		}
		
	}
}


int main(int arg,char **argv)
{
	

	char *filename = new char[25];

	char *filetype = new char[25];

	cout<<"Which file you like to transer files into?:";
	
	cin>>filename;
	cout<<endl<<"What type of files do you want transfered?:";
	cin>>filetype;
	cout<<endl;
	
	std::vector<std::string> filenames = getAllFiles(filetype);
	for(std::string a : filenames)
	{
		cout<<a<<endl;
	}
	transferVectorFilesToOne(filenames,filename);
	delete filename;
	delete filetype;
	
}
