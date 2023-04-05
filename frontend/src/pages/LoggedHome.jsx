import React from 'react';
import jwt_decode from 'jwt-decode';
import { setAuthToken } from './Login';
import Button from 'react-bootstrap/Button';

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
            <h1>Jesteś zalogowany</h1>
            <Button onClick={LogOut}>Wyloguj</Button>
        </>
    );
}

export default LoggedHome;