import Plank from "./Plank";
import Button from "./Button";
import { useEffect, useRef, useState } from "react";
import Cadre from "./Cadre";
import Chat from "./Chat";
import { SendHorizonal } from "lucide-react";

function Form({route, title}) {
    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);
    const ws = useRef(null);
    const description = {
        Course : "Generate a Course\n Provide a topic, and the AI will create a personalized, well-organized course you can revisit anytime to study or review.",
        Evaluation: "Practice & Self-Test\n Get questions and exercises to test your knowledge. The AI gives instant feedback and explanations to help you prepare for exams.",
        Chat:'Learn a Concept\n Chat with the AI to explore a topic, ask questions, and get clear explanations with examples. Perfect for deep understanding',
    }

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

    return <div className={`min-h-0 flex-1 pb-4 flex flex-col ${messages && messages.length > 0 ? "justify-end" : "justify-center gap-6"}`}>
            <Cadre size={messages && messages.length > 0 ? "msg" : "text"} componentChildren={
                messages && messages.length > 0
                ? <Chat messages={messages} />
                : <p className="text-gray-400 text-center p-6 whitespace-pre-line">{description[title]}</p>
            }/>
            <div className="border m-4 border-gray-400 rounded-3xl drop-shadow-xl">
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
                  className="
                    bg-gradient-to-r from-[var(--primary)] to-emerald-400
                    text-white px-4 py-2 rounded-full disabled:opacity-50
                    hover:brightness-110
                    active:scale-95
                    transition-all duration-200
                    flex items-center justify-center
                  "
                >
                  <SendHorizonal
                    size={28}
                    strokeWidth={1.75}
                    className="hover:translate-x-1 transition-transform"
                  />
                </button>
            </form>
        </div>
    </div>
}

export default Form;
