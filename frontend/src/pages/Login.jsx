import React, { useState } from 'react';
import { Link } from "react-router-dom";
import Button from 'react-bootstrap/Button'
import axios from 'axios';

export const setAuthToken = token => {
    if (token) {
        axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    }
    else
        delete axios.defaults.headers.common["Authorization"];
}

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = () => {
        const loginPayload = {
            username: 'eve.holt@reqres.in',
            password: 'cityslicka',
        }

        axios.post("https://reqres.in/api/login", loginPayload)
            .then(response => {
                //get token from response
                const token = response.data.token;

                //set JWT token to local
                localStorage.setItem("token", token);

                //set token to axios common header
                setAuthToken(token);

                //redirect user to home page
                window.location.href = '/'
            })
            .catch(err => console.log(err));
    };
    return (
        <><header className="App-header">
            szaszki.pl
        </header>
            <div className="form">
                <form onSubmit={handleSubmit}>
                    <div className="form-body">
                        <div className="login">
                            <label className="form_label" htmlFor="firstName">Logowanie</label>
                        </div>
                        <div className="username">
                            <input value={username} onChange={(e) => setUsername(e.target.value)} className="form_input" type="text" id="userName" placeholder="Nazwa użytkownika" />
                        </div>
                        <div className="password">
                            <input value={password} onChange={(e) => setPassword(e.target.value)} className="form_input" type="password" id="password" placeholder="Hasło" />
                        </div>
                    </div>
                    <div className="footer">
                        <Link to='/registration'>
                            <Button variant="Primary" className="btn">Nie masz konta? Zarejestruj się!</Button>
                        </Link>
                        <Button variant="Primary" type="submit" className="btn">Zaloguj</Button>
                    </div>
                </form>
            </div>
        </>
    );
}

export default Login;