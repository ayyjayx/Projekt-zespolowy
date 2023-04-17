import React, { useState } from 'react';
import { Link } from "react-router-dom";
import Button from 'react-bootstrap/Button'
import axios from 'axios';
import Cookies from 'universal-cookie';


export const setAuthToken = token => {
    if (token) {
        axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    }
    else
        delete axios.defaults.headers.common["Authorization"];
}

function Login() {
    const cookies = new Cookies();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loginStatus, setLoginStatus] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        const loginPayload = {
            username: username,
            password: password,
        }

        axios.post("http://localhost:5000/login", loginPayload)
            .then(response => {

                console.log(response.data)
                const access_token = response.data.access_token;
                const refresh_token = response.data.refresh_token;
                cookies.set("access_token", access_token);
                cookies.set("refresh_token", refresh_token)
                //set token to axios common header
                setAuthToken(access_token);

                console.log(response);
                response.status === 201 ?
                    setLoginStatus('Logowanie nie powiodło się. Spróbuj ponownie')
                    :
                    window.location.href = '/loggedhome'

            }).catch(err => console.log(err));
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
                    <p>{loginStatus}</p>
                </form>
            </div>
        </>
    );
}

export default Login;