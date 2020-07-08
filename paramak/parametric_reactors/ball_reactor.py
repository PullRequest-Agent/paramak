from paramak import Reactor
import paramak

class BallReactor(Reactor):
    """Creates geometry for a simple ball reactor including a plasma,
    cylindical center column shielding, square toroidal field coils

    :param major_radius: 
    :type height: float

    :return: a shape object that has generic functionality
    :rtype: paramak shape object
    """

    def __init__(
        self,
        major_radius,
        minor_radius,
        offset_from_plasma,
        blanket_thickness,
        center_column_shield_inner_radius,
        center_column_shield_outer_radius,
        number_of_tf_coils,
        rotation_angle = 360
    ):

        super().__init__()

        self.major_radius = major_radius
        self.minor_radius = minor_radius
        self.offset_from_plasma = offset_from_plasma
        self.blanket_thickness = blanket_thickness
        self.rotation_angle = rotation_angle
        self.center_column_shield_inner_radius = center_column_shield_inner_radius
        self.center_column_shield_outer_radius = center_column_shield_outer_radius
        self.number_of_tf_coils = number_of_tf_coils

        self.create_components()


    def create_components(self):

        plasma = paramak.Plasma(major_radius=self.major_radius,
                                minor_radius=self.minor_radius,
                                rotation_angle=self.rotation_angle)
        plasma.create_solid()

        self.add_shape_or_component(plasma)

        blanket = paramak.BlanketConstantThicknessArcV(
            inner_mid_point=(plasma.minor_radius + 
                             plasma.major_radius + 
                             self.offset_from_plasma,
                             0),
            inner_upper_point=(plasma.x_point,
                               plasma.z_point+self.offset_from_plasma),
            inner_lower_point=(plasma.x_point,
                               -(plasma.z_point+self.offset_from_plasma)),
            thickness=self.blanket_thickness,
            rotation_angle=self.rotation_angle
        )

        self.add_shape_or_component(blanket)

        # The height of this center column is calculated using CadQuery commands
        center_column_shield = paramak.CenterColumnShieldCylinder(
            height=2*(plasma.z_point + self.offset_from_plasma + self.blanket_thickness),
            inner_radius=self.center_column_shield_inner_radius,
            outer_radius=self.center_column_shield_outer_radius,
            rotation_angle=self.rotation_angle,
            # color=centre_column_color,
            stp_filename="center_column_shield.stp",
            material_tag="center_column_material",
        )
        self.add_shape_or_component(center_column_shield)

        inboard_tf_coils = paramak.InnerTfCoilsCircular(
            height=2*(plasma.z_point + self.offset_from_plasma + self.blanket_thickness),
            outer_radius = self.center_column_shield_inner_radius,
            inner_radius = 30,
            number_of_coils = self.number_of_tf_coils,
            gap_size=10,
            stp_filename="inboard_tf_coils.stp",
            material_tag="inboard_tf_coils_material",
        )

        self.add_shape_or_component(inboard_tf_coils)