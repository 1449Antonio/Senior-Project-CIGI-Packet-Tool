import dataclasses, json, types
from dataclasses import dataclass

@dataclass
class LayerField:
    value: any = None
    valid: bool = True
    valid_range: list = None
    validator: types.FunctionType = None
    error_msg: str = ""

    def assign(self, new_value):
        self.value = new_value

    def validate(self):
        if self.validator is not None:
            self.valid = self.validator(self)

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

def inclusiveRangeValidator(field: LayerField) -> bool:
    if field.value is None:
        field.error_msg = "Value is null"
        return False
    if field.valid_range is None:
        return True
    if field.valid_range[0] is not None and field.value < field.valid_range[0]:
        field.error_msg = f"Value outside of valid range (inclusive): {field.valid_range}"
        return False
    if field.valid_range[1] is not None and field.value > field.valid_range[1]:
        field.error_msg = f"Value outside of valid range (inclusive): {field.valid_range}"
        return False
    return True

def discreteValueValidator(field: LayerField) -> bool:
    if field.valid_range is None:
        return True
    if field.value in field.valid_range:
        return True
    field.error_msg = f"Value not found in {field.valid_range}"
    return False

def exclusiveRangeValidator(field: LayerField) -> bool:
    if field.value is None:
        field.error_msg = "Value is null"
        return False
    if field.valid_range is None:
        return True
    if field.valid_range[0] is not None and field.value <= field.valid_range[0]:
        field.error_msg = f"Value outside of valid range (exclusive): {field.valid_range}"
        return False
    if field.valid_range[1] is not None and field.value >= field.valid_range[1]:
        field.error_msg = f"Value outside of valid range (exclusive): {field.valid_range}"
        return False
    return True

@dataclass
class Control:
    control_size: LayerField = LayerField(validator = discreteValueValidator)
    control_error: bool = False

