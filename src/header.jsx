import { Link } from 'react-router-dom';

const Header = ({signin}) => {
  
  return ( 
    <header className="App-header">
    <span>
      <h1><Link to="/home">UsourceFul</Link></h1>
    </span>
      <nav className='nav-bar'>
        <span className='nav-icon'>
          <Link to="/about">About</Link>
          <Link to="/home">Home</Link>
          {/* <a href="./pages/community">Community</a> */}
          <Link to="/blog">Blog</Link>
        </span>
      </nav>
    </header>
    );
}
 
export default Header;