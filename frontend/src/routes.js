import React from "react";
import { Redirect, Switch, Route, Router } from "react-router-dom";
import { history } from './helpers/history';
import Home from "./pages/Home";
import Login from "./pages/Login";
 
function Routes() {
   return (
       <Router history={history}>
           <Switch>
               <Route exact path="/" component={Home} />
               <Route path="/login" component={Login} />
               <Redirect to="/" />
           </Switch>
       </Router>
   );
}
 
export default Routes