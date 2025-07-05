import Plank from '../components/Plank';
import Title from "../components/Title"
import Form from '../components/Form';
import { useState, useEffect } from 'react';
import  Selection  from '../components/Selection';

function Home({route}) {
    const [title, setTitle] = useState("Chat");
    const [selection, setSelection] = useState(null);
    const [isSelectionComplete, setIsSelectionComplete] = useState(false);

    useEffect(() => {
        setTitle(
            route.includes("course")
                ? "Course"
                : route.includes("evaluation")
                    ? "Evaluation"
                    : "Chat"
        );
    }, [route]);

    const handleSubmitSelection = (selection) => {
        setSelection(selection);
        setIsSelectionComplete(true);
        console.log("Selection submitted:", selection);
    }

    return (
    !isSelectionComplete ? (
        <Selection handlesubmitSelection={handleSubmitSelection} />
    ) : (
        <div className='h-screen flex w-full flex-col'>
            <h1 className='text-5xl text-center p-2 text-[var(--primary)]/70 drop-shadow-lg '>{title}</h1>
            <Form route={route} title={title} />
        </div>
    )
);
}

export default Home;
