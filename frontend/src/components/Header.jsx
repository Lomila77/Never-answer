import Button from "./Button";

const Header = () => {
    return (
        <div className="navbar bg-neutral p-4">
            <Button theme={"dark"} text="Never Answer" to="/"/>
        </div>
    );
};

export default Header;