import { useState } from "react";
import api from "../api"
import { useNavigate } from "react-router-dom"
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import Username from "./input/username";
import Password from "./input/password";
import Plank from "./Plank";
import NeutralButtonXL from "./Button";

function Form({route, method}) {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate()

    const name = method === "login" ? "Login" : "Register";

    const handleSubmit = async (e) => {
        setLoading(true);
        e.preventDefault();
        try {
            const res = await api.post(route, { username, password })
            if (method === "login") {
                localStorage.setItem(ACCESS_TOKEN, res.data.access);
                localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
                navigate("/")
            } else {
                navigate("/login")
            }
        } catch (error) {
            alert(error)
        } finally {
            setLoading(false)
        }
    }

    return <Plank componentChildren={
        <form onSubmit={handleSubmit} className="form-container">
            <h2 className="text-3xl font-bold text-neutral inner-text-shadow-lg font-sans">{name} :</h2>
            <div className='mb-4'/>
            <Username onChange={setUsername}/>
            <div className='mb-4'/>
            <Password onChange={setPassword}/>
            <div className='mb-4'/>
            <NeutralButtonXL text={name} submit={(e) => handleSubmit(e)}/>
        </form>
    } />
}

export default Form;