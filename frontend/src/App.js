import React from "react";
import "./App.css"
import UploadAudio from "./components/UploadAudio"

function App(){
  return(
    <div className="App">
      <h1>Music Genre Classification</h1>
      <p>Upload a .au file to classify its genre</p>
      <UploadAudio />
    </div>
  )
}

export default App;