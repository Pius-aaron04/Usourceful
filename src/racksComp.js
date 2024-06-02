import React, { useState, useEffect, useCallback, useContext } from 'react';
import './pages/Home.css';
import SideBar from "./navComps";
import { Link, useParams, useNavigate } from 'react-router-dom';
import UserContext from './context';
import YoutubeEmbed from './Youtube';

export const Resource = ({content, title, desc, type, handleDelete, id}) => {

    // if (type === 'YouTubeURL'){
    //     return(
    //         <YoutubeEmbed embedId={content.split('v=')[1] || content.split('=')[1]}/>
    //     )

    // }

    return(
        <div className="resource-preview">
            <h3 className="resource-title"><a target='_blank' href={content}>{title}</a></h3>
            <div className="resource-info">
                <p className="rack-desc"><a target='_blank' href={content}>{desc}</a></p>
                <span className="extra-desc">
                    <p className="resource-type">type: {type}</p>
                    <Link to={`/resources/${id}`}>Open resource</Link>
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
            <h3 className="rack-title">{props.title}</h3>
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
export const Rack = () => {
    const [resources, setResources] = useState([]);
    const {rackId} = useParams();
    const {racks, isLoggedIn} = useContext(UserContext);
    const name = racks.filter((rack) => rack.id === rackId)[0].name || null;
    const navigate = useNavigate();

    if (!name || !isLoggedIn) navigate("/login")

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
            <h4>Texts and Web Urls</h4>
            <div className="resource-container">
                {resources.map((resource) => (<Resource
                    title={resource.title}
                    desc={resource.description}
                    type={resource.type}
                    content={resource.content}
                    handleDelete={handleDelete}
                    id={resource.id}
                    key={resource.id}
                    />))}
            </div>
            {/* <h4>Youtube Vids</h4>
            <div className='Yt-vids'>
                {resources.map((resource) => {resource.type === 'YouTubeURL' && <Resource />})}
            </div> */}
        </div>
        </>
    )
}

export const ResourceView = () => {
    const { resourceId } = useParams();
    const [resource, setResource] = useState({});
    const {user} = useContext(UserContext);
    const [inputs, setInputs] = useState({public: resource.public});
    const [update, setUpdate] = useState(false)

    const UpdateResource = () => {
        setUpdate(!update);
    }

    const handleInputChange = (event) => {
        const name = event.target.name;
        const value = event.target.value;
        if (name === "public"){
            setInputs({...inputs, public: !inputs.public});
        }else{
        setInputs(values => ({...values, [name]: value}));
        }
        console.log(inputs)
    }

    useEffect( () => {
            const fetchResource = async () => {
            const response = await fetch(`http://0.0.0.0:5000/api/v1/resources/${resourceId}`)
            if (response.ok){
                const data = await response.json();
                setTimeout(()=> setResource(data), 2000)
            }
        }

            fetchResource()
    }, [resourceId])

    return (
        <div className="resource-page" style={{
            marginTop: "70px"
        }}>
            <h1 style={{
                textJustify: "left"
            }}>{resource.title} </h1>
            {!update ?
                <>
                <h3>Resource description</h3>
                <p>{resource.description}</p>
                <h3>Resource content</h3>
                { resource.type === "YouTubeURL" ? <YoutubeEmbed embedId={ resource.content.split('v=')[1] || resource.content.split('=')[1] }/> : 
                    <p>{resource.type === 'URL' ? <a href={resource.content}>{resource.content}</a> : resource.content }</p> }
                </>
                :
                 
                <form>
                    <label htmlFor='resource-description'>Resource description
                        <input
                        type="text"
                        name="description"
                        onChange={handleInputChange}
                        value = { inputs.description || resource.description} />
                    </label>
                     <label htmlFor="resource-content"> Resource content
                        <textarea 
                            id="resource-content"
                            name = "content"
                            onChange={handleInputChange}
                            placeholder='write your content here'
                            value={ inputs.content || resource.content } ></textarea>
                    </label>
                    <label className="public" htmlFor='public'>
                        <input
                            className="public"
                            id='public'
                            type='checkbox'
                            name='public'
                            onChange={handleInputChange}
                            checked={inputs.public}
                        />Make Public
                    </label>
                    <div className='confirm-option'>
                        <button onClick={UpdateResource} >cancel</button>
                        <input type='submit' value="Update" />
                    </div>
                </form>
            }
            {
                (resource.userId === user.id || !update) &&
                <button onClick={UpdateResource}><ion-icon name="create-outline"></ion-icon></button>
            }
        </div>
    )
}

export default Rack;
