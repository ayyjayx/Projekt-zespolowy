import React, { useState } from 'react';
import 'chessboard-element';
import './style.css';
// import { isLoggedIn } from '../utils/isLoggedIn';
// import { onlyAllowLegalMoves } from '../gameUtils/onlyAllowLegalMoves';
// import { hasJWT } from '../utils/hasJWT';
import axios from 'axios';


function Home() {
    // hasJWT() ? window.location.href = '/loggedhome' : '';

    const [loading, setLoading] = useState(false);
    const handleClick = () => {
        setLoading(true);
        axios.get('http://localhost:5000/creategame')
        .then(response => {
            const gameId = response.data.id;
            window.location.href = `/game/${gameId}`;
        })
        .finally(() => {
            setLoading(false);
        });

    }

    return (
        <div className='center'>
            <h2>Jesteś nie zalogowany</h2>

            <button disabled={loading} onClick={handleClick}> Zagraj tu! </button>
        </div>
    );
}

export default Home;