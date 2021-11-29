import React from 'react';
import { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import './RollPitchYaw.css';

let frame = [];
let roll = [];
let yaw = [];
let pitch = [];

function RollPitchYaw(props) {

  const [graphContent, setGraphContent] = useState([]);
  const createGraphData = (input) => {

    input.forEach(packet => {
      if (packet.ig_control && packet.entity_control) {
        frame.push(packet.ig_control.host_frame_number.value)
        roll.push(packet.entity_control.roll.value)
        yaw.push(packet.entity_control.yaw.value)
        pitch.push(packet.entity_control.pitch.value)
      }
    });
    
  setGraphContent({
      labels: frame,
      datasets: [
        {
          label: 'Roll Data',
          data: roll,
          borderColor: 'blue',
        },
        {
          label: 'Yaw Data',
          data: yaw,
          borderColor: 'pink',
        },
        {
          label: 'Pitch Data',
          data: pitch,
          borderColor: '#fc0303',
        }
      ]
    });
  };

  useEffect(() => {
    while(frame.length)
    frame.pop();
    while (roll.length)
    roll.pop();
    while (yaw.length)
    yaw.pop();
    while (pitch.length)
    pitch.pop();
    createGraphData(props.graphData);
  }, [props]);

  return (
    <div className="RollPitchYawContainer"> 
      <Line legend = {
        {
          display: true,
          position: 'bottom',
        }
      }
      data={graphContent}

      options = {
        {   plugins: {
              title: {
                display: true,
                text: 'Entity Control Yaw, Pitch & Roll Over Time',
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
                text: 'Degrees'
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
      }/>

    </div> 
  )
}


export default RollPitchYaw;