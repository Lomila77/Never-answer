import React, { useState } from 'react';
import {Mic } from 'lucide-react';

export default function VoiceChat({ route, sendAudio }) {
    const [recording, setRecording] = useState(false);
    const [mediaRecorder, setMediaRecorder] = useState(null);

    const startRecording = async () => {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const recorder = new MediaRecorder(stream);
        let chunks = [];

        recorder.ondataavailable = (e) => {
            chunks.push(e.data);
        };

        recorder.onstop = () => {
            const blob = new Blob(chunks, { type: 'audio/wav' });
            // sendAudio(blob);
            chunks = [];
        };

        recorder.start();
        setMediaRecorder(recorder);
        setRecording(true);
    };

    const stopRecording = () => {
        if (mediaRecorder) {
            mediaRecorder.stop();
            setRecording(false);
        }
    };

    return (
        <div>
            <h2>Chat vocal</h2>
            <button onClick={recording ? stopRecording : startRecording}
            className={`btn btn-gray-400 size-10 flex items-center justify-center
                ${recording ? "bg-[var(--primary)] hover:scale-110 hover:brightess-100" :
                     "bg-gray-400 hover:bg-gradient-to-r from-[var(--primary)] to-emerald-400 "}
                      rounded-full p-4 shadow-lg active:scale-95
                    transition-all duration-200`}
            >
                <Mic className=" text-white absolute" />
                <span class={`absolute inline-flex h-full w-full rounded-full bg-sky-400 opacity-75` + (recording ? "animate-ping" : "")}>
                    </span>
                {/* <span class="relative inline-flex size-10 -z-30 rounded-full bg-sky-500">
                    </span> */}
                {/* {recording ? "⏹️ Stop" : "🎤 Record"} */}
            </button>
        </div>
    );
}
