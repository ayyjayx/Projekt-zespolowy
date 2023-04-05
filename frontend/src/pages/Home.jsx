import React from 'react';
import Button from 'react-bootstrap/Button';
import { Link } from "react-router-dom";
import { hasJWT } from '../utils/hasJWT.jsx';



function Home() {
    let isLoggedIn = "Jesteś nie zalogowany";
    hasJWT() ? isLoggedIn = window.location.href = '/loggedhome' : "";

    return (
        <>
        <div className="center">
            <h1>tu kiedyś będą szaszki</h1>
            <h2>{isLoggedIn}</h2>
            <Link to='/login'>
                <Button variant="Primary">Logowanie</Button>
            </Link>
            <Link to='/registration'>
                <Button variant="Primary">Rejestracja</Button>
            </Link>
        </div>
        </>
    );
}

export default Home;