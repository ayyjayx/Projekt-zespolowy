import React from 'react';
import jwt_decode from 'jwt-decode';
import { setAuthToken } from './Login';
import Button from 'react-bootstrap/Button';
import board from "../assets/board.avif";

const token = localStorage.getItem("token");
if (token) {
    setAuthToken(token);
}

function LogOut() {
    localStorage.removeItem("token");
    setAuthToken(false);
    window.location.href = '/'
}

function LoggedHome() {
    let username = jwt_decode(token, { header: true })
    console.log(username);
    return (
        <>
            <header className='App-header'>szaszki.pl</header>
            <div className="center">
                <img src={board} width="700" height="500" alt=""></img>
                <h1>Jesteś zalogowany</h1>
                <Button onClick={LogOut}>Wyloguj</Button>
            </div>
        </>
    );
}

export default LoggedHome;