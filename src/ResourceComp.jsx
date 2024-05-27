import React from 'react';

const Resource = (props) => {
    return (
        <div className="resource">
            <h3><a href="https://youtube.com">Youtube vid</a></h3>
            <div className='resource-content'>
                <p>Hello here is what i have here<br />https://youtube.com</p>
            </div>
            <p>Resource type</p>
        </div>
    );
}

export default Resource;