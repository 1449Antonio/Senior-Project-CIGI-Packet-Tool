import React from 'react';
import Accordion from 'react-bootstrap/Accordion';
import Card from 'react-bootstrap/Card';
import Form from 'react-bootstrap/Form'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import './ControlAccordion.css';
import ErrorIcon from '../Table/warning.png';  // Icons made by Freepik from www.flaticon.com

function ControlAccordion(props) {
  let cardAmount = -1;

  const incrementKey = () => {
    cardAmount = cardAmount + 1;
    return cardAmount;
  };

  return (
    <div>
      {JSON.stringify(props.packet) !== '{}'
        ? <div className="AccordionContainer">
          <Accordion>
            {Object.keys(props.packet).map(packetKey => (
              props.packet[packetKey] !== null && packetKey !== 'packet_error'
                ?
                <Card key={packetKey}>
                  <Card.Header>
                    <Accordion.Toggle style={{ textTransform: 'capitalize' }} className={props.packet[packetKey].control_error ? 'redText' : 'blackText'} as={Card.Header} eventKey={String(incrementKey())}>
                      <div>{props.packet[packetKey].control_error ? <div className="ErrorIconDivAccordion"><img className="ErrorIconImg" src={ErrorIcon} alt="Error Found" /></div> : ''} <div className="ErrorFlaggedTitle">{packetKey.replace(/_/g, ' ')}</div></div>
                    </Accordion.Toggle>
                  </Card.Header>
                  <Accordion.Collapse eventKey={String(cardAmount)}>
                    <Card.Body>
                      <Form.Group>
                        {
                          Object.keys(props.packet[packetKey]).map(attributeKey => (
                            attributeKey !== 'control_error'
                              ?
                              <OverlayTrigger
                                key={packetKey + attributeKey}
                                placement='right'
                                overlay={
                                  props.packet[packetKey][attributeKey].valid ?
                                    <Tooltip>
                                      No Errors Found
                                    </Tooltip>
                                    : <Tooltip>
                                      {props.packet[packetKey][attributeKey].error_msg}
                                    </Tooltip>
                                }
                              >
                                <div key={packetKey + attributeKey}>
                                  <Form.Label style={{ textTransform: 'capitalize' }}>{attributeKey.replace(/_/g, ' ')}</Form.Label>
                                  <Form.Control isInvalid={!props.packet[packetKey][attributeKey].valid} type="text" disabled={1} key={attributeKey + packetKey} placeholder={String(props.packet[packetKey][attributeKey].value).replace(null, '')} />
                                </div>
                              </OverlayTrigger>
                              : null
                          ))
                        }
                      </Form.Group>
                    </Card.Body>
                  </Accordion.Collapse>
                </Card>
                : null
            ))
            }
          </Accordion>
        </div>
        : null}
    </div>
  )
}

export default ControlAccordion;