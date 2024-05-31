import React, { useState, useEffect, useCallback, useContext } from 'react';
import './pages/Home.css';
import SideBar from "./navComps";
import { Link, useParams, useNavigate } from 'react-router-dom';
import UserContext from './context';
import YoutubeEmbed from './Youtube';

export const Resource = ({content, title, desc, type, handleDelete, id}) => {

    if (type === 'YouTubeURL'){
        return(
            <YoutubeEmbed embedId={content.split('v=')[1] || content.split('=')[1]}/>
        )

    }

    return(
        <div className="resource-preview">
            <h3 className="resource-title"><a target='_blank' href={content}>{title}</a></h3>
            <div className="resource-info">
                <p className="rack-desc"><a target='_blank' href={content}>{desc}</a></p>
                <span className="extra-desc">
                    <p className="resource-type">type: {type}</p>
                    <button className="delete-button" onClick={() => handleDelete(id)}>Delete<ion-icon name="trash-outline"></ion-icon></button>
                </span>
            </div>
        </div>
    )
}


// Rack preview component containing
export const RackPrev = (props) => {

    const navigate = useNavigate();
    return (
        <div className="rack-preview" onClick={(event)=>{if (!event.target.closest('#rack-delete')) navigate(`/my_racks/${props.rack_id}`)}}>
            <h3 className="rack-title"><Link id="view-button" to={`/my_racks/${props.rack_id}`}>{props.title}</Link></h3>
            <div className="rack-info">
                <p className="rack-desc">{props.desc}</p>
                <span className="extra-desc">
                    <p>Items: {props.items}</p>
                    <Link id="view-button" to={`/my_racks/${props.rack_id}`}>Open Rack</Link>
                    <button id='rack-delete' onClick={() => props.handleDelete(props.rack_id)}>delete</button>
                </span>
            </div>
        </div>
    );
}

// Individual rack page component
export const Rack = ({rackName}) => {
    const [resources, setResources] = useState([]);
    const {rackId} = useParams();
    const {racks} = useContext(UserContext);
    const name = racks.filter((rack) => rack.id == rackId)[0].name || rackName;

    useEffect(() =>{
        const fetchResources = async () =>{
            const response = await fetch(`http://0.0.0.0:5000/api/v1/racks/${rackId}/resources`)
            const data = await response.json()
            setTimeout(() => setResources(data), 2000);
        }
        fetchResources();
    }, [rackId])
      
    const handleDelete = (id) => {
        const newResources = resources.filter(resource => resource.id !== id);
        const response = fetch('http://0.0.0.0:5000/api/v1/resources/' + id, {
            method: 'DELETE'
        })
        if (response.ok){
            console.log("delete successful")
        }else{
            console.log('delete failed');
        }
        setResources(newResources);
    }

    return(
        <>
        <SideBar />
        <div className='rack-content'>
            <h1>{name}</h1>
            <div className="resource-container">
                <h4>Texts and Web Urls</h4>
                {resources.map((resource) => (resources.type !== 'YouTubeURL' && <Resource
                    title={resource.title}
                    desc={resource.description}
                    type={resource.type}
                    content={resource.content}
                    handleDelete={handleDelete}
                    id={resource.id}
                    key={resource.id}
                    />))}
            </div>
            <h4>Youtube Vids</h4>
            <div>
                {resources.map((resource) => {resource.type === 'YouTubeURL' && <Resource />})}
            </div>
        </div>
        </>
    )
}

export default Rack;
