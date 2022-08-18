from manim import *
from cosserat_rod import *
from copy import copy
class RodPlot(Scene):
    def construct(self):
        ax = Axes(
            x_range=[-0.5, 0.5, 0.05],
            y_range=[-1, 5, 1],
            #x_length=9,
            #y_length=6,
            #x_axis_config={"numbers_to_include": np.arange(0, 40, 5)},
            #y_axis_config={"numbers_to_include": np.arange(-5, 34, 5)},
            tips=False,
        )
        labels = ax.get_axis_labels(
            x_label=Tex("x"), y_label=Tex("y")
        )

        rod = CosseratRod()
        # Arbitrary base frame assignment
        p0 = np.array([[0, 0, 0]])
        R0 = np.eye(3)
        rod.set_initial_conditions(p0, R0)

        for i, f in enumerate(np.linspace(0,-1,10)):
            wrench = np.array([f/10.,0.,f,0,0,0])
            states = rod.push_end(wrench)
            x_vals , y_vals = states[:,1], states[:,2]
            if i > 0:
                old_graph = copy(graph)
            graph = ax.plot_line_graph(x_values=x_vals, y_values=y_vals)
            if i == 0:
                self.play(Create(ax), Create(graph))#, Write(graph_label))
                self.wait()
            else:
                self.play(ReplacementTransform(old_graph, graph))
                self.wait()

class LineRodPlot(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-3, 3],
            y_range=[-5, 5],
            axis_config={"color": BLUE},
        )

        # Create Graph
        graph = axes.get_graph(lambda x: x**2, color=WHITE)
        graph_label = axes.get_graph_label(graph, label='x^{2}')

        graph2 = axes.get_graph(lambda x: x**3, color=WHITE)
        graph_label2 = axes.get_graph_label(graph2, label='x^{3}')

        # Display graph
        self.play(Create(axes), Create(graph), Write(graph_label))
        self.wait(1)
        self.play(Transform(graph, graph2), Transform(graph_label, graph_label2))
        self.wait(1)



class LineRodPlot3d(ThreeDScene):
    def construct(self):
        #self.camera.background_color = WHITE
        ax = ThreeDAxes(
            x_length = 1.0,
            y_length = 1.0,
            z_length = 1.0,
                        axis_config={
                            'tick_size': 0.001,
                            'tip_width': 0.01,
                            'tip_height': 0.01,
                            'include_tip': False,
                            'color' : WHITE,
                            'stroke_width' : 0.1,
                            'include_numbers' : False,
                            'decimal_number_config' : {
                                'num_decimal_places' : 0,
                                'include_sign' : True,
                                'color' : WHITE,

                }})

        self.set_camera_orientation(phi=2*PI/5, theta=-PI/4 , zoom=15)
        self.add(ax)

        z_label = ax.get_z_axis_label("z").set_color(WHITE)
        y_label = ax.get_y_axis_label("y").set_color(WHITE)
        x_label = ax.get_x_axis_label("x").set_color(WHITE)
        grid_labels = VGroup(x_label, y_label, z_label)

        self.add(grid_labels)

        rod = CurvedCosseratRod()
        # Arbitrary base frame assignment
        p0 = np.array([[0, 0, 0]])
        R0 = np.eye(3)
        rod.set_initial_conditions(p0, R0)
        rod.params['L'] = 1.5
        kappa = np.deg2rad(80) / rod.params['L']
        print(kappa)
        rod.inital_conditions['kappa_0'] = np.array([0, kappa, 0])

        rod.params['kappa'] = np.array([0., kappa, 0])

        for i, f in enumerate(np.linspace(0, 0.2, 10)):
            wrench = np.array([0 , -f, 0, 0, 0, 0])
            states = rod.push_end(wrench)
            x_vals, y_vals, z_vals = states[:, 0], states[:, 1], states[:, 2]
            if i > 0:
                old_graph = copy(graph)
            graph = ax.plot_line_graph(x_values=x_vals, y_values=y_vals, z_values=z_vals, vertex_dot_radius=0.00001)
            if i == 0:
                self.play(Create(ax), Create(graph))  # , Write(graph_label))
                self.wait()
            else:
                self.play(ReplacementTransform(old_graph, graph))
                self.wait()


class MoveSingleRod(ThreeDScene):
    def construct(self):
        #self.camera.background_color = WHITE
        ax = ThreeDAxes(
            x_length = 1.0,
            y_length = 1.0,
            z_length = 1.0,
                        axis_config={
                            'tick_size': 0.001,
                            'tip_width': 0.01,
                            'tip_height': 0.01,
                            'include_tip': False,
                            'color' : WHITE,
                            'stroke_width' : 0.1,
                            'include_numbers' : False,
                            'decimal_number_config' : {
                                'num_decimal_places' : 0,
                                'include_sign' : True,
                                'color' : WHITE,

                }})

        self.set_camera_orientation(phi=2*PI/5, theta=-PI/4 , zoom=15)
        self.add(ax)

        z_label = ax.get_z_axis_label("z").set_color(WHITE)
        y_label = ax.get_y_axis_label("y").set_color(WHITE)
        x_label = ax.get_x_axis_label("x").set_color(WHITE)
        grid_labels = VGroup(x_label, y_label, z_label)

        self.add(grid_labels)

        rod = CurvedCosseratRod()
        # Arbitrary base frame assignment
        p0 = np.array([[0, 0, 0]])
        R0 = np.eye(3)

        rod.set_initial_conditions(p0, R0)
        rod.params['L'] = 1.

        kappa = np.deg2rad(90) / rod.params['L']
        rod.inital_conditions['kappa_0'] = np.array([0, 0, 0])

        rod.params['kappa'] = kappa
        rod.params['straight_length'] = 0.9

        states = rod.push_end(np.array([0, 0, 0, 0, 0, 0]))
        Rn0 = np.reshape(states[-1][3:12], (3, 3))
        pn0 = np.asarray([states[-1][:3]])

        for i, p in enumerate(np.linspace(0.1, 1, 20)):
            f = 3 * p
            r = np.pi * p
            R0 = np.array([[np.cos(r), -np.sin(r), 0],
                           [np.sin(r), np.cos(r), 0],
                           [0, 0, 1]])
            rod.set_initial_conditions(p0, R0)
            rod.inital_conditions['kappa_0'] = np.array([0, 0, 0])
            states = rod.push_end(np.array([0, 0, 0, 0, 0, 0]))
            Rn0 = np.reshape(states[-1][3:12], (3, 3))
            wrench = np.array([0, 0, -f, 0, 0, 0])
            wrench[:3] = Rn0 @ wrench[:3]
            wrench[3:] = Rn0 @ wrench[3:]
            states = rod.push_end(wrench)

            x_vals, y_vals, z_vals = states[:, 0], states[:, 1], states[:, 2]
            if i > 0:
                old_graph = copy(graph)
            graph = ax.plot_line_graph(x_values=x_vals, y_values=y_vals, z_values=z_vals, vertex_dot_radius=0.00001)
            if i == 0:
                self.play(Create(ax), Create(graph))  # , Write(graph_label))
                #self.wait()
            else:
                self.play(ReplacementTransform(old_graph, graph))
                #self.wait()