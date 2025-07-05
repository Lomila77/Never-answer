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
        <div className='h-screen w-full flex flex-col'>
             <h1 className='text-5xl text-emerald-500'>{title}</h1>
            <Form route={route} />
        </div>
        )
}

export default Home;
