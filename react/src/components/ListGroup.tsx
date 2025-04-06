import { FC } from "react";

interface Props {
  items: string[];
  heading: string;
  // (item: string) => void
  onSelectItem: (index: number) => void;
}

const ListGroup: FC<Props> = ({ items, heading, onSelectItem }) => {

  return (
    <>
      <h1>{heading}</h1>
      {items.length === 0 && <p>No item found</p>}
      <ul className="list-group">
        {items.map((item, index) => (
          <li
            className="list-group-item"
            key={index}
            onClick={() => onSelectItem(index)}
          >
            {item}
          </li>
        ))}
      </ul>
    </>
  );
}

export default ListGroup;
