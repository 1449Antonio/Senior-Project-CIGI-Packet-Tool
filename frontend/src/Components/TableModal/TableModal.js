import React from 'react';
import Modal from 'react-bootstrap/Modal'
import ControlAccordion from '../ConctrolAccordion/ControlAccordion';
import './TableModal.css'

function TableModal(props) {
  return (
    <div>
      {JSON.stringify(props.packet) !== '{}'
        ?
        <Modal show={props.show} onHide={props.handleClose} size="xl">
          <Modal.Header>
          </Modal.Header>
          <Modal.Body>
            <ControlAccordion packet={props.packet} />
            <div className="CloseButton"><button onClick={props.handleClose}>Close</button></div>
          </Modal.Body>
        </Modal>
        : null}
    </div>
  )
}

export default TableModal;