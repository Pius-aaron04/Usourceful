import React, { useEffect, useState, useContext } from 'react'
import Header from './header';
import { Link, useNavigate } from 'react-router-dom';
import UserContext from './context';


export function SignUp() {
    const [inputs, setInputs] = useState({});
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleInputChange = (event) => {
        const name = event.target.name;
        const value = event.target.value;
    setInputs(values => ({...values, [name]: value}));
    }
    
    const handleSubmit = async (event) => {
        event.preventDefault();
        if (inputs.confirmPassword === inputs.password){
            try{
                const response = await fetch('http://localhost:5000/api/v1/users',{
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(inputs)
                });

                if (!response.ok){
                    throw new Error(JSON.stringify(response.json()));
                }
                const data = await response.json();
                console.log(data);
                navigate("/login");
            }catch (error){
                setError(error.message);
                console.log(inputs);
                console.log(error.message);
            };
        } else {
            setError('Passwords must match')
        }
    }

    return (
        <>
        <Header sigin={false}/>
        <div className="form-container">
            {error && <p style={{color: "red"}}>{error}</p>}
          <h2>Create an account</h2>
          <form onSubmit={handleSubmit}>
                <label htmlFor="firstname">Firstname
                    <input 
                    value={inputs.firstname || ""}
                    name="firstname"
                    type="text"
                    onChange={handleInputChange}
                    required />
                </label>
                <label htmlFor='lastname'>Lastname
                    <input
                    type="text"
                    name="lastname"
                    value={inputs.lastname || ""}
                    onChange={handleInputChange}
                    required/>
                </label>
                <label htmlFor='username'>Username
                    <input
                    type="text"
                    id="username"
                    name="username"
                    value={inputs.username || ""}
                    onChange={handleInputChange}
                    required/>
                </label>
                <label htmlFor="email">Email:
                    <input
                    type="email"
                    name="email"
                    id="email"
                    value={inputs.email || ""}
                    onChange={handleInputChange}
                    required/>
                </label>
                <label htmlFor="password" >Password
                    <input
                    type="password"
                    id="password"
                    name='password'
                    value={inputs.password || ""}
                    onChange={handleInputChange}
                    required/>
                </label>
                <label htmlFor='confirm-password'>Confirm password
                    <input
                    id='confirm-password'
                    type="password"
                    name='confirmPassword'
                    value={inputs.confirmPassword || ""}
                    onChange={handleInputChange}
                    required/>
                </label>
                <input value="Sign up" type='submit' />
                <p>Do you have an account? <Link to="/login">Log in</Link></p>
            </form>
        </div>
        </>
    );
}

export function SignIn() {
    const {user, isLoggedIn, setValue} = useContext(UserContext)
    const [inputs, setInputs] = useState({});
    const navigate = useNavigate();
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);


    useEffect( () => {
    if (isLoggedIn) return (navigate("/home"));
    }, [isLoggedIn, navigate])

    const handleInputChange = (event) => {
        const name = event.target.name;
        const value = event.target.value;
        setInputs(values => ({...values, [name]: value}))
    }
    const handleSubmit = async (event) => {
        event.preventDefault();
    
        const fetchData = async () => {
            try {
                const response = await fetch('http://localhost:5000/api/v1/auth/me', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(inputs)
                });
    
                if (!response.ok) {
                    throw new Error('Log in Failed');
                }
    
                const data = await response.json();
                localStorage.setItem('user', JSON.stringify(data));
                setValue({ user: data, isLoggedIn: true });
            } catch (error){setError(error.message)}
        }
        setIsLoading(true);
        fetchData();
        setIsLoading(false);
        console.log(user);
        navigate("/home");
    };
    
    return (
        <>
        <Header signin={true}/>
        <div className='form-container'>
            <h2>Welcome!</h2>
            <p>Login to your account</p>
            { !isLoading ?
            <>
            <form onSubmit={handleSubmit}  className="login-form">
                {error && <p style={{color: "red"}}>{error}</p>}
                <label htmlFor="username">Username:
                    <input
                    type="text"
                    name="username"
                    value={inputs.username || ""}
                    onChange={handleInputChange}
                    id="username"
                    required/>
                </label>
                <label htmlFor="password">Password:
                    <input
                    type="password"
                    name='password'
                    id='password'
                    value={inputs.password || ""}
                    onChange={handleInputChange}
                    required/>
                </label>    
                <input type='submit' value="Log in"/>
                <p><a href="/reset/password">Forgot your password?</a> or <Link to="/signup">Sign Up</Link></p>
            </form>
            </> : <img src="./three-11928_256.gif" />}
        </div>
        </>
    )
}
export default SignIn;
