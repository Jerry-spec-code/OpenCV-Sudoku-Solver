import React from 'react';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { CircularProgress } from '@mui/material';

type Props = {
    clicked : boolean;
    setClicked : (args : boolean) => void
    text : string;
}

const Btn = ({clicked, setClicked, text} : Props) => {
  const widthPercentage = text == 'Solve Grid!' ? "40%" : "10%";
  const marginLeftPx = text == 'Solve Grid!' ? "2px" : "10px";
  return (
    <div>   
      <Button disabled={clicked} variant="contained" color="primary" sx={{textTransform: "None", width: widthPercentage}} onClick={() => setClicked(true)}>
        <Typography sx={{ fontSize: "large"}}>
            {text}
        </Typography>
        {clicked && <CircularProgress sx={{ ml : marginLeftPx}} color="primary" />}
      </Button>
    </div>
  )
}

export default Btn;