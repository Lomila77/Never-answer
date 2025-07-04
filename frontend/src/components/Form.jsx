import Plank from "./Plank";
import Button from "./Button";
import { useEffect, useRef, useState } from "react";
import Cadre from "./Cadre";
import Chat from "./Chat";

function Form({route, method}) {
    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);
    const ws = useRef(null);

    useEffect(() => {
        // Remplacez l'URL par celle de votre backend WebSocket
        ws.current = new WebSocket("ws://localhost:3001");
        ws.current.onopen = () => {
            console.log("WebSocket connecté");
        };
        ws.current.onmessage = (event) => {
            setMessages(prev => [...prev, event.data]);
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
    }, []);

    const handleSubmit = (e) => {
        e.preventDefault();
        setLoading(true);
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
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
            <div className="messages">
                {messages.map((msg, idx) => (
                    <div key={idx} className="message">{msg}</div>
                ))}
            </div>
        </form>
    </div>
}

export default Form;