@dataclass
class IPLayer(Control):
    source_ip: LayerField = LayerField()
    destination_ip: LayerField = LayerField()
    protocol: LayerField = LayerField()
    source_port: LayerField = LayerField()
    destination_port: LayerField = LayerField()
    checksums: LayerField = LayerField()

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class IGControl(Control):
    control_size = LayerField(valid_range = [24], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 1)
    db_number: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,127]) # 0 = No load requested , 1 - 127 Identifies desired database
    ig_mode: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,2]) # 0 = Reset/Standby , 1 = Operate, 2 = Debug
    timestamp_valid: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Invalid , 1 = Valid
    extrapolation_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    minor_version: LayerField = LayerField(value = 2)
    host_frame_number: LayerField = LayerField()
    timestamp: LayerField = LayerField()
    last_ig_frame_number: LayerField = LayerField()

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class EntityControl(Control):
    control_size = LayerField(valid_range = [48], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 2)
    entity_id: LayerField = LayerField(validator = inclusiveRangeValidator)
    entity_state: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,2]) # 0 = Inactive/Standby , 1 = Active, 2 = Destroyed
    attach_state: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Detach , 1 = Attach
    coll_det_request: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    inherit_alpha: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Not Inherited , 1 = Inherited
    ground_ocean_clamp: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,2]) # 0 = No Clamp , 1 = Non-Conformal, 2 = Conformal
    animation_dir: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Forward , 1 = Backward
    animation_loop_mode: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = One-Shot , 1 = Continuous
    animation_state: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,3]) # 0 = Stop , 1 = Pause , 2 = Play , 3 = Continue
    extrapolation_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    alpha: LayerField = LayerField()
    entity_type: LayerField = LayerField()
    parent_id: LayerField = LayerField()
    roll: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-180,180])
    pitch: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-90,90])
    yaw: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,360])
    lat_xoff: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-90,90])
    lon_yoff: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-180,180])
    alt_zoff: LayerField = LayerField()

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class ConformalClampedEntityControl(Control):
    control_size = LayerField(valid_range = [24], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 3)
    entity_id: LayerField = LayerField()
    yaw: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,360])
    latitude: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-90,90])
    longitude: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-180,180])

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class ComponentControl(Control):
    control_size = LayerField(valid_range = [32], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 4)
    component_id: LayerField = LayerField()
    instance_id: LayerField = LayerField()
    component_class: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,63]) # 0 = Entity, 1 = View, 2 = View Group, 3 = Sensor, 4 = Regional Sea Surface, 5 = Regional Terrain Surface, 6 = Regional Layered Weather, 7 = Global Sea Surface, 8 = Global Terrain Surface, 9 = Global Layered Weather, 10 = Atmosphere, 11 = Celestial Sphere, 12 = Event, 13 = System, 14 = Symbol Surface, 15 = Symbol, 16–63 = Reserved 
    component_state: LayerField = LayerField()
    component_data: LayerField = LayerField()

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class ShortComponentControl(Control):
    control_size = LayerField(valid_range = [16], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 5)
    component_id: LayerField = LayerField()
    instance_id: LayerField = LayerField()
    component_class: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,63]) # 0 = Entity, 1 = View, 2 = View Group, 3 = Sensor, 4 = Regional Sea Surface, 5 = Regional Terrain Surface, 6 = Regional Layered Weather, 7 = Global Sea Surface, 8 = Global Terrain Surface, 9 = Global Layered Weather, 10 = Atmosphere, 11 = Celestial Sphere, 12 = Event, 13 = System, 14 = Symbol Surface, 15 = Symbol, 16–63 = Reserved 
    component_state: LayerField = LayerField()
    component_data: LayerField = LayerField()

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class ArticulatedPartControl(Control):
    control_size = LayerField(valid_range = [32], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 6)
    entity_id: LayerField = LayerField()
    part_id: LayerField = LayerField()
    articulated_part_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    x_offset_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    y_offset_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    z_offset_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    roll_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    pitch_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    yaw_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    x_offset: LayerField = LayerField()
    y_offset: LayerField = LayerField()
    z_offset: LayerField = LayerField()
    roll: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-180,180])
    pitch: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-90,90])
    yaw: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,360])

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class ShortArticulatedPartControl(Control):
    control_size = LayerField(valid_range = [16], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 7)
    entity_id: LayerField = LayerField()
    part_id_1: LayerField = LayerField()
    part_id_2: LayerField = LayerField()
    dof_select_1: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,6]) # 0 = Not Used, 1 = X Offset, 2 = Y Offset, 3 = Z Offset, 4 = Yaw, 5 = Pitch, 6 = Roll
    dof_select_2: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,6]) # 0 = Not Used, 1 = X Offset, 2 = Y Offset, 3 = Z Offset, 4 = Yaw, 5 = Pitch, 6 = Roll
    part_enable_1: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    part_enable_2: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    dof_1: LayerField = LayerField()
    dof_2: LayerField = LayerField()

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class RateControl(Control):
    control_size = LayerField(valid_range = [32], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 8)
    entity_id: LayerField = LayerField()
    part_id: LayerField = LayerField()
    apply_to_part: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = False , 1 = True
    coordinate_system: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = World/Parent , 1 = Local
    x_rate: LayerField = LayerField()
    y_rate: LayerField = LayerField()
    z_rate: LayerField = LayerField()
    roll_rate: LayerField = LayerField()
    pitch_rate: LayerField = LayerField()
    yaw_rate: LayerField = LayerField()

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class CelestialSphereControl(Control):
    control_size = LayerField(valid_range = [16], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 9)
    hour: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,23])
    minute: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,59])
    ephemeris_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    sun_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    moon_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    star_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    date_time_valid: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Invalid , 1 = Valid
    date: LayerField = LayerField()
    star_intensity: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,100]) 

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class AtmosphereControl(Control):
    control_size = LayerField(valid_range = [32], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 10)
    atmospheric_model_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    humidity: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,100])
    air_temp: LayerField = LayerField()
    visibility_range: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,None]) # Range is >= 0 ICD page 86
    horiz_wind: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,None]) # Range is >= 0 ICD page 86
    vert_wind: LayerField = LayerField() 
    wind_direction: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,360])
    barometric_pressure: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,None]) # Range is >= 0 ICD page 86

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class EnvironmentalRegionControl(Control):
    control_size = LayerField(valid_range = [48], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 11)
    region_id: LayerField = LayerField()
    region_state: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,2]) # 0 = Inactive, 1 = Active, 2 = Destroyed
    merge_weather_properties: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Use Last , 1 = Merge
    merge_aerosol_concentrations: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Use Last , 1 = Merge
    merge_maritime_surface_conditions: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Use Last , 1 = Merge
    merge_terrestrial_surface_conditions: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Use Last , 1 = Merge
    latitude: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-90,90])
    longitude: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-180,180])
    size_x: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,None]) # Range is > 0 ICD page 98
    size_y: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,None]) # Range is > 0 ICD page 98
    corner_radius: LayerField = LayerField() # Range is  0 to lesser of (1/2 * Size X) or (1/2 * Size Y) ICD page 99
    rotation: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-180,180])
    transition_perimeter: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,None]) # Range is >= 0 ICD page 99

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class WeatherControl(Control):
    control_size = LayerField(valid_range = [56], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 12)
    entity_region_id: LayerField = LayerField()
    layer_id: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,255]) # 0 = Ground Fog, 1 = Cloud Layer 1, 2 = Cloud Layer 2, 3 = Cloud Layer 3, 4 = Rain, 5 = Snow, 6 = Sleet, 7 = Hail, 8 = Sand, 9 = Dust, 10 – 255 = Defined by IG
    humidity: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,100])
    weather_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    scud_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    random_winds_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    random_lightning_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    cloud_type: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,15]) # 0 = None, 1 = Altocumulus, 2 = Altostratus, 3 = Cirrocumulus, 4 = Cirrostratus, 5 = Cirrus, 6 = Cumulonimbus, 7 = Cumulus, 8 = Nimbostratus, 9 = Stratocumulus, 10 = Stratus, 11 – 15 = Other
    scope: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,2]) # 0 = Global, 1 = Regional, 2 = Entity
    severity: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,5])
    air_temp: LayerField = LayerField()
    visibility_range: LayerField = LayerField()
    scud_frequency: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,100])
    coverage: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,100])
    base_elevation: LayerField = LayerField()
    thickness: LayerField = LayerField()
    transition_band: LayerField = LayerField()
    horiz_wind: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,None]) # Range is >= 0 ICD page 106
    vert_wind: LayerField = LayerField()
    wind_direction: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,360])
    barometric_pressure: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,None]) # Range is >= 0 ICD page 106
    aerosol_concentration: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,None]) # Range is >= 0 ICD page 106

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class MaritimeSurfaceConditionsControl(Control):
    control_size = LayerField(valid_range = [24], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 13)
    entity_id: LayerField = LayerField()
    surface_conditions_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    whitecap_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    scope: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,2]) # 0 = Global, 1 = Regional, 2 = Entity
    sea_surface_height: LayerField = LayerField()
    surface_water_temperature: LayerField = LayerField()
    surface_clarity: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,100])

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class WaveControl(Control):
    control_size = LayerField(valid_range = [32], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 14)
    entity_id: LayerField = LayerField()
    wave_id: LayerField = LayerField()
    wave_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    scope: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,2]) # 0 = Global, 1 = Regional, 2 = Entity
    breaker_type: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,2]) # 0 = Plunging, 1 = Spilling, 2 = Surging
    wave_height: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,None]) # Range is >= 0 ICD page 112
    wavelenght: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,None]) # Range is >= 0 ICD page 113
    period: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,None]) # Range is >= 0 ICD page 113
    direction: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,360])
    phase_offset: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-360,3600])
    leading: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-180,180])

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class TerrestrialSurfaceConditionsControl(Control):
    control_size = LayerField(valid_range = [8], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 15)
    entity_id: LayerField = LayerField()
    surface_condition_id: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,None])  # 0 = Dry(reset),  > 0 = defined by IG ICD page 115
    severity: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,31]) 
    surface_condition_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    scope: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,2]) # 0 = Global, 1 = Regional, 2 = Entity
    coverage: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,100])

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class ViewControl(Control):
    control_size = LayerField(valid_range = [32], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 16)
    view_id: LayerField = LayerField()
    group_id: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0, 255]) # 0 = None, 1 - 255 = Specifies view group
    xoff_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    yoff_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    zoff_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    roll_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    pitch_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    yaw_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable , 1 = Enable
    entity_id: LayerField = LayerField()
    xoff: LayerField = LayerField()
    yoff: LayerField = LayerField()
    zoff: LayerField = LayerField()
    roll: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-180,180])
    pitch: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-90,90])
    yaw: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,360])

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class SensorControl(Control):
    control_size = LayerField(valid_range = [24], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 17)
    view_id: LayerField = LayerField()
    sensor_id: LayerField = LayerField()
    track_mode: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,7]) # 0 = Off, 1 = Force Correlate, 2 = Scene, 3 = Target, 4 = Ship, 5 – 7 = Defined by IG
    sensor_on_off: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Off, 1 = On
    polarity: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = White hot, 1 = Black hot
    line_by_line_dropout_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable, 1 = Enable
    automatic_gain: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable, 1 = Enable
    track_white_black: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = White, 1 = Black
    response_type: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Normal, 1 = Extended
    gain: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0.0,1.0])
    level: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0.0,1.0])
    ac_coupling: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0.0,None]) # Range is >= 0.0 ICD page 128
    noise: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0.0,1.0])

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class MotionTrackerControl(Control):
    control_size = LayerField(valid_range = [8], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 18)
    view_id: LayerField = LayerField()
    tracker_id: LayerField = LayerField()
    tracker_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable, 1 = Enable
    boresight_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable, 1 = Enable
    x_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable, 1 = Enable
    y_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable, 1 = Enable
    z_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable, 1 = Enable
    roll_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable, 1 = Enable
    pitch_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable, 1 = Enable
    yaw_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable, 1 = Enable
    view_select: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = View, 1 = View Group

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)
@dataclass
class EarthReferenceModelDefinition(Control):
    control_size = LayerField(valid_range = [24], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 19)
    custom_erm_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable, 1 = Enable
    equatorial_radius: LayerField = LayerField()
    flattening: LayerField = LayerField()

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class TrajectoryDefinition(Control):
    control_size = LayerField(valid_range = [24], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 20)
    entity_id: LayerField = LayerField()
    acceleration_x: LayerField = LayerField()
    acceleration_y: LayerField = LayerField()
    acceleration_z: LayerField = LayerField()
    retardation_rate: LayerField = LayerField()
    terminal_velocity: LayerField = LayerField()

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

