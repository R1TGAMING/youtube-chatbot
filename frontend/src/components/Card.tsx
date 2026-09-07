import React from "react";

const Card = ({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) => {
  return (
    <div
      className={
        "flex items-center justify-center rounded hover:scale-105 transition-all duration-300 ease-in-out bg-white " +
        className
      }
    >
      {children}
    </div>
  );
};

export default Card;
