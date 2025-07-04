import Plank from "./Plank";
import Button from "./Button";
import { useEffect, useRef, useState } from "react";
import Cadre from "./Cadre";
import Chat from "./Chat";

function Form({route}) {
    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);
    const ws = useRef(null);

    useEffect(() => {
        setMessages([]);
        ws.current = new WebSocket(route);
        ws.current.onopen = () => {
            console.log("WebSocket connecté");
        };
        ws.current.onmessage = (event) => {
            setMessages(prev => [
                ...prev,
                { from: "ia", text: event.data }
            ]);
        };
        ws.current.onerror = (err) => {
            alert("Erreur WebSocket : " + err.message);
        };
        ws.current.onclose = () => {
            console.log("WebSocket déconnecté");
        };
        return () => {
            ws.current && ws.current.close();
        };
    }, [route]);


    const handleSubmit = (e) => {
        e.preventDefault();
        setLoading(true);
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            setMessages(prev => [
                ...prev,
                { from: "user", text: message }
            ]);
            ws.current.send(message);
            setMessage("");
        } else {
            alert("WebSocket non connecté");
        }
        setLoading(false);
    }

    return <div>
            <Cadre size={"large"} componentChildren={
                <Chat messages={messages}/>
            }/>
            <form onSubmit={handleSubmit} className="form-container">
                <div className='mb-4'/>
                <input
                type="text"
                value={message}
                onChange={e => setMessage(e.target.value)}
                placeholder="Votre message"
                className="input"
                disabled={loading}
            />
            <div className='mb-4'/>
            <Button theme={"dark"} text="Envoyer" submit={handleSubmit}/>
            <div className='mb-4'/>
        </form>
    </div>
}

export default Form;