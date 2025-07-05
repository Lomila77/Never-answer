import { useEffect, useRef } from 'react';

const Cadre = ({ size, componentChildren }) => {
  const bottomRef = useRef(null);


  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
;

  }, [componentChildren]); // déclenche sur changement de contenu

  const classname =
    size === "text"
      ? "flex flex-col items-center justify-center"
      : "flex flex-col justify-end w-full overflow-y-auto max-h-[80vh] p-4";
// changer icic le css pour que le stext soi au centre si p
  return (
    <div className={classname}>
      {componentChildren}
      <div classname="bottom flex" ref={bottomRef} />
    </div>
  );
};

export default Cadre;
