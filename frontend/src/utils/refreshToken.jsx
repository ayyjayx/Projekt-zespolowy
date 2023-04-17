import Cookies from 'universal-cookie';
import axios from 'axios';
import setAuthToken from '../pages/Login';


export function refreshToken() {

    const cookies = new Cookies();
    const token = cookies.get("access_token");
    const refresh_token = cookies.get("refresh_token");
    console.log("refresh_token", refresh_token);
    const tokenPayload = {
        refresh_token: refresh_token
    };

    axios.post("http://localhost:5000/refresh", {
        headers: {
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + token
        },
        tokenPayload
    })
        .then(response => {
            const token = response.data.token;
            cookies.set("access_token", token);
            setAuthToken(token);
            // const new_token = response.data.token;
            // cookies.set("jwt_auth", new_token);
        })
        .catch(err => { console.log(err) })
}