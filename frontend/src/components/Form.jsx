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
            console.log("Réponse de l'IA :", event.data); // 👈 Ajoute ceci
            const data = JSON.parse(event.data);
            if (data.audio) {
                const audioBlob = base64ToBlob(data.audio);
                setMessages(prev => [
                    ...prev,
                    { from: "ia", audio: audioBlob }
                ]);
            }
            else if (data.text) {
                setMessages(prev => [
                ...prev,
                { from: "ia", text: data.text }
            ]);
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

    const sendAudio = async (blob) => {
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
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
        setLoading(true);
        if (message === "")
            return;
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            setMessages(prev => [
                ...prev,
                { from: "user", text: message }
            ]);
            ws.current.send(JSON.stringify({text: message}))
            setMessage("");
        } else {
            alert("WebSocket non connecté");
        }
    }
    // a tester pour voir la performance
    // const handleSubmit = (e) => {
    //     e.preventDefault();
    //     if (message === "") return;
    //     setLoading(true);
    //     // Décale le travail lourd (base64 + WebSocket) pour ne pas bloquer le thread principal
    //     setTimeout(async () => {
    //       if (ws.current && ws.current.readyState === WebSocket.OPEN) {
    //         const base64text = await textToBase64(message);
    //         const message64 = {
    //           text: base64text,
    //         };
    //         ws.current.send(JSON.stringify(message64));
    //         setMessages(prev => [
    //           ...prev,
    //           { from: "user", text: message }
    //         ]);
    //         setMessage("");
    //       } else {
    //         alert("WebSocket non connecté");
    //       }
    //     }, 0);
    //   };

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
                <VoiceChat sendAudio={sendAudio}/>
                <input
                type="text"
                value={message}
                onChange={e => setMessage(e.target.value)}
                placeholder="Votre message"
                className="flex-1 px-4 py-2 focus:outline-none disabled:bg-gray-100"
                />

                <button
                type="submit"
                //disabled={loading}
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
