import React, { useState } from 'react';
import axios from 'axios';
import { Link } from "react-router-dom";
import Button from 'react-bootstrap/Button'
import './style.css'


function ResetEmail() {

    const [email, setEmail] = useState('');
    const [resetStatus, setResetStatus] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        const registerPayload = {
            email: email
        }

        axios.post("http://uwmchess.herokuapp.com/api/reset_send_email", registerPayload, {
            headers: {
                "Content-Type": "application/json"
            },
        })
            .then(response => {
                setResetStatus(response.data.email);
                console.log(response.data.exception)
                setEmail('');
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
                <form onSubmit={handleSubmit}>
                    <div className="form-body">
                        <div className="reset password">
                            <label className="form_label" htmlFor="firstName">Rejestracja </label>
                        </div>
                        <div className="email">
                            <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" id="email" className="form_input" placeholder="Email" />
                        </div>
                    </div>
                    <div className="footer">
                        <Button variant="Primary" type="submit" className="btn float-right">Zresetuj hasło</Button>
                        <Link to='/login'>
                            <Button variant="Primary" className="btn">Powrót do logowania</Button>
                        </Link>
                    </div>
                    <p>{resetStatus}</p>
                </form>
            </div></>
    );
}

export default ResetEmail;