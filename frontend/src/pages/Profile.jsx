import React, { useState, useEffect } from "react";
import axios from 'axios';
import jwt_decode from "jwt-decode";

function Profile() {
    const [account, setAccount] = useState('');
    const token = localStorage.getItem('token');
    const decoded = jwt_decode(token);
    const account_id = decoded.id;

    useEffect(() => {
        axios.get("http://localhost:5000/account", {
            headers: {
                "Content-Type": "application/json",
                'Authorization': 'Bearer '+token,
            },
            data: {id: account_id}, })
        .then(response => {
            console.log(response.data);
            setAccount(response.data); })
        .catch(err => {
            console.log(err)}); },
    []);

    const handleEdit = () => {
        // przejscie na stronę do edycji
        window.location.href = '/account/update'
    };

    const handleDelete = () => {
        const deletePayload = {
            id: decoded.id,
        }

        axios.delete("http://localhost:5000/account/delete", deletePayload)
        .then(response => {
            console.log(response);
            // tu statusy
        })
        .catch(err => {
            console.log(err);
            // tu tesz
        });
    };

    return (
        <div>
        <h1>Profile</h1>
        <p>{decoded.id}</p>
        <p>Username: {account.username}</p>
        <p>Email: {account.email}</p>
        <p>Created on: {account.created_on}</p>
        <button onClick={handleEdit}>Edit</button>
        <button onClick={handleDelete}>Delete</button>
    </div>
    );
}

export default Profile;