def viewDefinitionValidator(viewDefinition: any, ):
    return 

@dataclass
class ViewDefinition(Control):
    control_size = LayerField(valid_range = [32], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 21)
    view_id: LayerField = LayerField()
    group_id: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,255]) # 0 = None, 1 - 255 = Specifies View Group
    near_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable, 1 = Enable
    far_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable, 1 = Enable
    left_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable, 1 = Enable
    right_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable, 1 = Enable
    top_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable, 1 = Enable
    bottom_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable, 1 = Enable
    mirror_mode: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,3]) # 0 = None, 1 = Horizontal, 2 = Vertical, 3 = Horizontal and Vertical
    pixel_replication_mode: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,7]) # 0 = None, 1 = 1x2, 2 = 2x1, 3 = 2x2, 4 - 7 = Defined by IG
    projection_type: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Perspective, 1 = Orthographic Parallel
    reorder: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = No Reorder, 1 = Bring to Top
    view_type: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,7]) 
    near: LayerField = LayerField(validator = lambda field: field.value > 0.0 and field.value < far.value) # Range is > 0 to < Far
    far: LayerField = LayerField(validator = lambda field: field.value > near.value) # Range is > Near
    left: LayerField = LayerField(validator = lambda field: field.value > -90.0 and field.value < right.value) # Range is > -90.0 to < Right
    right: LayerField = LayerField(validator = lambda field: field.value > left.value and field.value < 90.0) # Range is > Left to < 90.0
    top: LayerField = LayerField(validator = lambda field: field.value > bottom.value and field.value < 90.0) # Range is > Bottom to < 90.0
    bottom: LayerField = LayerField(validator = lambda field: field.value > -90.0 and field.value < top.value) # Range is > -90.0 to < Top

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class CollisionDetectionSegmentDefinition(Control):
    control_size = LayerField(valid_range = [40], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 22)
    entity_id: LayerField = LayerField()
    segment_id: LayerField = LayerField()
    segment_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable, 1 = Enable
    x1: LayerField = LayerField()
    y1: LayerField = LayerField()
    z1: LayerField = LayerField()
    x2: LayerField = LayerField()
    y2: LayerField = LayerField()
    z2: LayerField = LayerField()
    material_mask: LayerField = LayerField()

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class CollisionDetectionVolumeDefinition(Control):
    control_size = LayerField(valid_range = [48], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 23)
    entity_id: LayerField = LayerField()
    volume_id: LayerField = LayerField()
    volume_enable: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Disable, 1 = Enable
    volume_type: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Sphere, 1 = Cuboid
    x: LayerField = LayerField()
    y: LayerField = LayerField()
    z: LayerField = LayerField()
    height: LayerField = LayerField(validator = exclusiveRangeValidator, valid_range = [0,None]) # Range is > 0
    width: LayerField = LayerField(validator = exclusiveRangeValidator, valid_range = [0,None]) # Range is > 0
    depth: LayerField = LayerField(validator = exclusiveRangeValidator, valid_range = [0,None]) # Range is > 0
    roll: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-180,180])
    pitch: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-90,90])
    yaw: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,360])

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class HatHotRequest(Control):
    control_size = LayerField(valid_range = [32], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 24)
    hat_hot_id: LayerField = LayerField()
    type: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,2]) # 0 = HAT, 1 = HOT, 2 = Extended
    coordinate_system: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Geodetic, 1 = Entity
    update_period: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,None]) # 0 = One-Shot Request, > 0 = Indicates Update Period
    entity_id: LayerField = LayerField()
    lat_xoff: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-90,90])
    lon_yoff: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-180,180])
    alt_zoff: LayerField = LayerField()

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class LineOfSightSegmentRequest(Control):
    control_size = LayerField(valid_range = [64], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 25)
    los_id: LayerField = LayerField()
    type: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Basic, 1 = Extended
    source_coord: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Geodetic, 1 = Entity
    destination_coord: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Geodetic, 1 = Entity
    response_coord: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Geodetic, 1 = Entity
    destination_entity_id_valid: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Not Valid, 1 = Valid
    alpha: LayerField = LayerField()
    entity_id: LayerField = LayerField()
    source_lat_xoff: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-90,90])
    source_lon_yoff: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-180,180])
    source_alt_zoff: LayerField = LayerField()
    destination_lat_xoff: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-90,90])
    destination_lon_xoff: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-180,180])
    destination_alt_xoff: LayerField = LayerField()
    material_mask: LayerField = LayerField()
    update_period: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,None]) # 0 = One-Shot Request, > 0 = Indicates Update Period
    destination_entity_id: LayerField = LayerField()

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class LineOfSightVectorRequest(Control):
    control_size = LayerField(valid_range = [56], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 26)
    los_id: LayerField = LayerField()
    type: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Basic, 1 = Extended
    source_coord: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Geodetic, 1 = Entity
    response_coord: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Geodetic, 1 = Entity
    alpha: LayerField = LayerField()
    entity_id: LayerField = LayerField()
    azimuth: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-180,180])
    elevation: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-90,90])
    min_range: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,None])
    max_range: LayerField = LayerField(validator = lambda field: field.value > min_range.value) # Range is > min_range
    source_lat_xoff: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-90,90])
    source_lon_yoff: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-180,180])
    source_alt_zoff: LayerField = LayerField()
    material_mask: LayerField = LayerField()
    update_period: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,None]) # 0 = One-Shot Request, > 0 = Indicates Update Period

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class PositionRequest(Control):
    control_size = LayerField(valid_range = [8], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 27)
    object_id: LayerField = LayerField() # If Object Class = 0: 0 – 65535,  If Object Class = 1: 0 – 65535,  If Object Class = 2: 0 – 65535, If Object Class = 3: 1 – 255,  If Object Class = 4: 0 – 255 
    part_id: LayerField = LayerField()
    update_mode: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = One-Shot, 1 = Continuous
    object_class: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,4]) # 0 = Entity, 1 = Articulated Part, 2 = View, 3 = View Group, 4 = Motion Tracker
    coord_system: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,2]) # 0 = Geodetic, 1 = Parent Entity, 2 = Submodel

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class EnvironmentalConditionsRequest(Control):
    control_size = LayerField(valid_range = [32], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 28)
    request_id: LayerField = LayerField() 
    type: LayerField = LayerField(validator = discreteValueValidator, valid_range=[1, 2, 4, 8]) # Values are 1 = Maritime Surface Conditions, 2 = Terrestrail Surface Conditions, 4 = Weather Conditions, 8 = Aerosol Concentrations
    lat: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-90,90])
    lon: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-180,180])
    alt: LayerField = LayerField()

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class StartOfFrame(Control):
    control_size = LayerField(valid_range = [24], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 101)
    db_number: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-128,127]) # -128 Indicates database is not available, -127 to -1 Identifies database being loaded, 1 to 127 Identifies database that is loaded, 0 Indicates IG controls database loading
    ig_status: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,255]) # 0 = Normal Operation, 1 - 255 = Defined by IG
    ig_mode: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,3]) # 0 = Reset/Standby, 1 = Operate, 2 = Debug, 3 = Offline Maintenance
    timestamp_valid: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Invaild, 1 = Valid
    earth_reference_model: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = WGS 84, 1 = Host-Defined
    minor_version: LayerField = LayerField(value = 2)
    ig_frame_number: LayerField = LayerField()
    timestamp: LayerField = LayerField()
    last_host_frame_number: LayerField = LayerField()

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class HatHotResponse(Control):
    control_size = LayerField(valid_range = [16], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 102)
    hat_hot_id: LayerField = LayerField()
    valid: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Invalid, 1 = Valid
    type: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = HAT, 1 = HOT
    host_frame_number_lsn: LayerField = LayerField()
    height: LayerField = LayerField()

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class HatHotExtendedResponse(Control):
    control_size = LayerField(valid_range = [40], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 103)
    hat_hot_id: LayerField = LayerField()
    valid: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Invaild, 1 = Valid
    host_frame_number_lsn: LayerField = LayerField()
    hat: LayerField = LayerField()
    hot: LayerField = LayerField()
    material_code: LayerField = LayerField()
    normal_vector_azimuth: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-180,180])
    normal_vector_elevation: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-90,90])

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class LineOfSightResponse(Control):
    control_size = LayerField(valid_range = [16], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 104)
    los_id: LayerField = LayerField()
    valid: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Invaild, 1 = Valid
    entity_id_valid: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Invaild, 1 = Valid
    visible: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Occluded, 1 = Visible
    host_frame_number_lsn: LayerField = LayerField()
    entity_id: LayerField = LayerField()
    range: LayerField = LayerField()

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class LineOfSightExtendedResponse(Control):
    control_size = LayerField(valid_range = [56], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 105)
    los_id: LayerField = LayerField()
    valid: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Invaild, 1 = Valid
    entity_id_valid: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Invaild, 1 = Valid
    range_valid: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Invaild, 1 = Valid
    visible: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Occluded, 1 = Visible
    host_frame_number_lsn: LayerField = LayerField()
    response_count: LayerField = LayerField()
    entity_id: LayerField = LayerField()
    range: LayerField = LayerField()
    lat_xoff: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-90,90])
    lon_yoff: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-180,180])
    alt_zoff: LayerField = LayerField()
    red: LayerField = LayerField()
    green: LayerField = LayerField()
    blue: LayerField = LayerField()
    alpha: LayerField = LayerField()
    material_code: LayerField = LayerField()
    normal_vector_azimuth: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-180,180])
    normal_vector_elevation: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-90,90])

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class SensorResponse(Control):
    control_size = LayerField(valid_range = [24], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 106)
    view_id: LayerField = LayerField()
    sensor_id: LayerField = LayerField()
    sensor_status: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,3]) # 0 = Searching for target, 1 = Tracking target, 2 = Impending breaklock, 3 = Breaklock
    gate_x_size: LayerField = LayerField()
    gate_y_size: LayerField = LayerField()
    gate_x_position: LayerField = LayerField()
    gate_y_position: LayerField = LayerField()
    host_frame_number: LayerField = LayerField()

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class SensorExtendedResponse(Control):
    control_size = LayerField(valid_range = [48], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 107)
    view_id: LayerField = LayerField()
    sensor_id: LayerField = LayerField()
    sensor_status: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,3]) # 0 = Searching for target, 1 = Tracking target, 2 = Impending breaklock, 3 = Breaklock
    entity_id_valid: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Invaild, 1 = Valid
    entity_id: LayerField = LayerField()
    gate_x_size: LayerField = LayerField()
    gate_y_size: LayerField = LayerField()
    gate_x_offset: LayerField = LayerField()
    gate_y_offset: LayerField = LayerField()
    host_frame_number: LayerField = LayerField()
    track_point_latitude: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-90,90])
    track_point_londitude: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-180,180])
    track_point_altitude: LayerField = LayerField()

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class PositionResponse(Control):
    control_size = LayerField(valid_range = [48], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 108)
    object_id: LayerField = LayerField() # If Object Class = 0: 0 – 65535,  If Object Class = 1: 0 – 65535,  If Object Class = 2: 0 – 65535, If Object Class = 3: 1 – 255,  If Object Class = 4: 0 – 255 
    part_id: LayerField = LayerField()
    object_class: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,4]) # 0 = Entity, 1 = Articulated Part, 2 = View, 3 = View Group, 4 = Motion Tracker
    coordinate_system: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,2]) # 0 = Geodetic, 1 = Parent Entity, 2 = Submodel
    lat_xoff: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-90,90])
    lon_yoff: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-180,180])
    alt_zoff: LayerField = LayerField()
    roll: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-180,180])
    pitch: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [-90,90])
    yaw: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,360])

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class WeatherConditionsResponse(Control):
    control_size = LayerField(valid_range = [32], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 109)
    request_id: LayerField = LayerField()
    humidity: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,100])
    air_temp: LayerField = LayerField()
    visibility_range: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,None]) # Range is >= 0 ICD page 244
    horiz_wind: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,None]) # Range is >= 0 ICD page 244
    vert_wind: LayerField = LayerField()
    wind_direction: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,360])
    barometric_pressure: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,None]) # Range is >= 0 ICD page 245

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)


