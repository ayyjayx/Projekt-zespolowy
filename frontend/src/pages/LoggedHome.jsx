import React from 'react';
import { setAuthToken } from './Login';
import board from "../assets/board.avif";
import { hasJWT } from '../utils/hasJWT.jsx';
import Cookies from 'universal-cookie';

const cookies = new Cookies();
const token = cookies.get("access_token");
if (token) {
    setAuthToken(token);
}

function LoggedHome() {
    if (!hasJWT()) {
        window.location.href = "/"
    }
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