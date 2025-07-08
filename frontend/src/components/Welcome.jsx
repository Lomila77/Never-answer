import React from "react";
import GradientButton from "./ButtonGradient";

const Welcome = ({ setWelcomeDisplayed }) => {
    return (
        <div className=" p-2 gap-6 flex-col flex justify-center text-center text-[var(--primary)] items-center bg-white/70 backdrop-blur-md rounded-3xl drop-shadow-xl w-full max-w-3xl mx-auto h-fit">
            <h1 className="text-2xl sm:text-2xl">Welcome to <span className="font-bold text-emerald-400"> SocraticIA</span></h1>
            <p className=" text-lg">
                SocraticIA is an AI-powered platform designed to enhance your learning experience through interactive courses and personalized evaluations.
            </p>
            <GradientButton onClick = {() => setWelcomeDisplayed(false)} className="w-fit self-center"> get started </GradientButton>
        </div>
    );
}

export default Welcome;
