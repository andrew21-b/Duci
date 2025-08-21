import React from "react";

export interface SliderProps {
  defaultValue: number[];
  max: number;
  step: number;
  onValueChange: (val: number[]) => void;
}

export const Slider: React.FC<SliderProps> = ({ defaultValue, max, step, onValueChange }) => {
  const [value, setValue] = React.useState(defaultValue[0]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = Number(e.target.value);
    setValue(newValue);
    onValueChange([newValue]);
  };

  return (
    <input
      type="range"
      min={0}
      max={max}
      step={step}
      value={value}
      onChange={handleChange}
      className="w-full accent-blue-600"
    />
  );
};

export default Slider;
