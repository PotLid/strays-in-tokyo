import React from 'react';
import ReactDOM from 'react-dom';

import {Provider} from "react-redux";
import store from './app/store';

import './normalize.css'
import './index.css';
import App from './App';

import {BrowserRouter as Router} from "react-router-dom";

ReactDOM.render(
    <React.StrictMode>
        <Provider store={store}>
            <Router>
                <App/>
            </Router>
        </Provider>
    </React.StrictMode>,
    document.getElementById('app-root')
);
