import React, { useEffect, useState, useContext } from 'react';
import SideBar from '../navComps';
import './create.css';
import UserContext from '../context';
import { useNavigate } from 'react-router-dom';


function CreatePage (){

    const [content, setContent] = useState("Rack");
    const {user, racks, setValue} = useContext(UserContext);
    const [inputs, setInputs] = useState({library_id: user.library_id, public: false});
    const [message, setMessage] = useState(null);


    useEffect(()=>{}, [inputs])

    const handleInputChange = (event) => {
        const name = event.target.name;
        const value = event.target.value;
        if (name === "public"){
            setInputs({...inputs, public: !inputs.public});
        }else{
        setInputs(values => ({...values, [name]: value}));
        }
    }

    const handleSubmit = (event) =>{
        event.preventDefault();
        // Make Api request

        if (content === 'Rack'){
            try {
                const fetchRack = async () => {
                    const response = await fetch(`http://localhost:5000/api/v1/users/${user.id}/library/racks`, {
                    method: 'POST',
                    headers: {'Content-type': 'application/json'},
                    body: JSON.stringify(inputs)}).catch(err => {setMessage(err.message); console.error(err)});

                    const data = await response.json();

                    if (!response.ok){
                        throw Error("Failed")
                    }
                    setMessage(`${inputs.name || inputs.title} created successfully`)
                    setTimeout(() => { setValue({racks: [...racks, data]}); console.log(racks)}, 2000)
                }
                fetchRack();
            } catch(error){
                setMessage(error.message)
            }
        } else {
            fetch(`http://localhost:5000/api/v1/resources`, {
                method: 'POST',
                headers: {'Content-type': 'application/json'},
                body: JSON.stringify(inputs)
            }).then(response => response.json())
            .catch(err => {setMessage(err.message); console.error(err)});
            setMessage(`${inputs.title} created succesfully`)
        }
        // notify user on create status
    }
    const handleCreateSwitch = (name) => {
        setContent(name);
        setInputs({library_id: user.library_id, public: false});
        setMessage(null);
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
                <label htmlFor='destination-choice'>Choose rack destination
                <select required id="destination-choice" name="rack_id" onChange={handleInputChange}>
                    <option >Choose destination rack</option>
                    {racks.map(
                        (rack) => (<option
                                    key={rack.id}
                                    value={rack.id} 
                                    name="rack_id">{rack.name}
                                    </option>))}
                </select>
                </label>
                <label htmlFor='resource-type'>
                <select required id="resource-type" name="type" onChange={handleInputChange}>
                    <option >Choose resource type</option>
                    <option name="type" value="URL">Website or resource link</option>
                    <option name="type" value="YouTubeURL">YouTube Video Link</option>
                    <option value="Text" name="type">Text</option>
                </select>
                </label>
                <label htmlFor="resource-content"> Resource content
                <textarea 
                id="resource-content"
                name = "content"
                onChange={handleInputChange}
                placeholder='write your content here'
                value={ inputs.content || "" } ></textarea>
                </label>
                </>
            }
            <label className="public" htmlFor='public'>
                <input
                className="public"
                id='public'
                type='checkbox'
                name='public'
                onChange={handleInputChange}
                checked={inputs.public}
                />Make Public</label>
            <input type="submit" value="Create" />
        </form>
        </div>
        </>
    )
}


// Short cut button at for creating resources or racks

export function CreateRack (){
    const [isOpen, setIsOpen] = useState(false);
    const {user, racks, setValue} = useContext(UserContext);
    const [inputs, setInputs] = useState({library_id: user.library_id, public: false});
    const [message, setMessage] = useState(null);
    const navigate = useNavigate();

    const toggleCreateForm = () => {
        setIsOpen(!isOpen);
    }

    const handleInputChange = (event) => {
        const name = event.target.name;
        const value = event.target.value;
        if (name === "public"){
            setInputs({...inputs, public: !inputs.public});
        }else{
        setInputs(values => ({...values, [name]: value}));
        }
    }

    useEffect(() => {
        const handleClickOutside = (event) => {
          if (isOpen && !event.target.closest('.open') && !event.target.closest('#pop-up')) {
            setIsOpen(false); // Close sidebar if clicked outside
          }
        };
    
        // Add event listener on mount, remove on unmount
        document.addEventListener('click', handleClickOutside);
        return () => document.removeEventListener('click', handleClickOutside);
    }, [isOpen, racks]);

    const handleSubmit = (event) =>{
    event.preventDefault();
    console.log(inputs);
    // Make Api request

        try {
            const fetchRack = async () => {
                const response = await fetch(`https://localhost:5000/api/v1/users/${user.id}/library/racks`, {
                method: 'POST',
                headers: {'Content-type': 'application/json'},
                body: JSON.stringify(inputs)}).catch(err => {setMessage(err.message); console.error(err)});

                const data = await response.json();
                if (response.ok){
                    setMessage(`Create ${inputs.name} successfully`);
                    navigate("/home");
                    setValue({racks: [...racks, ...data]});
                } else {
                    throw Error("create failed")
                }
           }
           fetchRack()
        } catch (error){
            console.error(error.message)
        }
    }

    return(
        <>
        <div className={isOpen ? 'open' : 'close'}>
            <h3>Create new Rack</h3>
            <form onSubmit={handleSubmit} className='create-form'>
                {message && <i>{message}</i>}
                <label htmlFor='name'>Rack name
                    <input
                        type="text"
                        id='name'
                        name='name'
                        value={inputs.name || ""}
                        onChange={handleInputChange}
                        required
                    />
                    </label>
                    <label htmlFor={'description'}>Rack description
                    <input
                        id="description"
                        type='text'
                        name="description"
                        value={inputs.description || ""}
                        onChange={handleInputChange}
                    />
                    </label>
                    <label className="public" htmlFor='public'>
                        <input
                        className="public"
                        id='public'
                        type='checkbox'
                        name='public'
                        onChange={handleInputChange}
                        checked={inputs.public}
                        />Make Public</label>
                    <input type="submit" value="Add"/>
            </form>
        </div>
        <button onClick={toggleCreateForm} id='pop-up'>
            {isOpen ? <ion-icon name="close-outline"></ion-icon> : <ion-icon name="add-outline"></ion-icon>}
        </button>
        </>
    );
}


export default CreatePage;
