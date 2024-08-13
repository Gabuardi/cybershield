import {useState} from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import {Button, CardActions, Grid, Stack, TextField, Typography} from "@mui/material";

function App() {

    return (
        <Card sx={{minWidth: 275}}>
            <CardContent>
                <Typography variant="h4" gutterBottom>
                    SIGN IN
                </Typography>
                <Stack spacing={2}>
                    <div>
                        <TextField id="outlined-basic" label="Email" variant="outlined"/>
                    </div>
                    <div>
                        <TextField id="outlined-basic" label="Password" variant="outlined"/>
                    </div>
                </Stack>
            </CardContent>
            <CardActions className="action_items">
                <Button variant="contained">LOG IN</Button>
            </CardActions>
        </Card>
    )
}

export default App
