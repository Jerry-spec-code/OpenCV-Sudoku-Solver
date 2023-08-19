import React from "react";
import { Outlet, Link } from "react-router-dom";

const Home = () => {
    return <div>
        <nav>
            <Link to="/gridSolver">Fill in the grid instead</Link>
            <Outlet />  
        </nav>
    </div>
};
  
export default Home;