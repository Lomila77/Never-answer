import Plank from '../components/Plank';
import Title from "../components/Title"
import Form from '../components/Form';
import { useState, useEffect } from 'react';

function Home({route}) {
    const [title, setTitle] = useState("Chat");

    useEffect(() => {
        setTitle(
            route.includes("course")
                ? "Course"
                : route.includes("evaluation")
                    ? "Evaluation"
                    : "Chat"
        );
    }, [route]);

    // return <Plank componentChildren={
        return (
        <div className='h-screen flex w-full flex-col'>
             <h1 className='text-5xl text-center p-2 text-[var(--primary)]/70 drop-shadow-lg '>{title}</h1>
            <Form route={route} title={title} />
        </div>
        )
}

export default Home;
