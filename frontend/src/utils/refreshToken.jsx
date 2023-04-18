import Cookies from 'universal-cookie';
import axios from 'axios';
import { setAuthToken } from '../pages/Login';


export function refreshToken() {

    const cookies = new Cookies();
    const refresh_token = cookies.get("refresh_token");
    console.log("refresh_tokenaaa: ", refresh_token);

    axios.post("http://localhost:5000/refresh", {
        headers: {
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + refresh_token
        }
    })
        .then(response => {
            console.log("access_token: ", response.data.access_token)
            const token = response.data.access_token;
            cookies.set("access_token", token);
            setAuthToken(token);
        })
        .catch(err => { console.log(err) })
}