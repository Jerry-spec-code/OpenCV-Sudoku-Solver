import java.util.LinkedList;
import java.util.List;

public class Solution {

	//Solves the Sudoku puzzle 
	public String solve(Cell[][] board) {	
		String solutionStatus = complete(board);	

		if(solutionStatus.equals("incomplete")) {	
			solutionStatus = LogicCycle1(board);

			if(solutionStatus.equals("incomplete")) {
				solutionStatus = LogicCycle2(board);

				if(solutionStatus.equals("incomplete"))
					solutionStatus = Guesser(board);
				
			}	
		}
		
		return solutionStatus;
	}
	
	// An empty cell is a value if it cannot be any other value 
	public String LogicCycle1(Cell[][] board) {
		// For each cell that is filled, remove the possibility for its neighbours to be that value. 
		for(int i = 0; i < board.length; i++)
			for(int j = 0; j < board[i].length; j++)
				if(board[i][j].getValue() != 0)
					remove(board[i][j]);
		
		return complete(board);
	}
	
	public void remove(Cell element) { //Removes the possibilites for element's neighbour to be the value of the element
		List<Integer> lstPossible = new LinkedList<Integer>();
		List<Cell> lstNeighbours = new LinkedList<Cell>();
		
		lstNeighbours = element.getNeighbour(); //Gets all the neighbours of element. 
		
		for(int k = 0; k < lstNeighbours.size(); k++) {
			Cell neighbour = lstNeighbours.get(k); //Gets a particular neighbour 
			neighbour.removePossible(element.getValue()); //Removes the value of the board from its neighbours.
			lstPossible = neighbour.getPossible(); //Gets the remaining possibilites after removal
			
			if(lstPossible.size() == 1) {//If the neighbour only has one possible value, set the neighbour to be that value. 
				neighbour.setValue(lstPossible.get(0));
				neighbour.emptyList();
				remove(neighbour);
			}
		}
	}
	
	// An empty cell is a value if that value cannot be anywhere else in the same row, column, or box 
	public String LogicCycle2(Cell[][] board) {
		List<Integer> possible = new LinkedList<Integer>();
		List<Cell> neighbours = new LinkedList<Cell>();
		
		for(int i = 0; i < board.length; i++)
			for(int j = 0; j < board[i].length; j++)
				if(board[i][j].getValue() == 0) {
					possible = board[i][j].getPossible(); //Gets all the possibilities of board[i][j]
					neighbours = board[i][j].getNeighbour(); //Gets all the neighbours of board[i][j]
					
					for(int a = 0; a < possible.size(); a++) { //Loops through each possibility in board[i][j]
						boolean unique = true;						
						//Initializes each neighbour to have neighbourType 1, 2, and/or 3
						//neighbourType = 1 ==> same row
						//neighbourType = 2 ==> same column
						//neighbourType = 3 ==> same box
						//Note: The initialization will be lists since each neighbour can be more than one type. 
						initialize(neighbours, i, j);
					
						for(int neighbourType = 1; neighbourType <= 3; neighbourType++) { //Loops through each neighbour type
							for(int k = 0; k < neighbours.size(); k++){//Loops through each neighbour in board[i][j]
								//If another cell within the same row, column, or box can also be the possible value
								//Then the possibility is not unique 
								if(neighbours.get(k).getNeighbourType().contains(neighbourType) 
										&& neighbours.get(k).getPossible().contains(possible.get(a))) {
									unique = false;
									break;
								}
							}
							// If no neighbouring cell within the same row, column, or box can be the possibility, 
							// Then it must be at the current cell 
							if(unique) {
								board[i][j].setValue(possible.get(a));
								board[i][j].emptyList();
								remove(board[i][j]); //Runs through logic 1.
								break;
							}
						}
							
					}		
				}
		
		return complete(board);
					
	}
	
	//Initializes each neighbour to have neighbourType 1, 2, and/or 3
	public void initialize(List<Cell> neighbours, int row, int column) {
		//Loops through each neighbour in neighbours 
		for(int i = 0; i < neighbours.size(); i++) { 
			Cell neighbourElement = neighbours.get(i);

			//Gets the rows and columns for the particular neighbour 
			int newRow = neighbourElement.getRow(); 
			int newColumn = neighbourElement.getColumn();
			
			if(newRow == row) //If the original cell and the neighbour are in the same row
				neighbourElement.setNeighbourType(1);
				
			if(newColumn == column) //If the original cell and the neighbour are in the same column
				neighbourElement.setNeighbourType(2);
			
			//If the original cell and the neighbour are in the same box 
			if(newRow - newRow % 3 == row - row % 3 && newColumn - newColumn % 3 == column - column % 3)
				neighbourElement.setNeighbourType(3);
		}
	}
	
