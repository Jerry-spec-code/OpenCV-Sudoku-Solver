const API_ROOT = process.env.NODE_ENV === 'development' ? 'http://localhost:5000/api' : '/api';

const ROUTES = {
    gridSolver : `${API_ROOT}/gridSolver`,
    imageSolver : `${API_ROOT}/imageSolver`,
};

export default ROUTES;