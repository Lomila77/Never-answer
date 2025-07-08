import { ArrowRight } from "lucide-react";
import React, { useState } from 'react';
import Mbti from "./Mbti";

const Selection = ({handlesubmitSelection}) => {
    const [selectedIndex, setSelectedIndex] = useState(null);
    const [showMbti, setShowMbti] = useState(true);
    const [mbtiSeletion, setMbtiSelection] = useState(null);
    const choices = [
    'history',
    'geography',
    'science',
    'literature',
    'art',
    'music',
    'technology',
    'mathematics',
    'language',
    ];

    return (
        <div className='bg-white/70 w-6/7 *:text-[var(--primary)] border-gray-400 rounded-3xl drop-shadow-xl flex flex-col items-center justify-center gap-4 p-6 max-w-3xl mx-auto'>
            {showMbti ?
            <Mbti setShowMbti={setShowMbti}  setMbtiSelection={setMbtiSelection} />
             :
            <>
            <h2 className='text-3xl text-[var(--primary)] text-center font-bold p-2  drop-shadow-[var(--primary)]/70 brightness-100'>Select a Topic</h2>
            <p className="text-center text-[var(--primary)]"> {`Choose a subject you want to work on and start learning at your own pace.Whether you want to review a lesson, understand a concept, or practice with exercises, this is here to help you improve and succeed!`}</p>
            <div className=' flex flex-wrap justify-center gap-4'>
                {choices.map((choice, index) => (
                    <button
                        key={index}
                        onClick={() => setSelectedIndex(index)}
                        className={`
                            px-4 py-2 rounded-full
                            transition-all duration-200 bg-[var(--secondary)]/20  text-[var(--primary)] font-semibold
                            ${selectedIndex === index
                              ? 'bg-gradient-to-r shadow-emerald-400/40 shadow-lg from-[var(--primary)] brightness-110 to-emerald-400 text-white'
                              : 'bg-[var(--secondary)] hover:text-transparent bg-clip-text hover:bg-gradient-to-r hover:from-[var(--primary)] hover:to-emerald-400'
                            }
                            hover:scale-120
                          `}
                            >
                        {choice}
                    </button>
                ))}
            </div>
            <button
                className=' disabled:opacity-15 hover:shadow-emerald-400/40 hover:shadow-lg transiton-all duration-200 hover:scale-120 !text-white brightness-110 px-6 py-2 rounded-full bg-gradient-to-r from-[var(--primary)] to-emerald-400 transition-colors mt-4'
                onClick={() => handlesubmitSelection(choices[selectedIndex])}
                disabled={selectedIndex === null}
            ><ArrowRight/></button></>}
        </div>
    )
}
export default Selection;
