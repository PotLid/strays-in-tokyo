import logo from './logo.svg';

import {Routes, Route, NavLink} from "react-router-dom";

import './App.css';

const Home = props => {

  return (
      <div>
        Home - init
      </div>
  )
}

const Temp = props => {

  return (
      <div>
        Temp - init
      </div>
  )
}

const NotFound = props => {

  return (
      <div style={{fontSize: '2rem', color: 'red'}}>
        NotFound
      </div>
  )
}

function App() {
  return (
    <div className="App">
      <nav>
        <NavLink to={'/'} >Home</NavLink>
        <NavLink to={'/temp'} >Temp</NavLink>
      </nav>
      <Routes>
        <Route path='/' element={<Home/>}/>
        <Route path='/temp' element={<Temp/>}/>
        <Route path={'*'} element={<NotFound/>} />
      </Routes>

    </div>
  );
}

export default App;
