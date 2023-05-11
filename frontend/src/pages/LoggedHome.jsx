import React, { useState } from 'react';
// import { isLoggedIn } from '../utils/isLoggedIn';
// import { hasJWT } from '../utils/hasJWT.jsx';
import axios from 'axios';


function LoggedHome() {
    // hasJWT() ? window.location.href = '/' : '';

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
            <h2>Jesteś zalogowany</h2>

            <button disabled={loading} onClick={handleClick}> Zagraj tu! </button>
        </div>
    );
}

export default LoggedHome;