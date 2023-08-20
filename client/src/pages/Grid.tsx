import React, { useEffect, useState } from "react";
import SudokuGrid from "../components/SudokuGrid/SudokuGrid";
import { Outlet, Link } from "react-router-dom";
import Btn from "../components/Button/Button";
import ROUTES from "../config/api";

const initialGrid = Array.from({ length: 9 }, () => Array.from({ length: 9 }, () => 0));

type Solution = {
    valid : boolean;
    solution : number[][];
    message : string;
};

const Grid = () => {

    const [solve, setSolve] = useState(false);
    const [data, setData] = useState<Solution | null>(null);
    const [grid, setGrid] = useState(initialGrid);
    const [message, setMessage] = useState('');

    useEffect(() => {
        if (solve) {
            const requestOptions = {
                method: "POST",
                headers: { "Content-Type": "application/json"},
                body: JSON.stringify({ grid : grid })
            }
            const fetchData = async () => {
                await fetch(ROUTES.gridSolver, requestOptions)
                    .then((res) => res.json())
                    .then((data) => {
                        console.log(data);
                        if (data.status === "success") {
                            setData(data);
                            if (data.valid) {
                                setGrid(data.solution);
                            }
                            setMessage(data.message);
                        }
                        else {
                            setData(null);
                        }
                        setSolve(false);
                    })
            }
            fetchData();
        }
    }, [solve]);

    return <div>
        <Link to="/">Upload an image instead</Link>
        <br />
        <p>Enter the known numbers and click the Solve button</p>
        <SudokuGrid grid={grid} setGrid={setGrid} message={message} setMessage={setMessage}/>
        <br />
        <Btn clicked={solve} setClicked={setSolve} text={"Solve!"}/>
    </div>
};
  
export default Grid;