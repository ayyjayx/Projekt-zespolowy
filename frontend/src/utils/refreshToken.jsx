import Cookies from 'universal-cookie';
import axios from 'axios';
import { setAuthToken } from '../pages/Login';


export function refreshToken() {

    const cookies = new Cookies();
    const refresh_token = cookies.get("refresh_token");
    setAuthToken(refresh_token);

    axios.post("http://localhost:5000/refresh",)
        .then(response => {
            const token = response.data.access_token;
            cookies.set("access_token", token);
            setAuthToken(token);
        })
        .catch(err => { console.log(err) })
}