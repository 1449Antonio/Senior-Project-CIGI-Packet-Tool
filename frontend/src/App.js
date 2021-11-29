import './App.css';
import Table from './Components/Table/Table';
import { useState } from 'react';
const JSON5 = require('json5');

function App() {
  const [parsedData, setParsedData] = useState([]);

  const getData = (file) => {
    if(file.name.includes('.pcapng') || file.name.includes('.pcap')) {
    const formData = new FormData();
    formData.append('file', file);
    fetch('http://127.0.0.1:8000/parsefile', {
      method: 'POST',
      body: formData,
    }).then(resp => {
      return resp.json();
    }).then(data => {
      let d = JSON5.parse(data);
      setParsedData(d)
    })
  } else {
    alert("Please select a valid file of extension: pcapng or pcap");
  }
  };

  const setInputFile = (file) => {
    getData(file.target.files[0]);
  };


  return (
    <div className="App">
      {
        <div>
            <Table tableData={parsedData} onFileChange={setInputFile} />
        </div>
      }
    </div>
  );
}

export default App;
