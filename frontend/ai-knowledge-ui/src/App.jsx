import { useState } from "react";


const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

function App() {
  console.log("frontend loaded", API_URL);

  const [text,setText] = useState("");
  const [source,setSource] = useState("note");
  const [question,setQuestion] = useState("");


  const handleIngest = async () => {
    console.log("ingest clicked", text, source);
    try {
      const response = await fetch(`${API_URL}/ingest`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text, source }),
      });

      const result = await response.json();
      console.log("Ingest response:", result);
      alert("Text ingested successfully!");
      setText("");
    } catch (error) {
      console.error("Error ingesting text:", error);
      alert("Failed to ingest text.");
    }
  };

  const handleQuery = async () => {
    console.log("question asked",question);
    try{

    const response = await fetch(`${API_URL}/query`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
    });

    const result = await response.json();
    console.log("Query response:", result);
    alert("Question answered successfully!");
    setQuestion("")
  } catch (error) {
    console.error("Error asking question:", error);
    alert("Failed to get answer.");
  }
  };

  return (
    <div className="App" style={{padding:"20px",fontFamily: "Arial"}}>
      <h1>AI Knowledge Inbox</h1>

      <h3>Add note or url</h3>
      <select value={source} onChange={(e) => setSource(e.target.value)} style={{marginBottom:"10px"}}>
        <option value="note">Note</option>
        <option value="url">URL</option>
        </select>
        <br/><br/>
        <textarea
        rows={4}
        cols={60}
        placeholder="Enter note text or url"
        value={text}
        onChange={(e) => setText(e.target.value)}
        />
        <br/><br/>

        <button onClick={handleIngest}>Save</button>

        <hr/>
        <h3>Ask Question</h3>

        <input
        type="text"
        size={60}
        placeholder="Enter your question"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        />
        <br/><br/>
        <button onClick={handleQuery}>Ask</button>

    </div>
  );
}

export default App;