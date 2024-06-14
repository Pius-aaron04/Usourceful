import React, { useState, useEffect, useContext } from 'react';
import '../pages/Home.css';
import { Link, useParams, useNavigate } from 'react-router-dom';
import UserContext from '../context';
import YoutubeEmbed from '../Youtube';


// Resource Component displaying resource Info


export const Resource = ({content, title, desc, type, handleDelete, id, userId}) => {
    const { user } = useContext(UserContext);

     /**
     * A function that handles the deletion of a rack after confirmation.
     *
     */
     const handleDeleteResource = () => {
        const confirmation = window.confirm(`Are sure you want to delete this \nresource: ${title}?`);
        if (confirmation) {
            handleDelete(id);
        }
    }

    return(
        <div className="resource-preview">
            <h3 className="resource-title"><a target='_blank' href={content}>{title}</a></h3>
            <div className="resource-info">
                <p className="rack-desc"><a target='_blank' href={content}>{desc}</a></p>
                <span className="extra-desc">
                    <p className="resource-type">type: {type}</p>
                    <Link to={`/resources/${id}`}>Open resource</Link>
                    { userId === user.id && 
                    <button className="delete-button" onClick={handleDeleteResource}>Delete<ion-icon name="trash-outline"></ion-icon></button>
                    }
                </span>
            </div>
        </div>
    )
}


// Rack preview component display rack info


export const RackPrev = (props) => {

    /**
     * A function that handles the deletion of a rack after confirmation.
     *
     */
    const handleDelete = () => {
        const confirmation = window.confirm(`Are sure you want to delete this \n rack:${props.title}?`);
        if (confirmation) {
            props.handleDelete(props.rack_id);
        }
    }

    const navigate = useNavigate();
    return (
        <div className="rack-preview" onClick={(event)=>{if (!event.target.closest('#rack-delete')) navigate(`/my_racks/${props.rack_id}`)}}>
            <h3 className="rack-title">{props.title}</h3>
            <div className="rack-info">
                <p className="rack-desc">{props.desc}</p>
                <span className="extra-desc">
                    <p>Items: {props.items}</p>
                    <Link id="view-button" to={`/my_racks/${props.rack_id}`}>Open Rack</Link>
                    <button id='rack-delete' onClick={() => handleDelete(props.rack_id)}>delete</button>
                </span>
            </div>
        </div>
    );
}

// Individual rack page component display resource components


export const Rack = () => {
    const [resources, setResources] = useState([]);
    const {rackId} = useParams();
    const {racks, isLoggedIn} = useContext(UserContext);
    const name = racks.filter((rack) => rack.id === rackId)[0].name || null;
    const navigate = useNavigate();

    if (!name || !isLoggedIn) navigate("/login")

     /**
     * Fetches resources from the server for a given rack ID.
     *
     * @return {Promise<void>} A promise that resolves when the resources have been fetched and the state has been updated.
     */
    useEffect(() =>{
        const fetchResources = async () =>{
            const response = await fetch(`http://localhost:5000/api/v1/racks/${rackId}/resources`)
            const data = await response.json()
            setTimeout(() => setResources(data), 2000);
        }
        fetchResources();
    }, [rackId])
      
   
    const handleDelete = (id) => {
        const newResources = resources.filter(resource => resource.id !== id);
        const response = fetch('http://localhost:5000/api/v1/resources/' + id, {
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
        <div className='rack-content'>
            <h1>{name}</h1>
            <div className="resource-container">
                {resources.length  >= 1 ? resources.map((resource) => (<Resource
                    title={resource.title}
                    desc={resource.description}
                    type={resource.type}
                    content={resource.content}
                    handleDelete={handleDelete}
                    id={resource.id}
                    key={resource.id}
                    userId={resource.userId}
                    />))  : <p>You have no resources in this racks <Link to="/create" >Create</Link></p>}
            </div>
        </div>
        </>
    )
}


// This Component desplays resource contents and features
export const ResourceView = () => {
    const { resourceId } = useParams();
    const [resource, setResource] = useState({});
    const {user} = useContext(UserContext);
    const [inputs, setInputs] = useState({public: resource.public});
    const [update, setUpdate] = useState(false);
    const [message, setMessage] = useState(null);

    const UpdateResource = () => {
        setUpdate(!update);
        setInputs({public: resource.public});
    }

    const handleSubmit = (event) => {
        event.preventDefault()

        const newData = {...resource, ...inputs};
        try{
            const updateData = async () => {
                const response = await fetch(`http://localhost:5000/api/v1/users/${user.id}/library/racks/${resource.rack_id}/resources/${resource.id}`, {
                    method: 'PUT',
                    headers: {'Content-type': 'application/json'},
                    body: JSON.stringify(newData)})


                if (response.ok){
                    console.log("Update successful")
                    setResource(newData);
                    return (true);
                } else {
                    console.error("Resource update failed");
                }
            }

            if (updateData()){ 
                setMessage("Updated");
                setUpdate(!update);
            } else {setMessage("Update failed");}
        } catch(error){
            console.error(error.message)
        }
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
            const response = await fetch(`http://localhost:5000/api/v1/resources/${resourceId}`)
            if (response.ok){
                const data = await response.json();
                setResource(data);
            }
        }

            fetchResource()
    }, [resourceId])

    return (
        <div className="resource-page" style={{
            marginTop: "70px", justifyContent: "left"
        }}>
            <h1 style={{
                weight: "500"
            }}>{resource.title} </h1>
            {!update ?
                <>
                <p
                 style={{
                    font: "italic",
                    color: "grey"
                 }}>{resource.description}</p>
                { resource.type === "YouTubeURL" ? <YoutubeEmbed embedId={ resource.content.split('v=')[1] || resource.content.split('=')[1] }/> : 
                    <p>{resource.type === 'URL' ? <a href={resource.content}>{resource.content}</a> : resource.content }</p> }
                </>
                :
                 
                <form onSubmit={handleSubmit}>

                    {message && <i>{message}</i>}
                    <label htmlFor='title'>Resource title<input
                        id="title"
                        name="title"
                        value={inputs.title || resource.title || ""}
                        onChange={handleInputChange}
                        type="text" /></label>
                    <label htmlFor='resource-description'>Resource description
                        <input
                        type="text"
                        name="description"
                        onChange={handleInputChange}
                        value = { inputs.description || resource.description || ""} />
                    </label>
                     <label htmlFor="resource-content"> Resource content
                        <textarea 
                            id="resource-content"
                            name = "content"
                            onChange={handleInputChange}
                            placeholder='write your content here'
                            value={ inputs.content || resource.content || "" } ></textarea>
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
                    <button onClick={UpdateResource} >Cancel</button>
                    <input type='submit' value="Update" />
                </form>
            }
            {
                (resource.userId === user.id && !update) &&
                <button style={{
                    width: "fit-content",
                    height: "fit-content",
                    color: 'green'
                }} 
                onClick={UpdateResource}>Edit<ion-icon style={{fontSize: "16px"}}
                name="create-outline"></ion-icon></button>
            }
        </div>
    )
}

export default Rack;
