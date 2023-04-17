import React, { useEffect, useState } from 'react';
import Button from 'react-bootstrap/Button'
import axios from 'axios';
import { hasJWT } from '../utils/hasJWT.jsx';
import jwt_decode from "jwt-decode";
import './style.css'
import Cookies from 'universal-cookie';
import { setAuthToken } from './Login.jsx';


function ProfileUpdate() {
    hasJWT() ? "" : window.location.href = '/login';
    const cookies = new Cookies();
    const token = cookies.get("access_token");
    const [account, setAccount] = useState('');
    const decoded = jwt_decode(token);
    const account_id = decoded.id;

    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [updateStatus, setUpdateStatus] = useState('');

    useEffect(() => {
        axios.get("http://localhost:5000/profile", {
            headers: {
                "Content-Type": "application/json",
                'Authorization': 'Bearer ' + token
            },
            data: { id: account_id },
        })
            .then(response => {
                setAccount(response.data);
                setAuthToken(response.data.token);
            })
            .catch(err => { console.log(err) });
    },
        []);

    const handleSubmit = (e) => {
        e.preventDefault();
        const updatePayload = {
            id: account.id,
            username: username,
            email: email,
            password: password
        }

        console.log("aaa", updatePayload);

        axios.post("http://localhost:5000/profile/update", {
            headers: {
                "Content-Type": "application/json",
                'Authorization': 'Bearer ' + token
            },
            updatePayload
        })
            .then(response => {
                console.log(response);
                setUpdateStatus(response.data);
                setPassword('');
            })
            .catch(err => {
                console.log(err)
            }
            );
    };

    return (
        <><header className="App-header">
            szaszki.pl
        </header>
            <div className="form">
                <h1>Twoje obecne dane</h1>
                <p>Nazwa użytkownika: {account.username}</p>
                <p>Email: {account.email}</p>
            </div>
            <div className="form">
                <form onSubmit={handleSubmit}>
                    <div className="form-body">
                        <div className="register">
                            <label className="form_label" htmlFor="firstName">Edycja danych</label>
                        </div>
                        <div className="username">
                            <input value={username} onChange={(e) => setUsername(e.target.value)} className="form_input" type="text" id="userName" placeholder="Nowa nazwa użytkownika" />
                        </div>
                        <div className="email">
                            <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" id="email" className="form_input" placeholder="Nowy email" />
                        </div>
                        <div className="password">
                            <input value={password} onChange={(e) => setPassword(e.target.value)} className="form_input" type="password" id="password" placeholder="Podaj aktualne hasło" />
                        </div>
                    </div>
                    <p>
                        Wypełnij tylko te pola z danymi, które chcesz zmienić
                    </p>
                    <div className="footer">
                        <Button variant="Primary" type="submit" className="btn">Zmień dane</Button>
                    </div>
                    <p>{updateStatus}</p>
                </form>
            </div></>
    );
}

export default ProfileUpdate;