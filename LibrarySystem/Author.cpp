#include <string>
class Author
{
	std::string firstName;
	std::string lastName;
	std::string dateOfBirth
	public Author(std::string first, std::string last, std::string Birth): firstName(first),lastName(last),datOfBirth(Birth){}
	public ~Author(){
	}
	ostream &operator<<(ostream &os,Author author)
	{
		os<<"firstname:"<<author.firstName<<author.lastName<<
	}
	
	bool operator==(Author author1, Author author2)
	{
		return author1.firstName == author2.firstName && author1.lastName == author2.lastName;
	}
	
	
}
