import React, { useEffect, useState } from 'react';
import './Graph.css';
import RollPitchYaw from '../RollPitchYawGraph/RollPitchYaw';
import LatitudeLongitudeGraph from '../LatitudeLogitudeGraph/LatitudeLongitudeGraph';
import AltitudeGraph from '../AltitudeGraph/AltitudeGraph';

function GraphContainer(props) {
const [graphState, setGraphState] = useState(['R','L','A']); // Order in collection is order of rendering: R - Roll Pitch Yaw, L - LatLong, A - Altitude
  
  useEffect(() => {
    setGraphState(['R','L','A']);
  },[]);

  return (
    <div className='GraphMainContainer'>
      <div className="TopGraphContainer"> {/* onClick should pass div index (0 here) and change that this swaps with index 0 and self, here 0 would swap 0 so we dont even need a handler really. */}
        { graphState[0] === 'R' ?
          <RollPitchYaw graphData={props.graphData} />
          : graphState[0] === 'L' ?
          <LatitudeLongitudeGraph graphData={props.graphData} />
          : <AltitudeGraph graphData={props.graphData} /> /*Final case*/
        }
      </div>
      <div className='BottomGraph' onClick={() => {setGraphState([graphState[1], graphState[0], graphState[2]])}}>
        {
          graphState[1] === 'R' ?
          <RollPitchYaw graphData={props.graphData} />
          : graphState[1] === 'L' ?
          <LatitudeLongitudeGraph graphData={props.graphData} />
          : <AltitudeGraph graphData={props.graphData} /> /*Final case*/
        }
      </div>
      <div className='BottomGraph' onClick={() => {setGraphState([graphState[2], graphState[1], graphState[0]])}}>
        {
          graphState[2] === 'R' ?
          <RollPitchYaw graphData={props.graphData} />
          : graphState[2] === 'L' ?
          <LatitudeLongitudeGraph graphData={props.graphData} />
          : <AltitudeGraph graphData={props.graphData} /> /*Final case*/
        }
      </div>
    </div>
  )
}

export default GraphContainer;