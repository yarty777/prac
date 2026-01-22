import { Route,Routes,BrowserRouter, Link } from 'react-router-dom';
import './App.css';
import Dashboard from './base/Dashboard'
import Login from './base/Login'
import Register from './base/Register'
import Quiz from './base/Quiz'
import Results from './base/Results'

function App() {
  return (
    <>
      <BrowserRouter>
      <nav style={{
        display:'flex',
        gap:'20px',
        margin:'20px',
        textDecoration:'none'
      }}>
      <Link to='/' style={{ textDecoration: 'none', color: '#333' }}>Хоме</Link>
      <Link to='/login' style={{ textDecoration: 'none', color: '#333' }}>Логінення хз</Link>
      <Link to='/register' style={{ textDecoration: 'none', color: '#333' }}>Регістрація</Link>
      <Link to='/quiz' style={{ textDecoration: 'none', color: '#333' }}>Квізи</Link>
      <Link to='/results' style={{ textDecoration: 'none', color: '#333' }}>Результат</Link>
      </nav>
      <Routes>
        <Route path='/' element={<Dashboard/>}></Route>
        <Route path='/login' element={<Login/>}></Route>
        <Route path='/register' element={<Register/>}></Route>
        <Route path='/quiz' element={<Quiz/>}></Route>
        <Route path='/results' element={<Results/>}></Route>
      </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
