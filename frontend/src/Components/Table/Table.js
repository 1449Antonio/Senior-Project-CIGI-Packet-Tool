import React from 'react';
import { useState, useEffect } from 'react';
import Columns from './Columns';
import TableModal from '../TableModal/TableModal';
import GraphContainer from '../Graph/GraphContainer/GraphContainer';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlus } from '@fortawesome/free-solid-svg-icons'
import './table.css';
import ErrorIcon from './warning.png'; // Icons made by Freepik from www.flaticon.com

function Table(props) {
  const [displayContent, setDisplayContent] = useState([]);
  const [packetInDetail, setPacketInDetail] = useState({});
  const [showTableModal, setShowTableModal] = useState(false);
  const [currentPage, setCurrentPage] = useState(-1);
  const [totalPages, setTotalPages] = useState(-1);
  const [paginatedData, setPaginatedData] = useState({});
  const [currentFilter, setCurrentFilter] = useState(null);

  const handleShowTableModal = () => {
    setShowTableModal(true);
    document.getElementById('root').style.filter = 'blur(5px)'
  };

  const handleHideTableModal = () => {
    document.getElementById('root').style.filter = 'blur(0px)'
    setShowTableModal(false);
    setPacketInDetail({});
  };

  useEffect(() => {
    const Paginated = [];
    let pages = Math.floor(props.tableData.length / 100);
    if (props.tableData.length % 100 !== 0)
      pages++;
    for (let i = 0; i < pages; ++i) {
      Paginated.push(props.tableData.slice(i * 100, (i + 1) * 100));
    }
    setCurrentPage(0);
    setTotalPages(pages - 1);
    if (Paginated.length >= 1) {
      setDisplayContent(Paginated[0]);
      setPaginatedData(Paginated);
    }

  }, [props]);

  const handleNextPage = () => {
    if (currentPage !== totalPages) {
      let nextPage = currentPage + 1;
      setCurrentPage(nextPage);
      if (currentFilter !== null)
        filterEntityControl(currentFilter, paginatedData[nextPage]);
      else
        setDisplayContent(paginatedData[nextPage]);
    }
  };

  const handlePrevPage = () => {
    if (currentPage !== 0) {
      let nextPage = currentPage - 1;
      setCurrentPage(nextPage);
      if (currentFilter !== null)
        filterEntityControl(currentFilter, paginatedData[nextPage]);
      else
        setDisplayContent(paginatedData[nextPage]);
    }
  };

  const handleDirectPage = (formData) => {
    formData.preventDefault();
    let value = formData.target[0].value;
    if ((value >= 1) && (value <= (totalPages + 1))) {
      setCurrentPage(value - 1);
      if (currentFilter !== null)
        filterEntityControl(currentFilter, paginatedData[value - 1]);
      else
        setDisplayContent(paginatedData[value - 1]);
    }
  };

  const onExpand = (event) => {
    setPacketInDetail(event);
    handleShowTableModal();
  };

  const handleSubmitFilter = (formData) => {
    formData.preventDefault();
    filterEntityControl(formData.target[0].value, displayContent);
  };

  const filterEntityControl = (searchValue, packetList) => {
    setCurrentFilter(searchValue);
    const newState = [];
    packetList.forEach(packet => {
      let shouldAdd = false;
      Object.keys(packet).forEach(packetKey => {
        if (packet[packetKey]) {
          if (packet[packetKey].op_code) {
            if (String(packet[packetKey].op_code.value) === String(searchValue)) {
              shouldAdd = true;
            }
          }
        }
      });
      if (shouldAdd) {
        newState.push(packet);
      }
    });
    if (newState.length) {
      setDisplayContent(newState);
    } else {
      alert("No Results!");
      resetTableData();
    }
  };

  const resetTableData = () => {
    setDisplayContent(paginatedData[currentPage]);
    setCurrentFilter(null);
  };
  let i = 0;
  return (
    <React.Fragment>
      <div className='TableWrapper'>
        <form style={{ paddingTop: '1%' }} onSubmit={handleSubmitFilter}>
          <label>
            Filter Opcode:
            <input disabled={displayContent.length === 0} type="text" name="Filter" />
          </label>
          <input disabled={displayContent.length === 0} type="submit" value="Submit" />
          <input disabled={displayContent.length === 0} type="reset" style={{ marginLeft: '1%' }} onClick={resetTableData} />
        </form>
        <div className='MainTable'>
          {
            <div>
              <br />
              <table id='table'>
                <thead>
                  <tr>
                    <th>More</th>
                    <th>Error</th>
                    {Columns.map(entry => (
                      <th key={entry.title}>{entry.title}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {displayContent.length !== 0 ?
                    displayContent.map(packet => (
                      <tr key={JSON.stringify(packet) + i} className={packet.packet_error ? 'Error' : 'NoError'}>
                        <td><button onClick={() => { onExpand(packet); }}><FontAwesomeIcon icon={faPlus} /></button></td>
                        <td style={{width: '10%'}}><div className="ErrorIconDiv">{packet.packet_error ? <img className="ErrorIconImg" src={ErrorIcon} alt="Error Found" /> : ''}</div></td>
                        {
                          Columns.map(col => (
                            <td key={JSON.stringify(col) + ++i}>{
                              packet[col.path[0]] ?
                                packet[col.path[0]][col.path[1]] ?
                                  packet[col.path[0]][col.path[1]].value
                                  : null : null
                            }</td>
                          ))
                        }
                      </tr>
                    )) : null}
                </tbody>
              </table>
            </div>
          }
          <TableModal handleClose={handleHideTableModal} packet={packetInDetail} show={showTableModal} />
        </div>
      </div>
      <GraphContainer graphData={displayContent} />
      <div className="PageNav">
        <div className='PageButtons'>
          <button disabled={displayContent.length === 0} style={{ marginRight: '5%' }} onClick={handlePrevPage}>Prev</button>
          Page {(currentPage + 1) + '/' + (totalPages + 1)}
          <button disabled={displayContent.length === 0} style={{ marginLeft: '5%' }} onClick={handleNextPage}>Next</button>
        </div>
        <form className='PageForm' onSubmit={handleDirectPage}>
          <label>
            Page:
            <input disabled={displayContent.length === 0} style={{ width: '30%' }} type="text" name="Page" />
            <input disabled={displayContent.length === 0} type="submit" value="Submit" />
          </label>
        </form>
        <input style={{ paddingTop: '1%' }} className="UnderInput" type="file" onChange={props.onFileChange} />
      </div>
    </React.Fragment>
  )
}

export default Table;