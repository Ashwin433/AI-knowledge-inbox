const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

function App() {
  console.log("frontend loaded", API_URL);
  return (
    <div className="App" style={{padding:"20px",fontFamily: "Arial"}}>
      <h1>AI Knowledge Inbox</h1>
    </div>
  );
}

export default App;