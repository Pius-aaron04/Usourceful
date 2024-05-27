import React, { useState } from "react";
import './pages/create.css'
import UserContext from "./context";


export function CreateRack (){
    const [isOpen, setIsOpen] = useState(true);
    const toggleCreateForm = () => {
        setIsOpen(!isOpen);
    }
    return(
        <div className={"create-rack " + isOpen ? 'open' : 'close'}>
            <h3>Create new Rack</h3>
            <form>
                <label for="rack-title" >
                    <input type="text" id="rack-title" name="rackTitle" placeholder="e.g Web development" required/>
                </label>
                <label for="rack-description"><input type="text" id="rack-decription" placeholder="web dev from zero to hero guide"/></label>
                <label for="public"><input type="checkbox" id="public" required/></label>
                <input type="submit" value="Add"/>
            </form>
            <ion-icon name="add-coutline"><button></button></ion-icon>
        </div>
    );
}
