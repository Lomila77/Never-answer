import Plank from "./Plank";
import Button from "./Button";
import { useEffect, useRef, useState } from "react";
import Cadre from "./Cadre";
import Chat from "./Chat";
import { SendHorizonal } from "lucide-react";
import VoiceChat from "./Recorder";
import {blobToBase64, textToBase64, base64ToText, base64ToBlob} from "../utils";



function Form({route, title}) {
    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);
    const [currentIaMessage, setCurrentIaMessage] = useState("");
    const [isReceived, setIsReceived] = useState(true);

    const ws = useRef(null);
    const description = {
        Course : "Generate a Course\n Provide a topic, and the AI will create a personalized, well-organized course you can revisit anytime to study or review.",
        Evaluation: "Practice & Self-Test\n Get questions and exercises to test your knowledge. The AI gives instant feedback and explanations to help you prepare for exams.",
        Chat:'Learn a Concept\n Chat with the AI to explore a topic, ask questions, and get clear explanations with examples. Perfect for deep understanding',
    }

    useEffect(() => {
        setMessages([]);
        if (!route) return;
        console.log("Connecting to WebSocket at", route);
        ws.current = new WebSocket(route);
        ws.current.onopen = () => {
            console.log("WebSocket connecté");
        };
        ws.current.onmessage = (event) => {
            console.log("Réponse de l'IA :", event.data);
            const data = JSON.parse(event.data);
            if (data.audio) {
                const audioBlob = base64ToBlob(data.audio);
                setMessages(prev => [
                    ...prev,
                    { from: "ia", audio: audioBlob }
                ]);
            }
            else if (data.text) {
                setCurrentIaMessage(prev => prev + data.text);

                setMessages(prev => {
                    if (prev.length > 0 && prev[prev.length - 1].from === "ia") {
                        return prev;
                    }
                    return [...prev, { from: "ia", text: "" }];
                });
            }
            if (data.done) {
                setCurrentIaMessage("");
                setIsReceived(true);
            }
            setLoading(false)
        };
        ws.current.onerror = (err) => {
            console.error("Erreur WebSocket : " + err.message); // permet d'eviter les alertes dans onerror ce qui peux bloquer
        };
        ws.current.onclose = () => {
            console.log("WebSocket déconnecté");
        };
        return () => {
            if (ws.current && ws.current.readyState === WebSocket.OPEN) {
              console.log("Closing websocket...");
              ws.current.close();
            }
            ws.current = null;
          };
    }, [route]);

    useEffect(() => {
        if (currentIaMessage !== "") {
            setIsReceived(false);
            setMessages(prev => {
                if (prev.length === 0) return prev;
                const last = prev[prev.length - 1];
                if (last.from === "ia") {
                    // Met à jour le texte du dernier message IA
                    return [
                        ...prev.slice(0, -1),
                        { ...last, text: currentIaMessage }
                    ];
                }
                return prev;
            });
        }
    }, [currentIaMessage]);

    const sendAudio = async (blob) => {
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            setIsReceived(false);
            const base64Audio = await blobToBase64(blob);
            const message = {
              audio: base64Audio,
            };
            ws.current.send(JSON.stringify(message));
            setMessages(prev => [...prev, { from: "user", audio: blob }]);
        } else {
            alert("WebSocket non connecté");
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (message === "") return;
        setLoading(true);
        setIsReceived(false);
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            setMessages(prev => [
                ...prev,
                { from: "user", text: message }
            ]);
            ws.current.send(JSON.stringify({text: message}));
            setMessage("");
        } else {
            alert("WebSocket non connecté");
        }
        setLoading(false);
    }

    const handleChange = (e) => {
        if(e.which === 13 && !e.shiftKey) {
            $(this).closest("form").submit();
        }
        setMessage(e.target.value);
    }

    return <div className={`min-h-0 flex-1 pb-4 flex flex-col ${messages && messages.length > 0 ? "justify-end" : "justify-center gap-6 max-w-4xl self-center"}`}>
            <Cadre size={messages && messages.length > 0 ? "msg" : "text"} componentChildren={
                messages && messages.length > 0
                ? <Chat messages={messages} />
                : <p className="text-gray-400 text-center p-6 whitespace-pre-line">{description[title]}</p>
            }/>
            <div className=" m-4 bg-white/70 border-gray-400 rounded-3xl drop-shadow-xl">
            <form
            onSubmit={handleSubmit}
            className="flex items-center gap-2 p-4 sticky bottom-0 w-full"
            >
                <VoiceChat disabled={isReceived} sendAudio={sendAudio}/>
                <input
                disabled={!isReceived}
                type="text"
                value={message}
                onChange={(e)=>handleChange(e)}
                placeholder="Votre message"
                className="flex-1 px-4 py-2 h-10 whitespace-pre-wrap text-wrap focus:outline-none"
                />

                <button
                type="submit"
                // disabled={loading}
                disabled={isReceived == false}
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
