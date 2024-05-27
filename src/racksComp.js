import React, { useState, useEffect } from 'react';
import './pages/Home.css';
import SideBar from "./navComps";
import { Link, useParams } from 'react-router-dom';

export const Resource = ({content, title, desc, type, handleDelete, id}) => {
    return(
        <div className="resource-preview">
            <h3 className="resource-title"><a href={content}>{title}</a></h3>
            <div className="resource-info">
                <p className="rack-desc"><a href={content}>{desc}</a></p>
                <span class="extra-desc">
                    <p class="resource-type">type: {type}</p>
                    <button className="delete-button" onClick={() => handleDelete(id)}>Delete<ion-icon name="trash-outline"></ion-icon></button>
                </span>
            </div>
        </div>
    )
}


// Rack preview component containing
export const RackPrev = (props) => {

    return (
        <div className="rack-preview">
            <h3 className="rack-title">{props.title}</h3>
            <div className="rack-info">
                <p className="rack-desc">{props.desc}</p>
                <span className="extra-desc">
                    <p>Items: {props.items}</p>
                    <p>Items: {props.rack_id}</p>
                    <Link id="view-button" to={`/my_racks/${props.rack_id}`}>Open Rack</Link>
                </span>
            </div>
        </div>
    );
}

// Individual rack page component
export const Rack = () => {
    const [resources, setResources] = useState([]);
    const {rackId} = useParams();

    useEffect(() =>{
        const fetchResources = async () =>{
            const response = await fetch(`http://0.0.0.0:5000/api/v1/racks/${rackId}/resources`)
            const data = await response.json()
            setResources(data);
        }
        fetchResources();
    }, [rackId])
      
    const handleDelete = (id) => {
        const newResources = resources.filter(resource => resource.id !== id);
        console.log(`deleted ${id}`)
        setResources(newResources);
    }

    return(
        <>
        <SideBar />
        <div className='rack-content'>
            <h1>Rack title</h1>
            <div className="resource-container">
                {resources.map((resource) => (<Resource
                    title={resource.title}
                    desc={resource.desc}
                    type={resource.type}
                    content={resource.content}
                    handleDelete={handleDelete}
                    id={resource.id}
                    />))}
            </div>
        </div>
        </>
    )
}

export default Rack;