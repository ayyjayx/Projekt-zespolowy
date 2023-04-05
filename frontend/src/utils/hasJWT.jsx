export function hasJWT() {
    let flag = false;

    //check user has JWT token
    localStorage.getItem("token") ? flag = true : flag = false

    return flag
}