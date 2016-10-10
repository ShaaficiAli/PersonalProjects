/*
 * By:Shaafici Ali
 * Knights tour board
 * 6/18/2016
 * A Board which is an object used for my main program
 */
//Import statements for all functions used insied the prgram
import java.awt.*;
import javax.swing.*;

public class Board extends Object
{
    boolean board[][]=new boolean[8][8];    //A boolean variable that keeps track of if you have been on the spot or not
    
    
    public void draw(Graphics g)
    {
        
        for(int i=0;i<8;i++)
        {
            for(int j=0;j<8;j++)
            {
                if((i+j)%2==0)                      //if the piece is even set it to black
                { 
                    g.setColor(Color.black);            
                }
                else                                //if its odd set it to white
                {
                    g.setColor(Color.white);
                }
                if(board[i][j]==true)               //if you have been on set the colour blue
                {
                    g.setColor(Color.blue);
                }
                g.fillRect(i*100,j*100,100,100);    //draw each rectangle and fill it with its respective color
            }
        }
    }
    public void beenonspot(int x,int y)     //sets the piece that youve been on to true
    {
        board[x][y]=true;
    }
    public boolean checkspot(int x,int y)   //checks if youve been on the spot using
    {
        return board[x][y];
    }
    public void Reset()                     //Resets the board all to not been on
    {
        for(int i=0;i<8;i++)
        {
            for(int j=0;j<8;j++)
            {
                board[i][j]=false;
            }
        }
    }
    Board()                                 //sets the board list to false 
    {
        for(int i=0;i<8;i++)
        {
            for(int j=0;j<8;j++)
            {
                board[i][j]=false;
            }
        }
    }
    
    
        
}
