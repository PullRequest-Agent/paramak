""" This example uses parametric_shapes to constuct a simple ball reactor geometry"""

from paramak import Reactor

# imports several parametric shapes that are used later
from paramak.parametric_shapes import (
    PlasmaShape,
    BlanketConstantThickness,
    DivertorBlock,
    CenterColumnShieldCylinder,
    PoloidalFieldCoil,
    PoloidalFieldCoilCase,
)


def make_reactor(
    output_folder="ball_reactor",
    rotation_angle=180,
    major_radius=350,
    minor_radius=156,
    triangularity=0.55,
    elongation=2.0,
    center_column_shield_inner_radius=100,
    center_column_shield_outer_radius=150,
    blanket_thickness=200,
    blanket_offset_from_plasma=80,
    blanket_start_angle=110,
    blanket_stop_angle=250,
    plasma_color=[0.95, 0.41, 0.7, 0.8],
    firstwall_color=[0.2, 0.2, 0.2],
    blanket_color=[0.4, 0.1, 0.4],
    divertor_color=[0.1, 0.35, 0.1],
    blanket_rear_wall_color=[0.2, 0.2, 0.2],
    centre_column_color=[0.15, 0.15, 0.45],
    poloidal_magnet_color=[0.45, 0.31, 0.8],
    poloidal_magnet_case_color=[0.9, 0.31, 0.2],
    inboard_toroidal_magnet_color=[0.55, 0.3, 0.15],
    outboard_toroidal_magnet_color=[0.55, 0.3, 0.15],
):
    """
       This function creates parametric shapes from the provided arguments and 
       adds them to a reactor object which is returned at the end of the function
    """

    # these parametes are defined from others which saves having
    # to pass even more arguments to the function
    divertor_lower_stop_angle = blanket_stop_angle
    divertor_upper_stop_angle = blanket_start_angle
    divertor_start_x_value = center_column_shield_outer_radius
    divertor_thickness = blanket_thickness
    divertor_offset_from_plasma = blanket_offset_from_plasma

    # initiates a reactor object to store the shapes
    my_reactor = Reactor()
    plasma = PlasmaShape(
        major_radius=major_radius,
        minor_radius=minor_radius,
        triangularity=triangularity,
        elongation=elongation,
        rotation_angle=rotation_angle,
        color=plasma_color,
        stp_filename="plasma.stp",
        material_tag="DT_plasma",
    )
    my_reactor.add_shape(plasma)

    # creates a blanket from the parametric shape
    blanket = BlanketConstantThickness(
        major_radius=major_radius,
        minor_radius=minor_radius,
        triangularity=triangularity,
        elongation=elongation,
        thickness=blanket_thickness,
        start_angle=blanket_start_angle,
        stop_angle=blanket_stop_angle,
        offset_from_plasma=blanket_offset_from_plasma,
        rotation_angle=rotation_angle,
        color=blanket_color,
        stp_filename="blanket.stp",
        material_tag="blanket_material",
    )
    my_reactor.add_shape(blanket)

    # creates an upper divertor from the parametric shape
    divertor_upper = DivertorBlock(
        major_radius=major_radius,
        minor_radius=minor_radius,
        triangularity=triangularity,
        elongation=elongation,
        thickness=divertor_thickness,
        stop_angle=divertor_upper_stop_angle,
        offset_from_plasma=divertor_offset_from_plasma,
        start_x_value=divertor_start_x_value,
        rotation_angle=rotation_angle,
        color=divertor_color,
        stp_filename="divertor_upper.stp",
        material_tag="divertor_material",
    )
    my_reactor.add_shape(divertor_upper)

    # creates a lower divertor from the parametric shape
    divertor_lower = DivertorBlock(
        major_radius=major_radius,
        minor_radius=minor_radius,
        triangularity=triangularity,
        elongation=elongation,
        thickness=divertor_thickness,
        stop_angle=divertor_lower_stop_angle,
        offset_from_plasma=divertor_offset_from_plasma,
        start_x_value=divertor_start_x_value,
        rotation_angle=rotation_angle,
        color=divertor_color,
        stp_filename="divertor_lower.stp",
        material_tag="divertor_material",
    )
    my_reactor.add_shape(divertor_lower)

    # The height of this center column is calculated using CadQuery commands
    center_column_shield = CenterColumnShieldCylinder(
        height=divertor_upper.solid.vertices(">Z").val().Vertices()[0].Z * 2.0,
        inner_radius=center_column_shield_inner_radius,
        outer_radius=center_column_shield_outer_radius,
        rotation_angle=rotation_angle,
        color=centre_column_color,
        stp_filename="center_column_shield.stp",
        material_tag="center_column_material",
    )
    my_reactor.add_shape(center_column_shield)

    # creates a PF coil (internal)
    pf_coil_1 = PoloidalFieldCoil(
        height=30,
        width=30,
        center_point=(600, 500),
        rotation_angle=rotation_angle,
        stp_filename="pf_coil_1.stp",
        material_tag="pf_coil_material",
    )
    my_reactor.add_shape(pf_coil_1)

    # creates a PF coil (casing)
    pf_coil_1_case = PoloidalFieldCoilCase(
        casing_thickness=10,
        coil_height=30,
        coil_width=30,
        center_point=(600, 500),
        rotation_angle=rotation_angle,
        color=poloidal_magnet_case_color,
        stp_filename="pf_coil_case_1.stp",
        material_tag="pf_coil_material",
    )
    my_reactor.add_shape(pf_coil_1_case)

    pf_coil_2 = PoloidalFieldCoil(
        height=30,
        width=30,
        center_point=(600, -500),
        rotation_angle=rotation_angle,
        stp_filename="pf_coil_2.stp",
        material_tag="pf_coil_material",
    )
    my_reactor.add_shape(pf_coil_2)

    pf_coil_2_case = PoloidalFieldCoilCase(
        casing_thickness=10,
        coil_height=30,
        coil_width=30,
        center_point=(600, -500),
        rotation_angle=rotation_angle,
        color=poloidal_magnet_case_color,
        stp_filename="pf_coil_case_2.stp",
        material_tag="pf_coil_material",
    )
    my_reactor.add_shape(pf_coil_2_case)

    pf_coil_3 = PoloidalFieldCoil(
        height=30,
        width=30,
        center_point=(800, -200),
        rotation_angle=rotation_angle,
        stp_filename="pf_coil_3.stp",
        material_tag="pf_coil_material",
    )
    my_reactor.add_shape(pf_coil_3)

    pf_coil_3_case = PoloidalFieldCoilCase(
        casing_thickness=10,
        coil_height=30,
        coil_width=30,
        center_point=(800, -200),
        rotation_angle=rotation_angle,
        color=poloidal_magnet_case_color,
        stp_filename="pf_coil_case_3.stp",
        material_tag="pf_coil_material",
    )
    my_reactor.add_shape(pf_coil_3_case)

    pf_coil_4 = PoloidalFieldCoil(
        height=30,
        width=30,
        center_point=(800, 200),
        rotation_angle=rotation_angle,
        stp_filename="pf_coil_4.stp",
        material_tag="pf_coil_material",
    )
    my_reactor.add_shape(pf_coil_4)

    pf_coil_4_case = PoloidalFieldCoilCase(
        casing_thickness=10,
        coil_height=30,
        coil_width=30,
        center_point=(800, 200),
        rotation_angle=rotation_angle,
        color=poloidal_magnet_case_color,
        stp_filename="pf_coil_case_4.stp",
        material_tag="pf_coil_material",
    )
    my_reactor.add_shape(pf_coil_4_case)

    return my_reactor


if __name__ == "__main__":
    my_reactor = make_reactor()
    my_reactor.export_stp(output_folder="ball_reactor")
    my_reactor.export_html(filename="ball_reactor/reactor.html")
    my_reactor.export_neutronics_description(filename="ball_reactor/manifest.json")
