import React, { useState, useRef } from 'react';
import {Mic } from 'lucide-react';

export default function VoiceChat({ route, sendAudio }) {
    const [recording, setRecording] = useState(false);
    const mediaRecorderRef = useRef(null);
    const chunksRef = useRef([]);
    const streamRef = useRef(null);

    const startRecording = async () => {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        streamRef.current = stream;
        const recorder = new MediaRecorder(stream);

        chunksRef.current = [];

        recorder.ondataavailable = (e) => {
            if (e.data.size > 0) {
                chunksRef.current.push(e.data);
            }
        };

        recorder.onstop = () => {
            const blob = new Blob(chunksRef.current, { type: 'audio/wav' });
            if (sendAudio) sendAudio(blob);
            chunksRef.current = [];
            setRecording(false);
            // Arrête le flux micro
            stream.getTracks().forEach(track => track.stop());
        };

        mediaRecorderRef.current = recorder;
        recorder.start();
        setRecording(true);
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current) {
            mediaRecorderRef.current.stop();
            setRecording(false);
        }
    };

    return (
        <div>
            {recording ? <p>true </p> : <p>false</p>}
            <button
                type="button"
                onClick={recording ? stopRecording : startRecording}
                className={`btn btn-gray-400 size-10 flex border-none items-center justify-center
                ${recording ? "bg-[var(--primary)] hover:scale-110 hover:brightess-100" :
                     "bg-gray-400 hover:bg-gradient-to-r from-[var(--primary)] to-emerald-400 "}
                      rounded-full p-4 shadow-lg active:scale-95
                    transition-all duration-200`}
            >
                <Mic className=" text-white absolute" />
                <span className={`absolute inline-flex size-8 rounded-full -z-10 bg-[var(--primary)] opacity-75` + (recording ? " animate-ping" : "")}>
                </span>
            </button>
        </div>
    );
}
