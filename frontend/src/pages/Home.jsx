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

    return <Plank componentChildren={
        <div className='flex flex-col items-start justify-start'>
            <Title size={"large"} content={title} />
            <Form route={route} />
        </div>
    } />
}

export default Home;