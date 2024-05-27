import React, { useEffect, useState, useContext } from 'react';
import SideBar from '../navComps';
import './create.css';
import UserContext from '../context';

function CreatePage (){

    const [content, setContent] = useState("Rack");
    const {user, racks, setValue} = useContext(UserContext);
    const [isChecked, setIsChecked] = useState(false);
    const [inputs, setInputs] = useState({library_id: user.library_id, public: isChecked});
    const [message, setMessage] = useState(null);


    useEffect(()=>{}, [inputs])

    const handleInputChange = (event) => {
        const name = event.target.name;
        const value = event.target.value;
        if (name === "public"){
            setIsChecked(!isChecked);
            setInputs({...inputs, public: isChecked});
        }else{
        setInputs(values => ({...values, [name]: value}));
        }
        console.log(inputs);
    }

    const handleSubmit = (event) =>{
        event.preventDefault();
        console.log(inputs);
        // Make Api request

        if (content === 'Rack'){
            fetch(`http://0.0.0.0:5000/api/v1/users/${user.id}/library/racks`, {
                method: 'POST',
                headers: {'Content-type': 'application/json'},
                body: JSON.stringify(inputs)
            }).then(response => response.json())
                .then(data => {
                    setMessage(`Create ${inputs.name} successfully`);
                    setValue({racks: data});
                }
            ).catch(err => {setMessage(err.message); console.error(err)});
        } else {
            fetch(`http://0.0.0.0:5000/api/v1/resources`, {
                method: 'POST',
                headers: {'Content-type': 'application/json'},
                body: JSON.stringify(inputs)
            }).then(response => response.json())
                .then(data => { 
                    setMessage(`Create ${inputs.title} successfully`);
            }).catch(err => {setMessage(err.message); console.error(err)});
        }
        console.log(inputs);
        // notify user on create status
    }
    const handleCreateSwitch = (name) => {
        setContent(name);
        setInputs({});
    }
    return(
        <>
        <SideBar />
        <div className='Create'>
        <h1>Create a new content</h1>
        <p>click to choose</p>
        <div className="create-buttons">
            <button
                className={content === "Rack" ? "focus" : ""}
                onClick={() => handleCreateSwitch('Rack')}>Rack</button>
            <button className={content !== "Rack" ? "focus" : ""}
                onClick={() => handleCreateSwitch('Resource')}>Resource</button>
        </div>
        <h4>New {content}</h4>
        <form onSubmit={handleSubmit} className='create-form'>
            {message && <i>{message}</i>}
            <label htmlFor='name'>{content + ' title'}
                <input
                    type="text"
                    id={ content === 'Rack' ? 'name' : "title"}
                    name={ content === 'Rack' ? 'name' : "title"}
                    value={inputs.name || inputs.title  || ""}
                    onChange={handleInputChange}
                    required
                />
            </label>
            <label htmlFor={'description'}>{content + ' description'}
                <input
                    id="description"
                    type='text'
                    name="description"
                    value={inputs.description || ""}
                    onChange={handleInputChange}
                />
            </label>
            {
                content !== "Rack" &&
                <>
                <select name="rack_id" onChange={handleInputChange}>
                    <option disabled>Choose destination rack</option>
                    {racks.map(
                        (rack) => (<option
                                    key={rack.id}
                                    value={rack.id} 
                                    name="rack_id">{rack.name}
                                    </option>))}
                </select>
                <select name="type" onChange={handleInputChange}>
                    <option selected>Choose resource type</option>
                    <option value="URL">Website or resource link</option>
                    <option value="YouTubeURL">YouTube Video Link</option>
                    <option value="Text">Text</option>
                </select>
                <textarea 
                name = "content"
                onChange={handleInputChange}
                placeholder='write your content here'
                value={ inputs.content || "" } ></textarea>
                </>
            }
            <label className="public" htmlFor='public'>
                <input
                className="public"
                id='public'
                type='checkbox'
                name='public'
                onChange={handleInputChange}
                checked={isChecked}
                />Make Public</label>
            <input type="submit" value="Create" />
        </form>
        </div>
        </>
    )
}

export default CreatePage;
