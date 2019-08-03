class AbandonedBook : Book
{
	int daysSinceLastRead;
	AbandonedBook(int daysSince): daysSinceLastRead(daysSince){}
	AbandonedBook(const Book &AbandonedBook, int daysSince):Book::Book(AbandonedBook)
	{
		AbandonedBook()
	}
}
