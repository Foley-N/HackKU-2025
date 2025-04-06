import { FC } from "react";

interface Props {
  items: string[];
  heading: string;
}

const ListGroups: FC<Props> = ({ items, heading }) => {

  return (
    <>
      <h1>{heading}</h1>
      {items.length === 0 && <p>No item found</p>}
      <ul className="list-group">
        {items.map((item, index) => (
          <li
            className="list-group-item"
            key={index}
          >
            {item}
          </li>
        ))}
      </ul>
    </>
  );
}

export default ListGroups;
