import Plank from "./Plank";
import Button from "./Button";
import { useEffect, useRef, useState } from "react";
import Cadre from "./Cadre";
import Chat from "./Chat";
import { SendHorizonal } from "lucide-react";

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

    return <div className="min-h-0 flex-1 pb-4 flex flex-col justify-end">
            <Cadre size={"large"} componentChildren={
                <Chat messages={messages}/>
            }/>
        <div className="border m-4 border-gray-600 rounded-3xl drop-shadow-xl">
            <form
            onSubmit={handleSubmit}
            className="flex items-center gap-2 p-4 sticky bottom-0 w-full"
            >
                <input
                type="text"
                value={message}
                onChange={e => setMessage(e.target.value)}
                placeholder="Votre message"
                className="flex-1 px-4 py-2 focus:outline-none  disabled:bg-gray-100"
                disabled={loading}
                />

                <button
                type="submit"
                disabled={loading}
                className="bg-emerald-400 text-white px-4 py-2 rounded-full hover:bg-emerald-700 disabled:opacity-50"
                >
                    <SendHorizonal size={28} strokeWidth={1.75} absoluteStrokeWidth />
                </button>
            </form>
        </div>
    </div>
}

export default Form;
