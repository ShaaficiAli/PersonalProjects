#include <iostream>
#include "Rectangle.h"
using std::cout;
using std::endl;
Rectangle::Rectangle(int x_start,int y_start,int width,int height)
{
	d_x_start=x_start;
	d_y_start=y_start;
	d_x_end=d_x_start+width;
	d_y_end=d_y_start+height;
}

void Rectangle::print()
{
	cout<<"Rectangle: ("<<d_x_start<<","<<d_y_start<<") to ("<<d_x_end<<","<<d_y_end<<")"<<endl;
}

bool Rectangle::intersect(Rectangle SecondRectangle)
{
	bool flag=false;
	if(d_x_start>=SecondRectangle.d_x_start&&d_x_start<=SecondRectangle.d_x_end || SecondRectangle.d_x_start>=d_x_start && SecondRectangle.d_x_start<=d_x_end)
	{
		if(d_y_start>=SecondRectangle.d_y_start&&d_y_start<=SecondRectangle.d_y_end || SecondRectangle.d_y_start>=d_y_start && SecondRectangle.d_y_start<=d_y_end)
		{
			flag=true;
		}
	}
	return flag;
}

Rectangle Rectangle::intersection(Rectangle SecondRectangle)
{
	int newWidth;
	int newHeight;
	int start_x;
	int start_y;
	int end_x;
	int end_y;
	Rectangle ReturnRectangle;
	if(intersect(SecondRectangle))
	{
		start_x= (d_x_start>=SecondRectangle.d_x_start) ? d_x_start:SecondRectangle.d_x_start;
		start_y= (d_y_start>=SecondRectangle.d_y_start) ? d_y_start:SecondRectangle.d_y_start;
		end_x= (d_x_end<=SecondRectangle.d_x_end) ? d_x_end:SecondRectangle.d_x_end;
		end_y= (d_y_end<=SecondRectangle.d_y_end) ? d_y_end:SecondRectangle.d_y_end;
		newWidth=end_x-start_x;
		newHeight=end_y-start_y;
		ReturnRectangle = Rectangle(start_x,start_y,newWidth,newHeight);
		
	}
	
	return ReturnRectangle;
	
	
}

std::array<Rectangle,4> Rectangle::split()
{
	int width1= ((d_x_end-d_x_start)%2==0) ? (d_x_end-d_x_start)/2:((d_x_end-d_x_start)/2)+1;
	int width2= (d_x_end-d_x_start)/2;
	int height1=((d_y_end-d_y_start)%2==0) ? (d_y_end-d_y_start)/2:((d_y_end-d_y_start)/2)+1;
	int height2=(d_y_end-d_y_start)/2;
	std::array<Rectangle,4> RectangleArray;
	RectangleArray[0]=Rectangle(d_x_start,d_y_start,width1,height1);
	RectangleArray[1]=Rectangle(d_x_start+width1,d_y_start,width2,height1);
	RectangleArray[2]=Rectangle(d_x_start,d_y_start+height1,width1,height2);
	RectangleArray[3]=Rectangle(d_x_start+width1,d_y_start+height1,width1,height2);
	return RectangleArray;	
}

	
