import './App.css';
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from '../pages/Home'; // Import your page components
import Xplore from '../pages/Xplore';
import Favourites from '../pages/Favourites';
import Community from '../pages/Community';
import About from '../pages/About';
import CreatePage from '../pages/CreatePage';
import Header from './header';
import SignIn, {SignUp} from '../components/forms';
import UserContext from '../context';
import { Rack, ResourceView } from './racksComp';
import { XploreRacks } from '../pages/Xplore';
import SideBar from './navComps';


function App() {

  const user_data = JSON.parse(localStorage.getItem('user')) || {};
  const [state, setState] = useState({
    user: user_data,
    isLoggedIn: user_data.id ? true : false,
    racks: []
  })

  const updateState = (newState) => setState({...state, ...newState});

  return (
    <Router>
      <div className="App">
        <UserContext.Provider value={{...state, setValue: updateState}}>
          <Header />
          <SideBar />
          <Routes>
            <Route path="/" exact index element={<Xplore />} />
            <Route path="/xplore" element={<Xplore />} />
            <Route path="/favourites" element={<Favourites />} />
            <Route path="/community" element={<Community />} />
            <Route path="/about" element={<About />} />
            <Route path="/home" element={<Home />} />
            <Route path="/create" element={<CreatePage />} />
            <Route path="/login" element={<SignIn />} />
            <Route path="/signup" element={<SignUp />} />
            <Route path="/my_racks/:rackId" element={<Rack />} />
            <Route path="/xplore/racks/:rackId" element={<XploreRacks />} />
            <Route path="/resources/:resourceId" element={<ResourceView />} />
          </Routes>
        </UserContext.Provider>
      </div>
    </Router>
  );
}
export default App;
