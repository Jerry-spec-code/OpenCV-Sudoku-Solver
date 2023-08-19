import java.util.LinkedList;
import java.util.List;

public class Cell {
	
	private int value, row, column;
	private List<Cell> neighbours;
	private List<Integer> possible;
	private List<Integer> neighbourType; //Type 1 is same row, type 2 is same column, type 3 is same box. 
	
	public Cell() {
		this.value = 0;
		this.neighbours = new LinkedList<Cell>();
		this.possible = new LinkedList<Integer>();
		this.neighbourType = new LinkedList<Integer>();
		this.row = 0;
		this.column = 0;
	}
	
	public void setAddress(int row, int column) { //Sets the row, column of a cell 
		this.row = row;
		this.column = column;
	}
	
	public int getRow() {//Gets the row of a cell
		return this.row;
	}
	
	public int getColumn() { //Gets the column of a cell
		return this.column;
	}
	
	public void setValue(int value) { //Sets the value of a cell as value 
		this.value = value;
	}
	
	public int getValue() { //Returns the value of a cell
		return this.value;
	}
	
	public void setNeighbourType(int value) { //Adds value to the list of neighbour types 
		this.neighbourType.add(value);
	}
	
	public List<Integer> getNeighbourType() { //Gets the list of neighbour types 
		return this.neighbourType;
	}
	
	public void setPossible(int value) { //Initializes the possibilities to the numbers from one to nine			
		if(value == 0)
			for(int i = 1; i <= 9; i++)
				this.possible.add(i);
	}
	
	public List<Integer> getPossible() { //Gets the list of possible values for any given cell			
		return this.possible;
	}
	
	public void removePossible(int value) {	 //Removes value as a possibility
		for(int i = 0; i < this.possible.size(); i++)
			if(this.possible.get(i) == value) {
				this.possible.remove(i);
				return;
			}
				
	}
	
	public void addPossible(int value) { //Adds value as a possibility
		this.possible.add(value);
	}
	
	public void emptyList() { //Clears all the possibilities 
		this.possible.clear();
	}
	
	public void setNeighbour(Cell cell) { //Adds cell as a neighbour 
		this.neighbours.add(cell);
	}
	
	public List<Cell> getNeighbour() { //Gets the list of neighbours
		return this.neighbours;
	}

}