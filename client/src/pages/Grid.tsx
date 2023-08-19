import React, { useEffect, useState } from "react";
import SudokuGrid from "../components/SudokuGrid/SudokuGrid";
import { Outlet, Link } from "react-router-dom";
import Btn from "../components/Button/Button";
import ROUTES from "../config/api";

const initialGrid = Array.from({ length: 9 }, () => Array.from({ length: 9 }, () => 0));

const Grid = () => {

    const [solve, setSolve] = useState(false);
    const [data, setData] = useState({});
    const [grid, setGrid] = useState(initialGrid);

    useEffect(() => {
        if (solve) {
            const requestOptions = {
                method: "POST",
                headers: { "Content-Type": "application/json"},
                body: JSON.stringify({ grid : grid})
            }
            const fetchData = async () => {
                await fetch(ROUTES.gridSolver, requestOptions)
                    .then((res) => res.json())
                    .then((data) => {
                        console.log(data);
                        if (data.status === "success") {
                            setData(data);
                            setGrid(data.result[1]);
                        }
                        else {
                            setData({});
                        }
                        setSolve(false);
                    })
            }
            fetchData();
        }
    }, [solve])

    return <div>
        <Link to="/">Upload an image instead</Link>
        <br />
        <p>Enter the known numbers and click the Solve button</p>
        <br />
        <SudokuGrid grid={grid} setGrid={setGrid}/>
        <br />
        <Btn clicked={solve} setClicked={setSolve} text={"Solve!"}/>
    </div>
};
  
export default Grid;