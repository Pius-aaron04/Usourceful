import { Link, useNavigate } from 'react-router-dom';
import UserContext from './context';
import { useContext } from 'react';

const Header = () => {

  const {isLoggedIn} = useContext(UserContext);
  const navigate = useNavigate();
  
  return ( 
    <header className="App-header">
    <span>
      <h1><Link to="/home">UsourceFul</Link></h1>
    </span>
      { !isLoggedIn && 
      <nav className='nav-bar'>
          <span className='nav-icon'>
            <Link to="/about">About</Link>
            <Link to="/home">Home</Link>
            {/* <a href="./pages/community">Community</a> */}
            {/* <Link to="/blog">Blog</Link> */}
            <Link to="/xplore">Xplore</Link>
          </span>
          <button style={{
          margin: "10px", backgroundColor: "#64B5F6"
          }} 
          onClick={() => navigate("/login")}>Log in</button>
        </nav>
    }
    </header>
    );
}
 
export default Header;