@dataclass
class AerosolConditionsResponse(Control):
    control_size = LayerField(valid_range = [8], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 110)
    request_id: LayerField = LayerField()
    layer_id: LayerField = LayerField()
    aerosol_concentration: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,None]) # Range is >= 0 ICD page 247

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class MaritimeSurfaceConditionsResponse(Control):
    control_size = LayerField(valid_range = [16], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 111)
    request_id: LayerField = LayerField()
    sea_surface_height: LayerField = LayerField()
    surface_water_temperature: LayerField = LayerField()
    surface_clarity: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,100])

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class TerrestrialSurfaceConditionsResponse(Control):
    control_size = LayerField(valid_range = [8], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 112)
    request_id: LayerField = LayerField()
    surface_condition_id: LayerField = LayerField(validator = inclusiveRangeValidator, valid_range = [0,65535])

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class CollisionDetectionsSegmentNotification(Control):
    control_size = LayerField(valid_range = [16], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 113)
    entity_id: LayerField = LayerField()
    segment_id: LayerField = LayerField()
    collision_type: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Non-entity, 1 = Entity
    contacted_entity_id: LayerField = LayerField()
    material_code: LayerField = LayerField()
    intersection_distance: LayerField = LayerField()

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class CollisionDetectionsVolumeNotification(Control):
    control_size = LayerField(valid_range = [16], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 114)
    entity_id: LayerField = LayerField()
    volume_id: LayerField = LayerField()
    collision_type: LayerField = LayerField(validator = discreteValueValidator, valid_range = [0,1]) # 0 = Non-entity, 1 = Entity
    contacted_entity_id: LayerField = LayerField()
    contacted_volume_id: LayerField = LayerField()

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class AnimationStopNotification(Control):
    control_size = LayerField(valid_range = [8], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 115)
    entity_id: LayerField = LayerField()

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class EventNotification(Control):
    control_size = LayerField(valid_range = [16], validator = discreteValueValidator)
    op_code: LayerField = LayerField(value = 116)
    event_id: LayerField = LayerField()
    event_data: LayerField = LayerField()

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class ImageGeneratorMessage(Control):
    control_size = LayerField(valid_range = [], validator = discreteValueValidator) # Size = 4 + message length  the size must be 8 <= (4 + message length) <= 104
    op_code: LayerField = LayerField(value = 117)
    message_id: LayerField = LayerField()

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class UserDefinedData(Control):
    control_size = LayerField(valid_range = [], validator = discreteValueValidator) # Size = 4 + (4 * n) where n is the number of data blocks and the size must be 4 + (4 * n) >= 8
    op_code: LayerField = LayerField(value = 201, validator=inclusiveRangeValidator, valid_range = [None, 117])
    data: LayerField = LayerField()

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

