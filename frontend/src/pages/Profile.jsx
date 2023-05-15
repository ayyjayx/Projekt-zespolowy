import React, { useEffect, useState } from "react";
import Button from 'react-bootstrap/Button'
import axios from 'axios';
import { hasJWT } from '../utils/hasJWT.jsx';


function Profile() {
    hasJWT();
    const [account, setAccount] = useState('');

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

    const handleMyGames = () => {
        window.location.href = '/profile/games'
    }

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
            <Button onClick={handleMyGames}>Moje Gry</Button>
            <Button onClick={handleEdit}>Edytuj</Button>
            <Button variant="danger" onClick={handleDelete}>Usuń konto</Button>
        </div>
    );
}

export default Profile;
