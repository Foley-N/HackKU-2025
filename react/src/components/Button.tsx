import React, { Children } from "react";

interface Props{
    children: string;
    color?: 'primary' | 'scondary' | 'danger';
    onClick: () => void;
}

const Button = ({children, onClick, color = 'primary'}: Props) => {
  return (
    <button className={'btn btn-' + color} onClick={onClick} style={{position: 'relative', zIndex: 2}}>
      {children}
    </button>
  )
}

export default Button