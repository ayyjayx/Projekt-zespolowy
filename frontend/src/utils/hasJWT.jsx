import { useEffect, useState } from "react";
import axios from 'axios';
import Cookies from 'universal-cookie';

axios.defaults.withCredentials = true;

export function hasJWT() {
    const cookies = new Cookies();
    const [hasAuth, setHasAuth] = useState();
    useEffect(() => {
        axios.get("http://uwmchess.herokuapp.com/api/check_auth",
            {
                withCredentials: true
            })
            .then(response => {
                if (response.data.auth === true) {
                    setHasAuth(true)
                }
            })
            .catch(err => {
                console.log(err);
                if (err.response.data.msg == "Token has expired") {
                    try {
                        axios.post("http://uwmchess.herokuapp.com/api/refresh",
                            {
                                withCredentials: true,
                            },
                            {
                                headers: {
                                    "X-CSRF-TOKEN": `${cookies.get("csrf_refresh_token")}`
                                }
                            }
                        )
                    }
                    catch {
                        console.error("error");
                    }
                }
            });
    },
        []);
    return hasAuth;
}