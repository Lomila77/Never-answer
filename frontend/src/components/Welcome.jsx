import React from "react";
import GradientButton from "./ButtonGradient";

const Welcome = ({ setWelcomeDisplayed }) => {
    return (
        <div className=" p-2 gap-6 flex-col flex justify-center text-center text-[var(--primary)] items-center bg-white/70 backdrop-blur-md rounded-3xl drop-shadow-xl w-full max-w-3xl mx-auto h-fit">
            <h1 className="text-2xl sm:text-2xl">Welcome to <span className="font-bold text-emerald-400"> FlowrishAI</span></h1>
            <p className=" text-lg">
            Flow is the state where learning feels effortless — not because it’s easy, but because it’s exactly the right kind of challenge.

            At Flowrish.ai, we don’t give you answers.
            We help you stay in that zone — focused, curious, and in control.
            Through adaptive prompts, interactive courses, and just-in-time guidance, Flowrish keeps your mind challenged — never overwhelmed, never bored.

            This is where real learning happens.
            Let the journey begin.            
                        </p>
            <GradientButton onClick = {() => setWelcomeDisplayed(false)} className="w-fit self-center"> get started </GradientButton>
        </div>
    );
}

export default Welcome;
