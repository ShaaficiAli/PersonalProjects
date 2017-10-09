import java.lang.System;
class Design3and5test{
public static void main(String[] args)
 {
 	PointCPDesign5 point1=new PointCPDesign3(1,1);
 	PointCPDesign3 point2=new PointCPDesign3(1,1);
 	double x;
 	double y;
 	long starttime=System.nanoTime();
 	for(int i=0;i<100000;i++)
 	{
 		point1=new PointCPDesign3(1,1);
 	}
 	long endtime=System.nanoTime();
 	System.out.print("Design5 constructor time:"+(endtime-starttime)+"\n");
 	
 	starttime=System.nanoTime();
 	for(int i=0;i<100000;i++)
 	{
 		point2=new PointCPDesign3(1,1);
 	}
 	endtime=System.nanoTime();
 	System.out.print("Design3 constructor time:"+(endtime-starttime)+"\n");
 	
 	starttime=System.nanoTime();
 	for(int i=0;i<100000;i++)
 	{
 		x=point1.getX();
 	}
 	endtime=System.nanoTime();
 	System.out.print("Design5 getX time:"+(endtime-starttime)+"\n");
 	
 	starttime=System.nanoTime();
 	for(int i=0;i<100000;i++)
 	{
 		x=point2.getX();
 	}
 	endtime=System.nanoTime();
 	System.out.print("Design3 getX time:"+(endtime-starttime)+"\n");	
 	
 	starttime=System.nanoTime();
 	for(int i=0;i<100000;i++)
 	{
 		y=point1.getY();
 	}
 	endtime=System.nanoTime();
 	System.out.print("Design5 getY time:"+(endtime-starttime)+"\n");

 	starttime=System.nanoTime();
 	for(int i=0;i<100000;i++)
 	{
 		y=point2.getY();
 	}
 	endtime=System.nanoTime();
 	System.out.print("Design3 getY time:"+(endtime-starttime)+"\n");

 	starttime=System.nanoTime();
 	for(int i=0;i<100000;i++)
 	{
 		y=point1.getRho();
 	}
 	endtime=System.nanoTime();
 	System.out.print("Design5 getRho time:"+(endtime-starttime)+"\n");

 	 starttime=System.nanoTime();
 	for(int i=0;i<100000;i++)
 	{
 		y=point2.getRho();
 	}
 	endtime=System.nanoTime();
 	System.out.print("Design3 getRho time:"+(endtime-starttime)+"\n");

 	starttime=System.nanoTime();
 	for(int i=0;i<100000;i++)
 	{
 		y=point1.getTheta();
 	}
 	endtime=System.nanoTime();
 	System.out.print("Design5 getTheta time:"+(endtime-starttime)+"\n");

 	starttime=System.nanoTime();
 	for(int i=0;i<100000;i++)
 	{
 		y=point2.getTheta();
 	}
 	endtime=System.nanoTime();
 	System.out.print("Design3 getTheta time:"+(endtime-starttime)+"\n");

 }
}