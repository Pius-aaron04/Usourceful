import React, { useState, useEffect} from "react";
import { Resource } from "../components/racksComp";
import { Link, useNavigate, useParams } from "react-router-dom";

const Xplore = () => {

    const [publicRacks, setPublicRacks] = useState([]);
    const navigate = useNavigate();

 
    useEffect( () => {
            const fetchPublicRacks = async () => {
            const response = await fetch('http://localhost:5000/api/v1/racks');
            if (response.ok){
                const data = await response.json();
                setTimeout(() => {setPublicRacks(data)}, 2000);
            }
        };

        fetchPublicRacks();
}, []);
    return(
        <>
        <section style={{
            marginTop: "100px",
            padding: "10px"}} className="intro">
        <h1>Xplore</h1>
        <p>Checkout resources and collections provided by other users.</p>
        <h4>Racks</h4>
        </section>
        <section className="racks-section">
            { publicRacks.map((rack) => 
                <div className="rack-preview" onClick={()=>{navigate(`/xplore/racks/${rack.id}`)}}>
                <h3 className="rack-title">{rack.name}</h3>
                <div className="rack-info">
                    <p className="rack-desc">{rack.description}</p>
                    <span className="extra-desc">
                        <p>Items: {rack.num_items}</p>
                        <Link id="view-button" to={`/xplore/racks/${rack.id}`}>Open Rack</Link>
                    </span>
                </div>
            </div>
            )}
        </section>
        </>
    )
}



// Visible rack component on Xplore page
export const XploreRacks = () => {
   const [rack] = useState({});
   const {rackId} = useParams();
   const [resources, setResources] = useState([]);

   useEffect(() =>{
    const fetchResources = async () =>{
        const response = await fetch(`http://localhost:5000/api/v1/racks/${rackId}/resources?public=true`);
        const data = await response.json();
        setResources(data);
    }

    fetchResources();
   }, [rackId])

    return(
        <>
        <div className='rack-content'>
            <h1>{rack.name}</h1>
            <div className="resource-container">
                {resources.map((resource) => (<Resource
                    title={resource.title}
                    desc={resource.description}
                    type={resource.type}
                    content={resource.content}
                    id={resource.id}
                    key={resource.id}
                    userId={resource.userId}
                    />))}
            </div>
        </div>
        </>
    )
}

export default Xplore;