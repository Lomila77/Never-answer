import React, { useState } from 'react';

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
            const blob = new Blob(chunks, { type: 'audio/webm' });
            sendAudio(blob);
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
            <button onClick={recording ? stopRecording : startRecording}>
                {recording ? "⏹️ Stop" : "🎤 Record"}
            </button>
        </div>
    );
}
