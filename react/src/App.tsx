import React,{useEffect, useState } from "react";
import Main from './components/Main';
import Button from "./components/Button";
import ListGroup from './components/ListGroup';
import { JSX } from "react/jsx-runtime";

const App: React.FC=() => {
  const[Activities, setActivities] = useState<Activity[]>([]);
  let items = ["New York", "San Francisco", "Tokyo", "London", "Paris"];
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
  const handleSelectItem = (item: string) => {
     console.log(item);
    }
  const [alertVisible, setAlertVisibility ]=useState(false);

  useEffect(() => {
    fetch('http://localhost:3001/data')
      .then((res) => res.json())
      .then((data: Activity[]) => {
        setActivities(data);
      })
      .catch((err) => {
        console.error('Failed to fetch activities:', err);
      });
  }, []);

  return(
    <div className="App">
      <Main />
      {/* <div className="d-flex justify-content-center mt-3">
        <Button color="primary" onClick={() =>setAlertVisibility(true)}>
          Strat
        </Button>
      </div> */}


      {/* {alertVisible && (
        <div className="alert alert-primary mt-3"> */}
      <div className="alert alert-primary mt-3">
        <ListGroup items={items} heading="Activities Today" onSelectItem={handleSelectItem}/>
        <ListGroup items={items} heading="Screentime" onSelectItem={handleSelectItem}/>
      </div>

      <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Activities</h1>
      <ul className="space-y-2">
        {Activities.map((activity) => (
          <li key={activity.id} className="p-3 rounded shadow border">
            <div><strong>Name:</strong> {activity.activityName ?? 'N/A'}</div>
            <div><strong>Type:</strong> {activity.activityType ?? 'N/A'}</div>
            <div><strong>Distance:</strong> {activity.activityDistance ?? 'N/A'}</div>
            <div><strong>Elapsed Time:</strong> {activity.activityElapsedTime ?? 'N/A'}</div>
            <div><strong>Elevation Gain:</strong> {activity.activityElevationGain ?? 'N/A'}</div>
            <div><strong>Start Time:</strong> {activity.activityStartTime ?? 'N/A'}</div>
            <div><strong>Avg Speed:</strong> {activity.activityAverageSpeed ?? 'N/A'}</div>
            <div><strong>Avg HR:</strong> {activity.activityAverageHR ?? 'N/A'}</div>
          </li>
        ))}
      </ul>
    </div>
      
    </div>
  );
}

export default App;
