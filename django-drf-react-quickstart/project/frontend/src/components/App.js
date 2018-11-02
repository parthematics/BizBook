import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import Table from "./Table";
import React, { Component } from 'react';
import './App.css';
import Header from './components/Header';

class App extends Component {
      render() {
        return (
          <Header />
        );
      }
    }
    export default App;

const App = () => (
  <DataProvider endpoint="api/lead/"
                render={data => <Table data={data} />} />
);
const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render(<App />, wrapper) : null;
