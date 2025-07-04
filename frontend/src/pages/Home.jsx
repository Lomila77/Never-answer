import Plank from '../components/Plank';
import Title from "../components/Title"
import Form from '../components/Form';


function Home({route}) {

    return <Plank componentChildren={
        <div className='flex flex-col items-start justify-start'>
            <Title size={"large"} content={"Never Answer"} />
            <Form route={route} method={"login"} />
        </div>
    } />
}

export default Home;