import java.util.Scanner;
import java.io.File;
import java.io.FileWriter;

public class Sudoku {

    public void sudokuSolver() throws Exception {
        int[][] values = getValues();
        Cell[][] board = new Cell[9][9];
        Solution result = new Solution();
        result.initialize(board);
        populate(board, values); //Sets everything in the cell except for its neighbours.
        result.neighbours(board); //Initializes the neighbours. 
        String status = result.solve(board);
        writeStatus(status);
        writeResult(board);        
	}

    //Writes the status of the solution (invalid, multiple, complete)
    public void writeStatus(String status) throws Exception {
        FileWriter myWriter = new FileWriter("status.txt");
        myWriter.write(status);
        myWriter.close();
    }

    //Writes the solution to answer.txt 
    public void writeResult(Cell[][] board) throws Exception { 
        FileWriter myWriter = new FileWriter("answer.txt");

        for(int i = 0; i < board.length; i++) {
            for(int j = 0; j < board[i].length; j++) {
                myWriter.write(Integer.toString(board[i][j].getValue()) + " ");
            }
            myWriter.write("\n");
        }

        myWriter.close();
    }

    //Reads the values from the board.txt file. 
    public int[][] getValues() throws Exception {

        File infile = new File("board.txt");
        Scanner input = new Scanner(infile);
        int[][] values = new int[9][9];

        for(int i = 0; i < 9; i++) {
            for(int j = 0; j < 9; j++) {
                values[i][j] = Integer.parseInt(input.next());
            }
        }

        input.close();
        return values;
    }

	public void populate(Cell[][] board, int[][] values) {
		for(int i = 0; i < board.length; i++)
			for(int j = 0; j < board[i].length; j++) {
				board[i][j].setValue(values[i][j]);
				board[i][j].setAddress(i, j);
				board[i][j].setPossible(values[i][j]);
			}
	}
}
