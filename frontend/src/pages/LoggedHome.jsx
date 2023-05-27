import React from 'react';
// import { setAuthToken } from './Login';
import board from "../assets/board.avif";
import { isLoggedIn } from '../utils/isLoggedIn';
// import { hasJWT } from '../utils/hasJWT.jsx';
// import Cookies from 'universal-cookie';

// const cookies = new Cookies();
// const token = cookies.get("access_token");
// if (token) {
//     setAuthToken(token);
// }

function LoggedHome() {
    isLoggedIn() ? '' : window.location.href = '/';
    // hasJWT() ? '' : window.location.href = '/';
    // console.log(hasJWT());
    return (
        <>
            <header className='App-header'>szaszki.pl</header>
            <div className="center">
                <img src={board} width="500" height="500" alt=""></img>
                <h1>¯\_(ツ)_/¯</h1>
            </div>
        </>
    );
}

export default LoggedHome;