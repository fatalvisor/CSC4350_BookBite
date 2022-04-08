import logo from "./logo.svg";
import "./App.css";
import React, { useState, useEffect } from "react";

// This is how I am planning to implement the React
// Whenever the user click on the book title/image it will send a post request back to the python server
// The post request will have to include the isbn number of that specific book. The React site will handle it from there
// I will have to work with you guys for this

function App() {
  const [book_data, setBookData] = useState([]);
  useEffect(() => {
    fetch("/getbook", { method: "POST" }).then((response) =>
      response.json().then((data) => {
        setBookIsbn(data.book);
      })
    );
  }, [setBookData]);
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
