import Cookies from 'universal-cookie';

export function hasJWT() {
    const cookies = new Cookies();
    let flag = false;

    //check user has access token
    cookies.get("access_token") ? flag = true : flag = false

    return flag
}