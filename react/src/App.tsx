import React, { useEffect, useState } from "react";
import Main from "./components/Main";
import Button from "./components/Button";
import ListGroup from "./components/ListGroup";
import { JSX } from "react/jsx-runtime";

const App: React.FC = () => {
  const [Activities, setActivities] = useState<Activity[]>([]);
  const [items01, setItems01] = useState<string[]>([]);
  let items02 = ["New York", "San Francisco", "Tokyo", "London", "Paris"];
  const [selectedIndex, setSelectedIndex] = useState<number | null>(null);
  type Activity = {
    id: string;
    activityName: string | null;
    activityType: string | null;
    activityDistance: string | null;
    activityElapsedTime: string | null;
    activityElevationGain: string | null;
    activityStartTime: string | null;
    activityAverageSpeed: string | null;
    activityAverageHR: string | null;
  };
  const handleSelectItem = (index: number) => {
    setSelectedIndex(index === selectedIndex ? null : index);
  };
  const [alertVisible, setAlertVisibility] = useState(false);

  useEffect(() => {
    fetch("http://localhost:3001/data")
      .then((res) => res.json())
      .then((data: Activity[]) => {
        setActivities(data);

        const dynamicItems = data.map(
          (activity) =>
            `${"Name: " + activity.activityName} | ${
              "Start Time: " + activity.activityStartTime
            }`
        );
        setItems01(dynamicItems);
      })
      .catch((err) => {
        console.error("Failed to fetch activities:", err);
      });
  }, []);

  useEffect(() => {
    fetch("http://localhost:3001/data")
      .then((res) => res.json())
      .then((data: Activity[]) => {
        setActivities(data);
      })
      .catch((err) => {
        console.error("Failed to fetch activities:", err);
      });
  }, []);
  const handleClick = (item: string, index: number) => {
    setSelectedIndex(index === selectedIndex ? null : index);
  };

  
  return (
    <div className="App">
      <Main />

      <div className="alert alert-primary mt-3">
        <ListGroup
          items={items01}
          heading="Activities Today"
          onSelectItem={handleSelectItem}
        />

        {/* 선택된 항목에 해당하는 데이터만 출력 */}
        {selectedIndex !== null && (
          <div className="p-4">
            <div className="p-3 rounded shadow border">
              <div>
                <strong>Name:</strong>{" "}
                {Activities[selectedIndex].activityName ?? "N/A"}
              </div>
              <div>
                <strong>Type:</strong>{" "}
                {Activities[selectedIndex].activityType ?? "N/A"}
              </div>
              <div>
                <strong>Distance:</strong>{" "}
                {Activities[selectedIndex].activityDistance ?? "N/A"}
              </div>
              <div>
                <strong>Elapsed Time:</strong>{" "}
                {Activities[selectedIndex].activityElapsedTime ?? "N/A"}
              </div>
              <div>
                <strong>Elevation Gain:</strong>{" "}
                {Activities[selectedIndex].activityElevationGain ?? "N/A"}
              </div>
              <div>
                <strong>Start Time:</strong>{" "}
                {Activities[selectedIndex].activityStartTime ?? "N/A"}
              </div>
              <div>
                <strong>Avg Speed:</strong>{" "}
                {Activities[selectedIndex].activityAverageSpeed ?? "N/A"}
              </div>
              <div>
                <strong>Avg HR:</strong>{" "}
                {Activities[selectedIndex].activityAverageHR ?? "N/A"}
              </div>
            </div>
          </div>
        )}

        <ListGroup
          items={items02}
          heading="Screentime"
          onSelectItem={handleSelectItem}
        />
      </div>
    </div>
  );
};

export default App;
