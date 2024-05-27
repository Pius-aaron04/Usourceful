import React, { useContext, useEffect, useState } from 'react';
import { RackPrev } from '../racksComp'
import SideBar from '../navComps';
import './Home.css';
import UserContext from '../context';
import { Link, useNavigate } from 'react-router-dom';

function Home() {
    const {user, racks, isLoggedIn, setValue} = useContext(UserContext);
    const navigate = useNavigate();
    const [message, setMessage] = useState(null);

    useEffect(
        () => {
            // redirects user to home page if not logged in
            if (!isLoggedIn) return(navigate("/login"));
            
            fetch('http://0.0.0.0:5000/api/v1/users/'+user.id+'/library/racks')
                .then(response => response.json()).then(data => {setMessage("Welcome");setValue({racks: data})})
                .catch(err => setMessage(err.message))
    }, [isLoggedIn])//, [racks, navigate, user.id, isLoggedIn, setValue])
 
    return(
        <>
        <SideBar />
        <div className='home-content'>
            <h1>My Racks</h1>
            <div className="racks-container">
                {racks.length >= 1 ? racks.map((rack) => (<RackPrev key={rack.id}
                    title={rack.name}
                    desc={rack.description}
                    items={rack.items}
                    rack_id={rack.id}
                    />)) : <h2>You have not created any rack yet. <Link to="/create">Create</Link></h2>
                }
            </div>
        </div>
        </>
    );
}

export default Home;