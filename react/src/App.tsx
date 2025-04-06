import React, { useEffect, useState } from "react";
import Main from "./components/Main";
import Button from "./components/Button";
import ListGroup from "./components/ListGroup";
import { JSX } from "react/jsx-runtime";
import ListGroups from "./components/ListGroups";

const App: React.FC = () => {
  const [Activities, setActivities] = useState<Activity[]>([]);
  const [Wellbeing, setWellbeing] = useState<Wellbeing[]>([]);
  const [items01, setItems01] = useState<string[]>([]);
  const [items02, setItems02] = useState<string[]>([]);
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

  type Wellbeing = {
    id: string;
    deviceName: string | null;
    timeUsage: string | null;
    timeGoal: string | null;
    dateUsage: string | null;
    mostUsedApp: string | null;
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
    fetch("http://localhost:3001/wellbeing")
      .then((res) => res.json())
      .then((data: Wellbeing[]) => {
        setWellbeing(data);

        const dynamicItems = data.map((wellbeing) => [
          `Device Name: ${wellbeing.deviceName}`,
          `Time Usage: ${wellbeing.timeUsage} mins`,
          `Time Goal: ${wellbeing.timeGoal} mins`,
          `Date Usage: ${wellbeing.dateUsage}`,
          `Most Used App: ${wellbeing.mostUsedApp}`,
        ]);
        setItems02(dynamicItems.flat());
      })
      .catch((err) => {
        console.error("Failed to fetch wellbeing data:", err);
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
        <div className="alert alert-primary mt-3">
          <ListGroups items={items02} heading="Screentime" />
        </div>
      </div>
    </div>
  );
};

export default App;