	// Runs a backtracking algorithm using recursion 
	public String Guesser(Cell[][] board) {
		Cell[][] boardCopy = new Cell[9][9]; 
		initialize(boardCopy);
		neighbours(boardCopy);
		copy(boardCopy, board); //Copies contents of board into boardCopy.
		int[] index = new int[2];
		int target = 2;
		
		//Finds a cell with target number of possible values 
		// If none exist, increment target 
		while(exist(board, target, index) == -1) 
			target++;
		
		//Runs the guesser 
		while(board[index[0]][index[1]].getPossible().size() != 0) {
			//Sets the corresponding cell of boardCopy to be the first possibility of that cell on board
			boardCopy[index[0]][index[1]].setValue(board[index[0]][index[1]].getPossible().get(0));
			//Removes that first possibility from the original board
			board[index[0]][index[1]].removePossible(board[index[0]][index[1]].getPossible().get(0));
			boardCopy[index[0]][index[1]].emptyList();
			
			String temp = solve(boardCopy);
			
			//If there are multiple solutions 
			if(temp.equalsIgnoreCase("multiple")) {
				copy(board, boardCopy);
				return temp;
			}

			//If there is one solution 
			else if(temp.equalsIgnoreCase("complete")) {
				//Need to check for multiple solutions. 
				Cell[][] newBoard = new Cell[9][9];
				initialize(newBoard);
				neighbours(newBoard);
				copy(newBoard, board); //Copies contents of board into newBoard
				copy(board, boardCopy); //Copies contents of boardCopy into board 

				String newTemp = solve(newBoard);

				//If the solution is invalid, then there was only one valid guess, which we already found
				if(newTemp.equalsIgnoreCase("invalid")) {
					return "complete";
				}

				return "multiple";
			}
				
			//If the guess is invalid, copy the original board back into boardCopy
			else if(temp.equalsIgnoreCase("invalid"))
				copy(boardCopy, board);
				
		}
		
		return complete(board);
			
	}
	
	//Copies the original board into a new board
	public void copy(Cell[][] copy, Cell[][] original) {
		for(int i = 0; i < copy.length; i++)
			for(int j = 0; j < copy[i].length; j++) {
				copy[i][j].emptyList();
				copy[i][j].setValue(original[i][j].getValue());
				copy[i][j].setAddress(i, j);	
				//The new board must have the same possibilites as the original board 
				for(int k = 0; k < original[i][j].getPossible().size(); k++)
					copy[i][j].addPossible(original[i][j].getPossible().get(k));
	
			}
	}
	
	//Finds a cell with target number of possible values and sets the index to correspond to that cell 
	public int exist(Cell[][] board, int target, int[] index) {
		for(int i = 0; i < board.length; i++)
			for(int j = 0; j < board[i].length; j++)
				if(board[i][j].getPossible().size() == target) {
					index[0] = i;
					index[1] = j;
					return target;
				}

		return -1;
	}
	
	//Creates a new cell object for each cell in the board
	public void initialize(Cell[][] board) {
		for(int i = 0; i < board.length; i++)
			for(int j = 0; j < board[i].length; j++)
				board[i][j] = new Cell();
	}
	
	//Checks if the board is invalid, incomplete, or complete 
	public String complete(Cell[][] board) {
		List<Cell> neighbours = new LinkedList<Cell>();
		
		for(int i = 0; i < board.length; i++)
			for(int j = 0; j < board[i].length; j++) {
				neighbours = board[i][j].getNeighbour();
				for(int k = 0; k < neighbours.size(); k++)
					//The board is invalid if two non-empty neighbours hold the same value or 
					//If an empty cell has no more possibilities 
					if(board[i][j].getValue() != 0 && neighbours.get(k).getValue() == board[i][j].getValue() || board[i][j].getValue() == 0 && board[i][j].getPossible().size() == 0)
						return "invalid";
			}
		
		for(int i = 0; i < board.length; i++)
			for(int j = 0; j < board[i].length; j++)
				if(board[i][j].getValue() == 0)
					return "incomplete";
			
		return "complete";
	}
	
	//For every cell in the same row, column, or box, initialize them as neighbours  
	public void neighbours(Cell[][] board) {
		for(int i = 0; i < board.length; i++) //Loops through the row
			for(int j = 0; j < board[i].length; j++) //Loops through the column
				for(int a = 0; a < board.length; a++) //For each cell, loops through rows and column again
					for(int b = 0; b < board[i].length; b++) {
						if(a == i && b == j)
							continue;
						
						if(a == i || b == j || a - a % 3 == i - i % 3 && b - b % 3 == j - j % 3) //Same row, column, box.
							board[i][j].setNeighbour(board[a][b]);
					}
						
	}
	
	//Displays the board in the console given the board
	public void display(Cell[][] board)
	{
		System.out.println();
		
		for(int i = 0; i < board.length; i++)
		{
			for(int j = 0; j < board[i].length; j++)
			{
				System.out.print(board[i][j].getValue() + "    ");
				if(j % 3 == 2)
					System.out.print("|     ");
			}
				
			System.out.println();
			
			if(i % 3 == 2)
				System.out.println("----------------------------------------------------------");
		}	
	}

	//Displays the board in the console given the values of the board
	public void display(int[][] values)
	{
		System.out.println();
		
		for(int i = 0; i < values.length; i++)
		{
			for(int j = 0; j < values[i].length; j++)
			{
				System.out.print(values[i][j] + "    ");
				if(j % 3 == 2)
					System.out.print("|     ");
			}
				
			System.out.println();
			
			if(i % 3 == 2)
				System.out.println("----------------------------------------------------------");
		}	
	}
}