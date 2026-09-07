const Button = ({
  color = "red",
  textColor = "black",
  borderColor = "black",
  text,
  className,
}: {
  color?: "red" | "blue" | "yellow" | "white" | "black" | "transparent";
  textColor?: "red" | "blue" | "yellow" | "white" | "black";
  borderColor?: "red" | "blue" | "yellow" | "white" | "black";
  text: string;
  className?: string;
}) => {
  const backgroundColors = {
    red: "bg-red-400",
    blue: "bg-blue-400",
    yellow: "bg-yellow-400",
    white: "bg-white",
    black: "bg-black",
    transparent: `bg-transparent border-2`,
  };

  const borderColors = {
    red: "border-red-400",
    blue: "border-blue-400",
    yellow: "border-yellow-400",
    white: "border-white",
    black: "border-black",
  };

  const textColors = {
    red: "text-red-400",
    blue: "text-blue-400",
    yellow: "text-yellow-400",
    white: "text-white",
    black: "text-black",
  };

  return (
    <button
      className={
        `${backgroundColors[color]} p-2 ${textColors[textColor]} text-center font-black rounded cursor-pointer ${borderColors[borderColor]} ` +
        className
      }
    >
      {text}
    </button>
  );
};

export default Button;
