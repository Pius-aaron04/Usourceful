import React, { useContext, useEffect, useState } from 'react';
import { RackPrev } from '../components/racksComp'
import './Home.css';
import UserContext from '../context';
import { Link, useNavigate } from 'react-router-dom';
import { CreateRack } from './CreatePage';

function Home() {
    const {user, racks, isLoggedIn, setValue} = useContext(UserContext);
    const navigate = useNavigate();
    const [message, setMessage] = useState(null);

    useEffect(
        () => {
            if (isLoggedIn && user){
            
                fetch('http://localhost:5000/api/v1/users/'+user.id+'/library/racks', {
                    headers: {'Authorization': `Bearer ${user.access_token}`} 
                })
                    .then(response => response.json()).then(data => {setMessage("Welcome");setValue({racks: data})})
                    .catch(err => setMessage(err.message))
            } else{
                navigate("/login");
            }
    }, [isLoggedIn])//, [racks, navigate, user.id, isLoggedIn, setValue])
 
    const handleDelete = (id) => {
        const updatedRacks = racks.filter(rack => rack.id !== id);
        const response = fetch('http://localhost:5000/api/v1/racks/' + id, {
            method: 'DELETE'
        }).catch((err) => console.log(err))
        if (response.ok){
            console.log("delete successful")
        }else{
            console.log('delete failed');
        }
        setValue({racks: updatedRacks});
    }

    return(
        <>
        <div className='home-content'>
            {message && <h1>{message} {user.username}!</h1>}
            {racks.length >= 1 && <h2>visit your racks below</h2>}
            <div className="racks-container">
                {racks.length >= 1 ? racks.map((rack) => (<RackPrev key={rack.id}
                    title={rack.name}
                    desc={rack.description}
                    items={rack.num_items}
                    rack_id={rack.id}
                    handleDelete={handleDelete}
                    />)) : <h2>You have not created any rack yet. <Link to="/create">Create</Link></h2>
                }
            </div>
            <CreateRack />
        </div>
        </>
    );
}

export default Home;