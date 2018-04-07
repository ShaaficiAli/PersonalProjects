#include <array>
#ifndef Rectangle_
#define Rectangle_

class Rectangle{
	int d_x_start;
	int d_x_end;
	int d_y_start;
	int d_y_end;
public:
	Rectangle(int x_start=-1,int y_start=-1,int width=1,int height=1);
	void print();
	bool intersect(Rectangle SecondRectangle);
	Rectangle intersection(Rectangle SecondRectangle);
	std::array<Rectangle,4> split();
	};
	#endif
