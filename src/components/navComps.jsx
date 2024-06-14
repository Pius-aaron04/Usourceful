import React, { useContext, useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import UserContext from '../context';

function SideBar() {
    const [isOpen, setIsOpen] = useState(false);
    const {isLoggedIn, setValue} = useContext(UserContext);
    const navigate = useNavigate();

    const toggleSidebar = () => {
        setIsOpen(!isOpen);
    }
  // Handle click outside the sidebar
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (isOpen && !event.target.closest('.side-bar')) {
        setIsOpen(false); // Close sidebar if clicked outside
      }
    };

    // Add event listener on mount, remove on unmount
    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  }, [isOpen]); 

  const handleLogout = () => {
    setValue({isLoggedIn: false, user: {}})
    localStorage.clear();
    navigate("/login");
    setIsOpen(!isOpen);
  }

    return (
        <nav className={`side-bar ${isOpen ? 'open' : 'closed'}`}>
            <button id="menu-button" onClick={toggleSidebar}>
                    {isOpen ? 
                    <ion-icon className="closed menu-icon" name="close-outline" size="large"></ion-icon> :
                    <ion-icon className="open menu-icon" name="menu-outline" size="large"></ion-icon>
                }
            </button>
            {isOpen &&
            <>
               <span className='top-section'>
            <ul>
              <li onClick={() => navigate('/home')}>
                <Link to="/home">Home <ion-icon name="home-outline"></ion-icon></Link>
              </li>
              <li onClick={() => navigate('/xplore')}>
                <Link to="/xplore">Xplore <ion-icon name="planet-outline"></ion-icon></Link>
              </li>
              <li onClick={() => {isLoggedIn ? navigate('/favourites') : navigate("/login")}}>
                <Link to="/favourites">Favourites <ion-icon name="star-half-outline"></ion-icon></Link>
              </li>

              {/* Nav icon opens new tab to the about section of the app's landing page*/}
              <li onClick={(e) => {
                e.preventDefault();
                window.open("https://Pius-aaron04.github.io/Usourceful/#about", "_blank");}}>
                <a href="https://Pius-aaron04.github.io/Usourceful/#about" target="_blank" >About <ion-icon name="map-outline"></ion-icon></a>
              </li>
              {/* Navigates to the create page*/}
              <li onClick={() => {isLoggedIn ? navigate('/create') : navigate("/login")}}>
                <Link to="/create">Create <ion-icon name="add-outline"></ion-icon></Link>
              </li>
            </ul>
          </span>
            {
              // Logical display of login and logout button
              isLoggedIn && <button className="log-in-out-btn out" onClick={handleLogout} ><ion-icon name="log-out-outline"></ion-icon> </button>
            }
            </>
            }
        </nav>
    )
}

export default SideBar;