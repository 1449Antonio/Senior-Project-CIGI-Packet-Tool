import React from 'react';
import { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';

let frames = [];
let longitude = [];
let latitude = [];

function LatitudeLongitudeGraph(props) {

  const [graphContent, setGraphContent] = useState([]);
  const createGraphData = (input) => {

    input.forEach(packet => {
      if (packet.ig_control && packet.entity_control) {
        frames.push(packet.ig_control.host_frame_number.value)
        longitude.push(packet.entity_control.lon_yoff.value)
        latitude.push(packet.entity_control.lat_xoff.value)
      }
    });
    
  setGraphContent({
      labels: frames,
      datasets: [
        {
          label: 'Longitude Data',
          data: longitude,
          borderColor: 'pink',
        },
        {
          label: 'Latitude Data',
          data: latitude,
          borderColor: '#fc0303',
        }
      ]
    });

  };

  useEffect(() => {
    while(frames.length)
    frames.pop();
    while (longitude.length)
    longitude.pop();
    while (latitude.length)
    latitude.pop();
    createGraphData(props.graphData);
  }, [props]);

  return (
    <div className="LatLongContainer"> 
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
                text: 'Entity Control Latitude & Longitude Over Time',
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
                text: 'Latitude or Longitude in Degrees'
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


export default LatitudeLongitudeGraph;