import React from 'react';
import { hasJWT } from '../utils/hasJWT.jsx';



function Profile() {
    hasJWT() ? "" : window.location.href = '/login'

    return (
        <h1>asd</h1>
    );
}

export default Profile;