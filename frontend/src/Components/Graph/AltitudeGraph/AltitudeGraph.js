import React from 'react';
import { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';

let frames = [];
let altitude = [];

function AltitudeGraph(props) {
  const [graphContent, setGraphContent] = useState([]);
  const createGraphData = (input) => {

    input.forEach(packet => {
      if (packet.ig_control && packet.entity_control) {
        frames.push(packet.ig_control.host_frame_number.value)
        altitude.push(packet.entity_control.alt_zoff.value)
      }
    });

    setGraphContent({
      labels: frames,
      datasets: [
        {
          label: 'Altitude Data',
          data: altitude,
          borderColor: 'blue',
        }
      ]
    });
  };

  useEffect(() => {
    while (frames.length)
      frames.pop();
    while (altitude.length)
      altitude.pop();
    createGraphData(props.graphData);
  }, [props]);

  return (
    <div className="AltitudeContainer">
      <Line legend={
        {
          display: true,
          position: 'bottom',
        }
      }
        data={graphContent}

        options={
          {
            plugins: {
              title: {
                display: true,
                text: 'Entity Control Altitude Over Time',
                position: 'top'
              },
              legend: {
                display: true,
                position: 'bottom'
              }
            },
            scales: {
              yAxes: {
                title: {
                  display: true,
                  text: 'Altitude in Meters'
                },
                offset: true
              },
              xAxes: {
                title: {
                  display: true,
                  text: "Time by Increasing Frame Number"
                }
              }
            }
          }
        } />

    </div>
  )
}


export default AltitudeGraph;