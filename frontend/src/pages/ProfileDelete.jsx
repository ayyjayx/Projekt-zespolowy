import React from 'react';
import Button from 'react-bootstrap/Button';
import { Link } from "react-router-dom";
import { hasJWT } from '../utils/hasJWT.jsx';
import { useState } from 'react';
import axios from 'axios';
import Cookies from 'universal-cookie';

axios.defaults.withCredentials = true;

function ProfileDelete() {
    const cookies = new Cookies();
    hasJWT();
    axios.defaults.withCredentials = true;
    const [confirm, setConfirm] = useState('');
    const [password, setPassword] = useState('');

    function isConfirmed() {
        setConfirm(true);
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        // const deletePayload = {
        //     password: password
        // }

        axios.delete("http://localhost:5000/profile/delete", {
            headers: {
                "X-CSRF-TOKEN": `${cookies.get("csrf_access_token")}`
            }
        }).then(response => {
            if (response.status === 200) {
                axios.post("http://localhost:5000/logout")
                    .then(response => {
                        console.log(response)
                    }).catch(err => console.log(err));
                window.location.href = '/';
            }
        })
            .catch(err => { console.log(err); }
            );
    };


    return (
        <div className="center">
            <h1>Czy na pewno chcesz usunąć konto?</h1>
            <Button variant="danger" onClick={isConfirmed}>Tak, jestem pewien</Button>
            <Link to='/profile'>
                <Button variant="Primary">Nie, wróć do profilu</Button>
            </Link>
            {confirm === true && (
                <>
                    <div className="form">
                        <form onSubmit={handleSubmit}>
                            <div className="password">
                                <input value={password} onChange={(e) => setPassword(e.target.value)} className="form_input" type="password" id="password" placeholder="Hasło" />
                            </div>
                            <div className="footer">
                                <Button variant="Primary" type="submit" className="btn">Potwierdź hasło</Button>
                            </div>
                        </form>
                    </div>
                </>
            )}
        </div>
    );
}

export default ProfileDelete;