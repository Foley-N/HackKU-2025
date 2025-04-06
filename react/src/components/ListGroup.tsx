import { useState } from "react";

interface Props {
  items: string[];
  heading: string;
  // (item: string) => void
  onSelectItem: (item: string) => void;
}

function ListGroup({ items, heading, onSelectItem }: Props) {
  //Hook
  const [selectedIndex, setSelectedIndex] = useState<number | null>(null);

  //Event handler
  const handleClick = (item: string, index: number) => {
    setSelectedIndex(index === selectedIndex ? null : index);
    onSelectItem(item);
  }

  return (
    <>
      <h1>{heading}</h1>
      {items.length === 0 && <p>No item found</p>}
      <ul className="list-group">
        {items.map((item, index) => (
          <li
            className={
              selectedIndex === index
                ? "list-group-item active"
                : "list-group-item"
            }
            key={item}
            onClick={() => handleClick(item, index)}
          >
            {item}
            {selectedIndex === index && (
              <div className="additional-content mt-2">
                <p>This is additional content for {item}.</p>
              </div>
            )}
          </li>
        ))}
      </ul>
    </>
  );
}

export default ListGroup;
