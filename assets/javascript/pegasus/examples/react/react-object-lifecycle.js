'use strict';
import React from "react";
import {createRoot} from "react-dom/client";
import EmployeeApplication from "./App";
import {getPegasusApiClient} from "../../pegasus";


const domContainer = document.querySelector('#object-lifecycle-home');
const root = createRoot(domContainer);
root.render(<EmployeeApplication client={getPegasusApiClient(SERVER_URL_BASE)} urlBase={urlBase}/>);
