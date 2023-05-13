import React from 'react';
import 'chessboard-element';
import './style.css';
// import { isLoggedIn } from '../utils/isLoggedIn';
// import { onlyAllowLegalMoves } from '../gameUtils/onlyAllowLegalMoves';
import { hasJWT } from '../utils/hasJWT';
import axios from 'axios';
import Button from 'react-bootstrap/Button';


function Home() {
    hasJWT() ? window.location.href = '/loggedhome' : '';

    const handleClick = () => {
        axios.get('http://localhost:5000/creategame')
        .then(response => {
            const gameId = response.data.id;
            window.location.href = `/game/${gameId}`;
        });
    }

    return (
        <div className='center'>
            <h2>Jesteś nie zalogowany</h2>
            <Button onClick={handleClick}> Zagraj tu! </Button>
        </div>
    );
}

export default Home;