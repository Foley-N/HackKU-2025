import React from 'react'
import { useState } from "react";
import Main from './components/main';
import Button from "./components/Button";
import ListGroup from './components/ListGroup';

function App() {
  let items = ["New York", "San Francisco", "Tokyo", "London", "Paris"];
  const handleSelectItem = (item: string) => {
     console.log(item);
    }
  const [alertVisible, setAlertVisibility ]=useState(false);
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
        <ListGroup items={items} heading="Activities" onSelectItem={handleSelectItem}/>
        <ListGroup items={items} heading="Screentime" onSelectItem={handleSelectItem}/>
      </div>

      
    </div>
  );
}

export default App;
