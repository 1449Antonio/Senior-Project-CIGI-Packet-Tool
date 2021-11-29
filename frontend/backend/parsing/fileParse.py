from dataclasses import fields
from packet import *
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pyshark.capture.pipe_capture import PipeCapture
from uvicorn import run
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/parsefile")
def parse_file(file: UploadFile = File(...)):
    capture = PipeCapture(file.file)
    packets = []
    for capture_packet in capture:
        constructed_object = {}
        if 'IP' in capture_packet:
            # Make new layer and populate with data
            packet_ip_layer = IPLayer()
            packet_ip_layer.source_ip.value = capture_packet.ip.src
            packet_ip_layer.destination_ip.value = capture_packet.ip.dst
            packet_ip_layer.protocol.value = capture_packet.transport_layer
            packet_ip_layer.source_port.value = capture_packet[capture_packet.transport_layer].srcport
            packet_ip_layer.destination_port.value = capture_packet[capture_packet.transport_layer].dstport
            constructed_object['ip_layer'] = dataclasses.asdict(packet_ip_layer)

        if 'cigi' in capture_packet:
            # do the same as above but programmatically 
            cigi_fields = capture_packet.cigi.__dict__['_all_fields']
            packet_fields = fields(Packet)
            for packet_field in packet_fields:
                if f"cigi.{packet_field.name}" not in cigi_fields:
                    continue
                packet_layer = packet_field.type()
                layer_fields = fields(packet_layer)
                for layer_field in layer_fields:
                    if layer_field.name in ("control_size", "control_error", "op_code"):
                        continue
                    label = f"cigi.{packet_field.name}.{layer_field.name}"
                    if label in cigi_fields:
                        est_value = capture_packet.cigi.get_field_value(label)
                        packet_layer[layer_field.name].assign(float(est_value))
                packet_layer['control_size'].assign(float(capture_packet.cigi.get_field_value(f'cigi.{packet_field.name}').size))
                for layer_field in layer_fields:
                    if not isinstance(packet_layer[layer_field.name], LayerField):
                        continue
                    packet_layer[layer_field.name].validate()
                    if packet_layer[layer_field.name].valid is False:
                        packet_layer.control_error = True
                constructed_object[packet_field.name] = dataclasses.asdict(packet_layer)
                if packet_layer.control_error and not packet_field.name is 'user_defined':
                    constructed_object['packet_error'] = True
        packets.append(constructed_object)
    return json.dumps(packets, cls=CustomJSONEncoder)

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)