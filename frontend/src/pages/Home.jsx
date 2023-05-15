import React from 'react';
import 'chessboard-element';
import './style.css';
import { hasJWT } from '../utils/hasJWT';
import Button from 'react-bootstrap/Button';


function Home() {
    hasJWT() ? window.location.href = '/loggedhome' : '';

    const handleClick = () => {
        window.location.href = 'game_noauth';
    }

    return (
        <div className='center'>
            <h2>Jesteś nie zalogowany</h2>
            <Button onClick={handleClick}> Zagraj tu! </Button>
        </div>
    );
}

export default Home;