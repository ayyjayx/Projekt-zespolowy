import React from 'react';
// import { isLoggedIn } from '../utils/isLoggedIn';
import { hasJWT } from '../utils/hasJWT.jsx';
import axios from 'axios';
import Button from 'react-bootstrap/Button';
import './style.css';


function LoggedHome() {
    hasJWT();

    const handleClick = () => {
        axios.get('http://localhost:5000/creategameauth')
        .then(response => {
            const gameId = response.data.id;
            window.location.href = `/authgame/${gameId}`;
        });

    }

    return (
        <div className='center'>
            <h2>Jesteś zalogowany</h2>
            <Button onClick={handleClick}> Zagraj tu! </Button>
        </div>
    );
}

export default LoggedHome;