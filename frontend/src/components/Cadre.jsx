import { useEffect, useRef } from 'react';

const Cadre = ({ size, componentChildren }) => {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [componentChildren]); // déclenche sur changement de contenu

  const classname =
    size === "small min-h-0"
      ? "flex flex-col items-center justify-center"
      : "flex flex-col  justify-end w-full overflow-y-auto max-h-[80vh] p-4";

  return (
    <div className={classname}>
      {componentChildren}
      <div classname="bottom flex" ref={bottomRef} />
    </div>
  );
};

export default Cadre;
