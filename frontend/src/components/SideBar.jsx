import Book from '../assets/book.png'
import Evaluation from '../assets/evaluation.png'
import Message from '../assets/chat.png'
import { useState } from 'react';
import { MessageCircle, GraduationCap, BookCheck } from 'lucide-react';
import React from 'react';

const SideBar = ({ setRoute }) => {
  const [activeButton, setActiveButton] = useState("ws://localhost:8000/ws");
  const [hoveredButton, setHoveredButton] = useState(null);

  const handleButtonClick = (route) => {
    setRoute(route);
    setActiveButton(route);
  };

  const buttons = [
    {
      route: "ws://localhost:8000/ws",
      icon: <MessageCircle />,
      label: "Chat"
    },
    {
      route: "ws://localhost:8000/ws/course",
      icon: <GraduationCap />,
      label: "Course"
    },
    {
      route: "ws://localhost:8000/ws/evaluation",
      icon: <BookCheck />,
      label: "evaluate"
    }
  ];

  return (
    <drawer className="felx flex-col bg-white shadow-2xl text-primary-content w-16 md:w-20 ">
      <div className="flex flex-col py-2 w-full items-center gap-6">
      {buttons.map((button) => (
          <div
            key={button.route}
            className="relative group"
            onMouseEnter={() => setHoveredButton(button.route)}
            onMouseLeave={() => setHoveredButton(null)}
          >
            <button
              onClick={() => handleButtonClick(button.route)}
              className={`active:scale-95 transition-transform p-2 w-full rounded-lg ${
                activeButton === button.route ? 'bg-[var(--primary)]/10' : ''
              }`}
            >
              {React.cloneElement(button.icon, {
                className: `${
                  activeButton === button.route ? 'text-[#04A3A9]' : 'text-gray-400'
                } hover:text-[#04A3A9] transition-colors duration-200`
              })}
            </button>

            {/* Étiquette (Tooltip) */}
            {hoveredButton === button.route && (
              <div className="absolute left-full ml-3 top-1/2 transform -translate-y-1/2">
                <div className="bg-white text-gray-400 text-xs font-medium px-2 py-2 rounded whitespace-nowrap">
                  {button.label}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </drawer>
  );
};

export default SideBar;
