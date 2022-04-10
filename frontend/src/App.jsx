import {Routes, Route} from "react-router-dom";

import {URL_HOME, URL_LOGIN, URL_ABOUT} from './app/const';

import {Header, Footer, Background} from './app/ui';
import {Home, Login, About, NotFound} from './app/views';

import './_App.scss';

function App() {
    return (
        <>
            <Header/>
            <Background />
            <Routes>
                <Route path={URL_HOME} element={<Home/>}/>
                <Route path={URL_LOGIN} element={<Login/>}/>
                {/*<Route path='/register' element={<Temp/>}/>*/}
                <Route path={URL_ABOUT} element={<About/>}/>
                <Route path={'*'} element={<NotFound/>}/>
            </Routes>
            <Footer/>
        </>
    );
}

export default App;
