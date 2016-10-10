/*
 * Shaafici Ali
 * Knights Tour
 * 6/18/2016
 * A program that solves the knights tour puzzle and replays it in slow motion to the user
 */
//All of the import statements
import java.awt.*;
import javax.swing.*;

public class Knightstour extends JFrame implements Runnable
{
    Board board=new Board();                //Creates a new board
    Knight knight=new Knight(0,0);          //Creates a new Knight and starts its position in the top left corner
    
    Thread myThread=new Thread(this);       //Creates a new Threa
    Knightstour()                           //Constructor
    {
        super("knights tour");              //makes the name of the program knights tour and shows it when you open the window
        //sets up the Layout
        Container pane= getContentPane();
        pane.setLayout(new FlowLayout());
        
        board.beenonspot(0,0);              //it makes the point that you start at equal to true
        setSize (800,800);                 //sets size of the window to 800*800
        setVisible(true);                   //sets the Visibility to true
        myThread.start();                   //Starts the thread
    }
    public void run()
    {
        Thread thisThread=Thread.currentThread();               
        while(thisThread==myThread)         //while our thread that we started is the current thread
        {
            try
            {
                if(knight.getwonflag()==true)           //if you have won then start off with a 2.5 second pause
                {
                    Thread.sleep(2500);
                }
                knight.move(board);                                     //Move the knight
                board.beenonspot(knight.getrow(),knight.getcol());      //tell the board that the knight is on a spot
                repaint();                                              //update the screen    
               
            }
            catch (InterruptedException ie)
            
            {
            
                System.out.println(ie.getMessage()); // print error message if necessary
            }
        } 
    }

    public void paint(Graphics g)
    {
        super.paint(g); 
        board.draw(g);                  //paint the board
        knight.draw(this,g);            //paint the knight
    }
    public static void main( String args[])                         //setup the application
    {
        Knightstour game = new Knightstour();                       //contruct the application
        game.setDefaultCloseOperation( JFrame.EXIT_ON_CLOSE);       //Use X to close the program
    }
}
