import React, { useState, useEffect } from "react";
import SideBar from "../navComps";
import { Resource } from "../racksComp";
import { Link, useNavigate, useParams } from "react-router-dom";

const Xplore = () => {

    const [publicRacks, setPublicRacks] = useState([]);
    const navigate = useNavigate()

    useEffect(
        () => {
            fetch('http://0.0.0.0:5000/api/v1/racks')
                .then(response => response.json()).then(data => {if (data.length > 1) setPublicRacks(data)})
    });

    return(
        <>
        <SideBar />
        <h1 style={
            {marginTop: "150px"}
        }>Xplore</h1>
        <p>Checkout resources and collections provided by other users.</p>
        <h4>Racks</h4>
        <section className="racks-section">
            {publicRacks.map((rack) => 
                <div className="rack-preview" onClick={()=>{navigate(`/xplore/racks/${rack.id}`)}}>
                <h3 className="rack-title"><Link id="view-button" to={`/xplore/racks/${rack.id}`}>{rack.name}</Link></h3>
                <div className="rack-info">
                    <p className="rack-desc">{rack.description}</p>
                    <span className="extra-desc">
                        <p>Items: {rack.items}</p>
                        <Link id="view-button" to={`/xplore/racks/${rack.id}`}>Open Rack</Link>
                    </span>
                </div>
            </div>
            )}
        </section>
        </>
    )
}


export const XploreRacks = () => {
   const [rack, setRack] = useState({});
   const {rackId} = useParams();
   const [resources, setResources] = useState([])

   useEffect(() =>{
        const fetchRack = async () =>{
            const response = await fetch(`http://0.0.0.0:5000/api/v1/racks/${rackId}`)
            const data = await response.json()
            setTimeout(() => setRack(data), 2000);
        }
       const fetchResources = async () =>{
           const response = await fetch(`http://0.0.0.0:5000/api/v1/racks/${rackId}/resources`)
           const data = await response.json()
           setTimeout(() => setResources(data), 2000);
       }
       fetchRack()
       fetchResources();
   }, [rackId])

    return(
        <>
        <SideBar />
        <div className='rack-content'>
            <h1>{rack.name}</h1>
            <div className="resource-container">
                <h4>Texts and Web Urls</h4>
                {resources.map((resource) => (resources.type !== 'YouTubeURL' && <Resource
                    title={resource.title}
                    desc={resource.description}
                    type={resource.type}
                    content={resource.content}
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

export default Xplore;