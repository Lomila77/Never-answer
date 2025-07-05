import { useEffect, useRef } from 'react';

const Cadre = ({ size, componentChildren }) => {
  const containerRef = useRef(null);



  useEffect(() => {
    const container = containerRef.current;
    if (container) {
      container.scrollTo({ top: container.scrollHeight, behavior: 'smooth' });
    }
  }, [componentChildren]);

  const classname =
    size === "text"
      ? "flex flex-col items-center justify-center "
      : "flex flex-col justify-end w-full overflow-y-auto p-4";
  return (
    <div ref={containerRef} className={classname}>
      {componentChildren}
      <div className="bottom"  />
    </div>
  );
};

export default Cadre;
