import './App.css';
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SideBar from './navComps'; // Import SideBar
import Home from './pages/Home'; // Import your page components
import Xplore from './pages/Xplore';
import Favourites from './pages/Favourites';
import Community from './pages/Community';
import About from './pages/About';
import Blog from './pages/Blog';
import CreatePage from './pages/CreatePage';
import Header from './header';
import SignIn from './forms';
import { SignUp } from './forms';
import UserContext from './context';
import Landing from './pages/landingPage'
import { Rack, ResourceView } from './racksComp';
import { XploreRacks } from './pages/Xplore';


function App() {

  const [state, setState] = useState({
    user: {email:'', name:''},
    isLoggedIn: false,
    racks: []
  })

  const updateState = (newState) => setState({...state, ...newState});

  return (
    <Router>
      <div className="App">
        <Header />
        {/* <SideBar /> Include the SideBar here */}
        <UserContext.Provider value={{...state, setValue: updateState}}>
          {/* <CreateRack /> */}
          <Routes>
            <Route path="/xplore" element={<Xplore />} />
            <Route path="/favourites" element={<Favourites />} />
            <Route path="/community" element={<Community />} />
            <Route path="/about" element={<About />} />
            <Route path="/blog" element={<Blog />} />
            <Route path="/home" element={<Home />} />
            <Route path="/create" element={<CreatePage />} />
            <Route path="/login" element={<SignIn />} />
            <Route path="/signup" element={<SignUp />} />
            <Route path="/" exact index element={<Landing />} />
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
