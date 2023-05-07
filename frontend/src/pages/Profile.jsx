import React, { useEffect, useState } from "react";
import Button from 'react-bootstrap/Button'
import axios from 'axios';
// import jwt_decode from "jwt-decode";
import { hasJWT } from '../utils/hasJWT.jsx';
// import Cookies from 'universal-cookie';


function Profile() {
    hasJWT();
    // const cookies = new Cookies();
    // const token = cookies.get("access_token");
    const [account, setAccount] = useState('');
    // const decoded = jwt_decode(token);
    // const account_id = decoded.id

    useEffect(() => {
        axios.get("http://localhost:5000/profile", {
            withCredentials: true
        },
            {
                headers: {
                    "Content-Type": "application/json",
                },
            })
            .then(response => {
                console.log(response.data);
                setAccount(response.data);
            })
            .catch(err => {
                console.log(err);
            });
    },
        []);

    const handleEdit = () => {
        window.location.href = '/profile/update'
    };

    const handleDelete = () => {
        window.location.href = '/profile/delete'
    };

    return (
        <div className="center">
            <h1>Twoje konto</h1>
            <p>Nazwa użytkownika: {account.username}</p>
            <p>Email: {account.email}</p>
            <p>Data utworzenia konta: {account.created_on}</p>
            <Button onClick={handleEdit}>Edytuj</Button>
            <Button variant="danger" onClick={handleDelete}>Usuń konto</Button>
        </div>
    );
}

export default Profile;
