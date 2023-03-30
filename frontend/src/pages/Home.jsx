import React from 'react';
import Button from 'react-bootstrap/Button'
import { Link } from "react-router-dom";

function Home() {
    return (
        <>
            <h1>tu kiedyś będą szaszki</h1>
            <Link to='/login'>
                <Button variant="Primary">Logowanie</Button>
            </Link>
            <Link to='/registration'>
                <Button variant="Primary">Rejestracja</Button>
            </Link>
        </>
    );
}

export default Home;