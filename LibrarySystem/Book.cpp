#include <string>
class Book
{
	std::string name;
	std::string date;
	Author author;
	double price;
	const double isbn;
	
	
	Book(std::string n, std::string d, Author a, double p, int pin): name(n), date(d), author(a), price(p),isbn(pin)
	{
		
	}
	Book(const Book&)= default{}
	}
	ostream &operator<<(ostream &os, const Book &item)
	{
		os<<"name:"<<item.name<<" date:"<<item.date<<" price:"<<item.price<<" Author"<<Author<<;
	}
	
	bool operator==(const Book book1,const Book book2)
	{
		return book1.name == book2.name && book1.author == book2.author && book1.price ==
	}
	
	template<typename T> void setPrice(T a)
	{
		this.price = a;
	}
	
	void setAuthor(Author a)
	{
		this.author = a;
	}
	
	
	
}
