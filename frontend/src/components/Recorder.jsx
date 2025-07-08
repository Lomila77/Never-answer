import React, { useState, useRef } from 'react';
import { Mic } from 'lucide-react';


// a modifier dans l'avenir car audio [Deprecation] The ScriptProcessorNode is deprecated. Use AudioWorkletNode instead
export default function VoiceChat({ route, sendAudio }) {
    const [recording, setRecording] = useState(false);
    const audioContextRef = useRef(null);
    const mediaStreamRef = useRef(null);
    const processorRef = useRef(null);
    const sourceRef = useRef(null);
    const audioDataRef = useRef([]);

    const startRecording = async () => {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaStreamRef.current = stream;

        const AudioContext = window.AudioContext || window.webkitAudioContext;
        const audioContext = new AudioContext();
        audioContextRef.current = audioContext;

        const source = audioContext.createMediaStreamSource(stream);
        sourceRef.current = source;

        const processor = audioContext.createScriptProcessor(4096, 1, 1);
        processorRef.current = processor;

        audioDataRef.current = [];

        processor.onaudioprocess = (e) => {
            const channelData = e.inputBuffer.getChannelData(0);
            audioDataRef.current.push(new Float32Array(channelData));
        };

        source.connect(processor);
        processor.connect(audioContext.destination);

        setRecording(true);
    };

    const stopRecording = async () => {
        setRecording(false);

        // Stop mic + disconnect
        processorRef.current.disconnect();
        sourceRef.current.disconnect();
        mediaStreamRef.current.getTracks().forEach(track => track.stop());

        const audioBuffer = flattenAudio(audioDataRef.current);
        const wavBlob = encodeWAV(audioBuffer, audioContextRef.current.sampleRate);
        const testWav = wavBlob.arrayBuffer().then(buffer => {
            const bytes = new Uint8Array(buffer.slice(0, 12));
            const header = String.fromCharCode(...bytes);
            return header})
        console.log("Header avant le send:", testWav); // Doit contenir "RIFF....WAVE"

        if (sendAudio) sendAudio(wavBlob);
    };

    // Concatène tous les buffers audio
    const flattenAudio = (buffers) => {
        const length = buffers.reduce((acc, b) => acc + b.length, 0);
        const result = new Float32Array(length);
        let offset = 0;
        for (const b of buffers) {
            result.set(b, offset);
            offset += b.length;
        }
        return result;
    };

    // Encode en WAV PCM 16 bits
    const encodeWAV = (samples, sampleRate) => {
        const buffer = new ArrayBuffer(44 + samples.length * 2);
        const view = new DataView(buffer);

        const writeString = (offset, str) => {
            for (let i = 0; i < str.length; i++) {
                view.setUint8(offset + i, str.charCodeAt(i));
            }
        };

        const floatTo16BitPCM = (output, offset, input) => {
            for (let i = 0; i < input.length; i++, offset += 2) {
                let s = Math.max(-1, Math.min(1, input[i]));
                s = s < 0 ? s * 0x8000 : s * 0x7FFF;
                view.setInt16(offset, s, true);
            }
        };

        writeString(0, 'RIFF');
        view.setUint32(4, 36 + samples.length * 2, true);
        writeString(8, 'WAVE');
        writeString(12, 'fmt ');
        view.setUint32(16, 16, true); // Subchunk1Size
        view.setUint16(20, 1, true); // PCM
        view.setUint16(22, 1, true); // Mono
        view.setUint32(24, sampleRate, true);
        view.setUint32(28, sampleRate * 2, true);
        view.setUint16(32, 2, true); // Block align
        view.setUint16(34, 16, true); // Bits per sample
        writeString(36, 'data');
        view.setUint32(40, samples.length * 2, true);

        floatTo16BitPCM(view, 44, samples);

        return new Blob([view], { type: 'audio/wav' });
    };

    return (
        <div>
            <button
                type="button"
                onClick={recording ? stopRecording : startRecording}
                className={`btn btn-gray-400 size-10 flex border-none items-center justify-center
                ${recording ? "bg-[var(--primary)] hover:scale-110 hover:brightess-100" :
                    "bg-gray-400 hover:bg-gradient-to-r from-[var(--primary)] to-emerald-400 "}
                    rounded-full p-4 shadow-lg active:scale-95
                    transition-all duration-200`}
            >
                <Mic className="text-white absolute" />
                <span className={`absolute inline-flex size-8 rounded-full -z-10 bg-[var(--primary)] opacity-75` + (recording ? " animate-ping" : "")}></span>
            </button>
        </div>
    );
}
