import { hasJWT } from "./hasJWT";

export function isLoggedIn() {
    let flag;
    hasJWT() ? flag = true : flag = false;

    return flag
}