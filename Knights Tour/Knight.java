/*
 * By:Shaafici Ali
 * KNIGHTSTOUR: Knight
 * 6/18/2016
 * A Knight which is an object that is used in my main program, its the piece that moves
 */
//All the import statements
import java.util.Random;
import java.awt.*;
import javax.swing.*;

public class Knight extends Object 
{
    ImageIcon pic=new ImageIcon("knightpiece.png");         //the imamge uysed for the night when it move
    boolean wonflag;                                        //a flag that keeps track if you have won or not
    private int startx;                                     //Your starting x-coordinate
    private int starty;                                     //Your starting y-coordinate
    boolean reset=false;                                    //a flag used to check if you need to reset
    int move[][]={{2,1},{2,-1},{-2,1},{-2,-1},{1,2},{-1,-2},{-1,2},{1,-2}};             //A list of moves for the knight that he can make
    int order[][]=new int[64][2];                                                       //a list that will keep track of where the knight has been
    int replay;                                                                         //a variable that keeps track of the amount of successive moves that he has made
    Random random=new Random();                                                         //Creates a new random number generator
    private int row;                                                                    //a variable that keeps track of which row the knights on
    private int col;                                                                    //a variable that keeps track of which column the knights on

    public int getrow()                                                                //a get method for the row the knights on
    {
        return row;
    }
    public int getcol()                                                                 //a get method for the column the knights on
    {
        return col;
    }
    public boolean getwonflag()                                                         //a get method for if the knight has won or not
    {
        return wonflag;
    }
    
    public boolean stuck(Board b)                                                       //A method that determines if you are stuck or not by return a boolean variable depending on if you are
    {
        boolean f=false;                                                                //A variable taht will be returned true or false depeing if you are stuck
 
        for(int i=0;i<8;i++)                                                            //A for loop that goes eight times throught the eight moves the knight has
        {
            int s=col+move[i][0];                                                       //a variable for where your row will be if you moved in that particular way        
            int t=row+move[i][1];                                                       //a variable for where your row will be if you moved in that particular way
            if(s<=7 && s>=0 && t>=0 && t<=7 && b.checkspot(t,s)==true)                  //If the moves is on the board but it the piece that the knight will land is taken then f is true
            {
                f=true;
            }
            else if(s<=7 && s>=0 && t>=0 && t<=7 &&  b.checkspot(t,s)==false)           //if you find a suitable move on the board and that piece is not taken then f is false and break and stop checking moves
            {
                f=false;
                break;
            }
        }
        //if f is true than your stuck
        //if f is false than your not stuck
        return f;                   //return the result
    }
    public boolean won(Board b)                                                         //a function to determine if you have solved knight tour or not
    {
           boolean flag=true;                                                   //a flag that will start of as true until you find a spot that you have gotten yet
           for(int i=0;i<8;i++)                                                 //A for loop inside a for loop that will go through each square
           {
               for(int j=0;j<8;j++)
               {
                   if(b.checkspot(j,i)==false)                                //If you find a square that you havent been on stop checing and flag is false
                   {
                       flag=false;
                       break;
                   }
               }
           }
           //if flag is true than you have won
           //if flag is false than you lost.
           return flag;                                                     //return the results of flag
    }

    public void move(Board b)                                               //The move function that moves the knight
    {
       int m=random.nextInt(8);                                             // a variable that picks a random number from 1-8 
       int c=col;                                                           //a variable to keep track of which column you are on
       int r=row;                                                           //a variable to keep track of which row you have been on
       c=c+move[m][0];                                                      //makes the move with a random move chosen by m to your column
       r=r+move[m][1];                                                      //makes the move with a random move chosen by m to your row
       
       if(wonflag==false)                                                   //If you havent solved the puzzle yet 
       {
           boolean stuck=stuck(b);                                          //a boolean to see if the knight are stuck
           boolean won=won(b);                                              //a boolean to see if knight has won
           if(stuck==true)                                                  //if you are stuck
           {
               if(won==false)                                               //if you havent won the reset and start back to where you originated
               {
                   b.Reset();                                               
                   row=startx;                                               
                   col=starty;
                   replay=1;                                            
               }
               else                                                         //if you have won 
               {    
                   wonflag=true;                                            //turn the flag for winning to true
                   order[0][0]=startx;                                      //the first row in the list that keeps track of where you have been is your starting row
                   order[0][1]=starty;                                      //the first column in the list that keeps track of where you have been is your starting column
                   row=startx;                                              //start at the starting row
                   col=starty;                                              //start at the starting column
                   
                   b.Reset();                                               //Reeset the board
    
                   replay=0;                                                //your replay counter starts at 0
    
               }
            }
           else if(0<=r && r<=7 && 0<=c && c<=7 && b.checkspot(r,c)==false)     //if you are not stuck and there is a possible move
           {
               row=r;                                                           //move your row
               col=c;                                                           //move your column
               order[replay][0]=row;                                            //keep track of where you just moved to
               order[replay][1]=col;                                            //keep track of where you just moved to
               

               replay++;                                                        //add to the replay counter
           }
           
        }
       else if(wonflag==true)                                                   //if you have solved the knights tour 
       {
            
            if(replay>63)                                                       //if you are at the end of your replay then reset and start at the beginning
            {
                b.Reset();
                wonflag=true;
                replay=0;

            }
            row=order[replay][0];                                               //move to the row that the replay is on
            col=order[replay][1];                                               //move to the column that the replay is on
           
            replay++;                                                           //add to replay so you can go to the next one 
       }
    }

    public void draw(Container c,Graphics g)
    {

        pic.paintIcon(c,g,row*100,col*100);                                     //paints the picture depending on the row and column                           
    }

    public Knight(int x, int y)                                         //Knight constructor that takes two coordinates and starts the knight their and fills in necessary information
    {
        wonflag=false;                                                          
        replay=0;
        row=x;
        col=y;
        startx=x;
        starty=y;
        order[0][0]=x;
        order[0][1]=y;
    }
}