@dataclass
class Packet:
    packet_error: bool = False
    ip_layer: IPLayer = None
    ig_control: IGControl = None
    entity_control: EntityControl = None
    conformal_clamped_entity_control: ConformalClampedEntityControl = None
    component_control: ComponentControl = None
    short_component_control: ShortComponentControl = None
    articulated_part_control: ArticulatedPartControl = None
    short_articulated_part_control: ShortArticulatedPartControl = None
    rate_control: RateControl = None
    celestial_sphere_control: CelestialSphereControl = None
    atmosphere_control: AtmosphereControl = None
    environmental_region_control: EnvironmentalRegionControl = None
    weather_control: WeatherControl = None
    maritime_surface_conditions_control: MaritimeSurfaceConditionsControl = None
    wave_control: WaveControl = None
    terrestrial_surface_conditions_control: TerrestrialSurfaceConditionsControl = None
    view_control: ViewControl = None
    sensor_control: SensorControl = None
    motion_tracker_control: MotionTrackerControl = None
    earth_reference_model_definition: EarthReferenceModelDefinition = None
    trajectory_definition: TrajectoryDefinition = None
    view_definition: ViewDefinition = None
    collision_detection_segment_definition: CollisionDetectionSegmentDefinition = None
    collision_detection_volume_definition: CollisionDetectionVolumeDefinition = None
    hat_hot_request: HatHotRequest = None
    line_of_sight_segment_request: LineOfSightSegmentRequest = None
    line_of_sight_vector_request: LineOfSightVectorRequest = None
    position_request: PositionRequest = None
    environmental_conditions_request: EnvironmentalConditionsRequest = None
    sof: StartOfFrame = None
    hat_hot_response: HatHotResponse = None
    hat_hot_extended_response: HatHotExtendedResponse = None
    line_of_sight_response: LineOfSightResponse = None
    line_of_sight_extended_response: LineOfSightExtendedResponse = None
    sensor_response: SensorResponse = None
    sensor_extended_response: SensorExtendedResponse = None
    position_response: PositionResponse = None
    weather_conditions_response: WeatherConditionsResponse = None
    aerosol_conditions_response: AerosolConditionsResponse = None
    maritime_surface_conditions_response: MaritimeSurfaceConditionsResponse = None
    terrestrial_surface_conditions_response: TerrestrialSurfaceConditionsResponse = None
    collision_detection_segment_notification: CollisionDetectionsSegmentNotification = None
    collision_detection_volume_notification: CollisionDetectionsVolumeNotification = None
    animation_stop_notification: AnimationStopNotification = None
    event_notification: EventNotification = None
    image_generator_message: ImageGeneratorMessage = None
    user_defined: UserDefinedData = None

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

class CustomJSONEncoder(json.JSONEncoder):
        def default(self, dc):
            if isinstance(dc, types.FunctionType):
                return None
            return super().default(dc)