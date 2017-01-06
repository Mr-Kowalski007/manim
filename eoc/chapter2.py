from helpers import *

from mobject.tex_mobject import TexMobject
from mobject import Mobject
from mobject.image_mobject import ImageMobject
from mobject.vectorized_mobject import *

from animation.animation import Animation
from animation.transform import *
from animation.simple_animations import *
from animation.playground import *
from topics.geometry import *
from topics.characters import *
from topics.functions import *
from topics.fractals import *
from topics.number_line import *
from topics.combinatorics import *
from topics.numerals import *
from topics.three_dimensions import *
from topics.objects import *
from scene import Scene
from scene.zoomed_scene import ZoomedScene
from camera import Camera
from mobject.svg_mobject import *
from mobject.tex_mobject import *

from eoc.chapter1 import OpeningQuote
from eoc.graph_scene import *


class Car(SVGMobject):
    CONFIG = {
        "file_name" : "Car", 
        "height" : 1,
        "color" : "#BBBBBB",
    }
    def __init__(self, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        self.scale_to_fit_height(self.height)
        self.set_stroke(color = WHITE, width = 0)
        self.set_fill(self.color, opacity = 1)

        randy = Randolph(mode = "happy")
        randy.scale_to_fit_height(0.6*self.get_height())
        randy.stretch(0.8, 0)
        randy.look(RIGHT)
        randy.move_to(self)
        randy.shift(0.07*self.height*(RIGHT+UP))
        self.add_to_back(randy)

        orientation_line = Line(self.get_left(), self.get_right())
        orientation_line.set_stroke(width = 0)
        self.add(orientation_line)
        self.orientation_line = orientation_line


        self.add_treds_to_tires()

    def move_to(self, point_or_mobject):
        vect = rotate_vector(
            UP+LEFT, self.orientation_line.get_angle()
        )
        self.next_to(point_or_mobject, vect, buff = 0)
        return self

    def get_front_line(self):
        return DashedLine(
            self.get_corner(UP+RIGHT), 
            self.get_corner(DOWN+RIGHT),
            color = YELLOW,
            dashed_segment_length = 0.05,
        )

    def add_treds_to_tires(self):
        for tire in self.get_tires():
            radius = tire.get_width()/2
            center = tire.get_center()
            tred = Line(
                0.9*radius*RIGHT, 1.4*radius*RIGHT,
                stroke_width = 2,
                color = BLACK
            )
            tred.rotate_in_place(np.pi/4)
            for theta in np.arange(0, 2*np.pi, np.pi/4):
                new_tred = tred.copy()
                new_tred.rotate(theta)
                new_tred.shift(center)
                tire.add(new_tred)
        return self

    def get_tires(self):
        return VGroup(self[1][1], self[1][3])

class MoveCar(ApplyMethod):
    def __init__(self, car, target_point, **kwargs):
        ApplyMethod.__init__(self, car.move_to, target_point, **kwargs)
        displacement = self.ending_mobject.get_right()-self.starting_mobject.get_right()
        distance = np.linalg.norm(displacement)
        tire_radius = car.get_tires()[0].get_width()/2
        self.total_tire_radians = -distance/tire_radius

    def update_mobject(self, alpha):
        ApplyMethod.update_mobject(self, alpha)
        if alpha == 0:
            return
        radians = alpha*self.total_tire_radians
        for tire in self.mobject.get_tires():
            tire.rotate_in_place(radians)

class IncrementNumber(Succession):
    CONFIG = {
        "start_num" : 0,
        "changes_per_second" : 1,
        "run_time" : 11,
    }
    def __init__(self, num_mob, **kwargs):
        digest_config(self, kwargs)
        n_iterations = int(self.run_time * self.changes_per_second)
        new_num_mobs = [
            TexMobject(str(num)).move_to(num_mob, LEFT)
            for num in range(self.start_num, self.start_num+n_iterations)
        ]
        transforms = [
            Transform(
                num_mob, new_num_mob, 
                run_time = 1.0/self.changes_per_second,
                rate_func = squish_rate_func(smooth, 0, 0.5)
            )
            for new_num_mob in new_num_mobs
        ]
        Succession.__init__(
            self, *transforms, **{
                "rate_func" : None,
                "run_time" : self.run_time,
            }
        )

class IncrementTest(Scene):
    def construct(self):
        num = TexMobject("0")
        num.shift(UP)
        self.play(IncrementNumber(num))
        self.dither()



############################

class Chapter2OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "So far as the theories of mathematics are about",
            "reality,", 
            "they are not",
            "certain;", 
            "so far as they are",
            "certain,", 
            "they are not about",
            "reality.",
        ],
        "highlighted_quote_terms" : {
            "reality," : BLUE,
            "certain;" : GREEN,
            "certain," : GREEN,
            "reality." : BLUE,
        },
        "author" : "Albert Einstein"
    }

class Introduction(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "What is a derivative?"
        )
        self.play(self.get_teacher().change_mode, "happy")
        self.dither()
        self.teacher_says(
            "It's actually a \\\\",
            "very subtle idea",
            target_mode = "well"
        )
        self.change_student_modes(None, "pondering", "thinking")
        self.dither()
        self.change_student_modes("erm")
        self.student_says(
            "Doesn't the derivative measure\\\\",
            "instantaneous rate of change", "?",
            student_index = 0,
        )
        self.dither()

        bubble = self.get_students()[0].bubble
        phrase = bubble.content[1]
        bubble.content.remove(phrase)
        self.play(
            phrase.center,
            phrase.scale, 1.5,
            phrase.to_edge, UP,
            FadeOut(bubble),
            FadeOut(bubble.content),
            *it.chain(*[
                [
                    pi.change_mode, mode,
                    pi.look_at, SPACE_HEIGHT*UP
                ]
                for pi, mode in zip(self.get_everyone(), [
                    "speaking", "pondering", "confused", "confused",
                ])
            ])
        )
        self.dither()
        change = VGroup(*phrase[-len("change"):])
        instantaneous = VGroup(*phrase[:len("instantaneous")])
        change_brace = Brace(change)
        change_description = change_brace.get_text(
            "Requires multiple \\\\ points in time"
        )
        instantaneous_brace = Brace(instantaneous)
        instantaneous_description = instantaneous_brace.get_text(
            "One point \\\\ in time"
        )
        clock = Clock()
        clock.next_to(change_description, DOWN)
        def get_clock_anim(run_time = 3):
            return ClockPassesTime(
                clock,
                hours_passed = 0.4*run_time,
                run_time = run_time,
            )
        self.play(FadeIn(clock))
        self.play(
            change.gradient_highlight, BLUE, YELLOW,
            GrowFromCenter(change_brace),
            Write(change_description),
            get_clock_anim()
        )
        self.play(get_clock_anim(1))
        stopped_clock = clock.copy()
        stopped_clock.next_to(instantaneous_description, DOWN)
        self.play(
            instantaneous.highlight, BLUE,
            GrowFromCenter(instantaneous_brace),
            Transform(change_description.copy(), instantaneous_description),
            clock.copy().next_to, instantaneous_description, DOWN,
            get_clock_anim(3)
        )
        self.play(get_clock_anim(6))

class FathersOfCalculus(Scene):
    CONFIG = {
        "names" : [
            "Barrow",
            "Newton", 
            "Leibniz",
            "Cauchy",
            "Weierstrass",
        ],
        "picture_height" : 2.5,
    }
    def construct(self):
        title = TextMobject("(A few) Fathers of Calculus")
        title.to_edge(UP)
        self.add(title)

        men = Mobject()
        for name in self.names:
            image = ImageMobject(name, invert = False)
            image.scale_to_fit_height(self.picture_height)
            title = TextMobject(name)
            title.scale(0.8)
            title.next_to(image, DOWN)
            image.add(title)
            men.add(image)
        men.arrange_submobjects(RIGHT, aligned_edge = UP)
        men.shift(DOWN)

        discover_brace = Brace(Mobject(*men[:3]), UP)
        discover = discover_brace.get_text("Discovered it")
        VGroup(discover_brace, discover).highlight(BLUE)
        rigor_brace = Brace(Mobject(*men[3:]), UP)
        rigor = rigor_brace.get_text("Made it rigorous")
        rigor.shift(0.1*DOWN)
        VGroup(rigor_brace, rigor).highlight(YELLOW)


        for man in men:
            self.play(FadeIn(man))
        self.play(
            GrowFromCenter(discover_brace),
            Write(discover, run_time = 1)
        )
        self.play(
            GrowFromCenter(rigor_brace),
            Write(rigor, run_time = 1)
        )
        self.dither()

class IntroduceCar(Scene):
    CONFIG = {
        "should_transition_to_graph" : True,
        "show_distance" : True,
    }
    def construct(self):
        point_A = DOWN+4*LEFT
        point_B = DOWN+5*RIGHT
        A = Dot(point_A)
        B = Dot(point_B)
        line = Line(point_A, point_B)
        VGroup(A, B, line).highlight(WHITE)        
        for dot, tex in (A, "A"), (B, "B"):
            label = TexMobject(tex).next_to(dot, DOWN)
            dot.add(label)

        car = Car()
        self.car = car #For introduce_added_mobjects use in subclasses
        car.move_to(point_A)
        front_line = car.get_front_line()

        time_label = TextMobject("Time (in seconds):", "0")
        time_label.shift(2*UP)

        distance_brace = Brace(line, UP)
        # distance_brace.set_fill(opacity = 0.5)
        distance = distance_brace.get_text("100m")

        self.add(A, B, line, car, time_label)
        self.play(ShowCreation(front_line))
        self.play(FadeOut(front_line))
        self.introduce_added_mobjects()
        self.play(
            MoveCar(car, point_B, run_time = 10),
            IncrementNumber(time_label[1], run_time = 11),
            *self.get_added_movement_anims()
        )
        front_line = car.get_front_line()
        self.play(ShowCreation(front_line))
        self.play(FadeOut(front_line))

        if self.show_distance:
            self.play(
                GrowFromCenter(distance_brace),
                Write(distance)
            )
            self.dither()

        if self.should_transition_to_graph:
            self.play(
                car.move_to, point_A,
                FadeOut(time_label),
                FadeOut(distance_brace),
                FadeOut(distance),
            )
            graph_scene = GraphCarTrajectory(skip_animations = True)
            origin = graph_scene.graph_origin
            top = graph_scene.coords_to_point(0, 100)
            new_length = np.linalg.norm(top-origin)
            new_point_B = point_A + new_length*RIGHT
            car_line_group = VGroup(car, A, B, line)
            for mob in car_line_group:
                mob.generate_target()
            car_line_group.target = VGroup(*[
                m.target for m in car_line_group
            ])
            B = car_line_group[2]
            B.target.shift(new_point_B - point_B)
            line.target.put_start_and_end_on(
                point_A, new_point_B
            )

            car_line_group.target.rotate(np.pi/2, about_point = point_A)
            car_line_group.target.shift(graph_scene.graph_origin - point_A)
            self.play(MoveToTarget(car_line_group, path_arc = np.pi/2))
            self.dither()

    def introduce_added_mobjects(self):
        pass

    def get_added_movement_anims(self):
        return []

class GraphCarTrajectory(GraphScene):
    CONFIG = {
        "x_min" : 0,
        "x_max" : 10.01,
        "x_labeled_nums" : range(1, 11),
        "x_axis_label" : "Time (seconds)",
        "y_min" : 0,
        "y_max" : 110,
        "y_tick_frequency" : 10,
        "y_labeled_nums" : range(10, 110, 10),
        "y_axis_label" : "Distance traveled \\\\ (meters)",
        "graph_origin" : 2.5*DOWN + 5*LEFT,
    }
    def construct(self):
        self.setup_axes(animate = False)
        graph = self.graph_function(lambda t : 100*smooth(t/10.))
        origin = self.coords_to_point(0, 0)

        self.introduce_graph(graph, origin)
        self.comment_on_slope(graph, origin)
        self.show_velocity_graph()
        self.ask_critically_about_velocity()

    def introduce_graph(self, graph, origin):
        h_line, v_line = [
            Line(origin, origin, color = color, stroke_width = 2)
            for color in MAROON_B, YELLOW
        ]
        def h_update(h_line, proportion = 1):
            end = graph.point_from_proportion(proportion)
            t_axis_point = end[0]*RIGHT + origin[1]*UP
            h_line.put_start_and_end_on(t_axis_point, end)
        def v_update(v_line, proportion = 1):
            end = graph.point_from_proportion(proportion)
            d_axis_point = origin[0]*RIGHT + end[1]*UP
            v_line.put_start_and_end_on(d_axis_point, end)

        car = Car()
        car.rotate(np.pi/2)
        car.move_to(origin)
        self.add(car)
        self.play(
            ShowCreation(
                graph,
                rate_func = None,
            ),
            MoveCar(
                car, self.coords_to_point(0, 100),
            ),
            UpdateFromFunc(h_line, h_update),
            UpdateFromFunc(v_line, v_update),
            run_time = 10,
        )
        self.dither()
        self.play(*map(FadeOut, [h_line, v_line, car]))

        #Show example vertical distance
        h_update(h_line, 0.6)
        t_dot = Dot(h_line.get_start(), color = h_line.get_color())
        t_dot.save_state()
        t_dot.move_to(self.x_axis_label_mob)
        t_dot.set_fill(opacity = 0)
        dashed_h = DashedLine(*h_line.get_start_and_end())
        dashed_h.highlight(h_line.get_color())
        brace = Brace(dashed_h, RIGHT)
        brace_text = brace.get_text("Distance traveled")
        self.play(t_dot.restore)
        self.dither()
        self.play(ShowCreation(dashed_h))
        self.play(
            GrowFromCenter(brace),
            Write(brace_text)
        )
        self.dither(2)
        self.play(*map(FadeOut, [t_dot, dashed_h, brace, brace_text]))

        #Name graph
        s_of_t = TexMobject("s(t)")
        s_of_t.next_to(
            graph.point_from_proportion(1), 
            DOWN+RIGHT,
            buff = SMALL_BUFF
        )
        s = s_of_t[0]
        d = TexMobject("d")
        d.move_to(s, DOWN)
        d.highlight(YELLOW)

        self.play(Write(s_of_t))
        self.dither()
        s.save_state()
        self.play(Transform(s, d))
        self.dither()
        self.play(s.restore)

    def comment_on_slope(self, graph, origin):
        delta_t = 1
        curr_time = 0
        ghost_line = Line(
            origin, 
            self.coords_to_point(delta_t, self.y_max)
        )
        rect = Rectangle().replace(ghost_line, stretch = True)
        rect.set_stroke(width = 0)
        rect.set_fill(BLUE, opacity = 0.3)

        change_lines = self.get_change_lines(curr_time, delta_t)
        self.play(FadeIn(rect))
        self.dither()
        self.play(Write(change_lines))
        self.dither()
        for x in range(1, 10):
            curr_time = x
            new_change_lines = self.get_change_lines(curr_time, delta_t)
            self.play(
                rect.move_to, self.coords_to_point(curr_time, 0), DOWN+LEFT,
                Transform(change_lines, new_change_lines)
            )
            if curr_time == 5:
                text = change_lines[-1].get_text(
                    "$\\frac{\\text{meters}}{\\text{second}}$"
                )
                self.play(Write(text))
                self.dither()
                self.play(FadeOut(text))
            else:
                self.dither()
        self.play(*map(FadeOut, [rect, change_lines]))
        self.rect = rect

    def get_change_lines(self, curr_time, delta_t = 1):
        p1 = self.input_to_graph_point(curr_time)
        p2 = self.input_to_graph_point(curr_time+delta_t)
        interim_point = p2[0]*RIGHT + p1[1]*UP
        delta_t_line = Line(p1, interim_point, color = YELLOW)
        delta_s_line = Line(interim_point, p2, color = MAROON_B)
        brace = Brace(delta_s_line, RIGHT, buff = SMALL_BUFF)
        return VGroup(delta_t_line, delta_s_line, brace)

    def show_velocity_graph(self):
        velocity_graph = self.get_derivative_graph()

        self.play(ShowCreation(velocity_graph))
        def get_velocity_label(v_graph):
            result = self.label_graph(
                v_graph,
                label = "v(t)",
                direction = UP+RIGHT,
                proportion = 0.5,
                buff = SMALL_BUFF,
                animate = False,
            )
            self.remove(result)
            return result
        label = get_velocity_label(velocity_graph)
        self.play(Write(label))
        self.dither()
        self.rect.move_to(self.coords_to_point(0, 0), DOWN+LEFT)
        self.play(FadeIn(self.rect))
        self.dither()
        for time, show_slope in (4.5, True), (9, False):
            self.play(
                self.rect.move_to, self.coords_to_point(time, 0), DOWN+LEFT
            )
            if show_slope:
                change_lines = self.get_change_lines(time)
                self.play(FadeIn(change_lines))
                self.dither()
                self.play(FadeOut(change_lines))
            else:
                self.dither()
        self.play(FadeOut(self.rect))

        #Change distance and velocity graphs
        self.graph.save_state()
        velocity_graph.save_state()
        label.save_state()
        def shallow_slope(t):
            return 100*smooth(t/10., inflection = 4)
        def steep_slope(t):
            return 100*smooth(t/10., inflection = 25)
        def double_smooth_graph_function(t):
            if t < 5:
                return 50*smooth(t/5.)
            else:
                return 50*(1+smooth((t-5)/5.))
        graph_funcs = [
            shallow_slope,
            steep_slope,
            double_smooth_graph_function,
        ]
        for graph_func in graph_funcs:
            new_graph = self.graph_function(
                graph_func,
                is_main_graph = False
            )
            self.remove(new_graph)
            new_velocity_graph = self.get_derivative_graph(graph = new_graph)
            new_velocity_label = get_velocity_label(new_velocity_graph)

            self.play(Transform(self.graph, new_graph))
            self.play(
                Transform(velocity_graph, new_velocity_graph),
                Transform(label, new_velocity_label),
            )
            self.dither(2)
        self.play(self.graph.restore)
        self.play(
            velocity_graph.restore,
            label.restore,
        )
        self.dither(2)

    def ask_critically_about_velocity(self):
        morty = Mortimer().flip()
        morty.to_corner(DOWN+LEFT)
        self.play(PiCreatureSays(morty,
            "Think critically about \\\\",
            "what velocity means."
        ))
        self.play(Blink(morty))
        self.dither()

class ShowSpeedometer(IntroduceCar):
    CONFIG = {
        "num_ticks" : 8,
        "tick_length" : 0.2,
        "needle_width" : 0.1,
        "needle_height" : 0.8,
        "should_transition_to_graph" : False,
        "show_distance" : False,
    }
    def setup(self):
        start_angle = -np.pi/6
        end_angle = 7*np.pi/6
        speedomoeter = Arc(
            start_angle = start_angle,
            angle = end_angle-start_angle
        )
        tick_angle_range = np.linspace(end_angle, start_angle, self.num_ticks)
        for index, angle in enumerate(tick_angle_range):
            vect = rotate_vector(RIGHT, angle)
            tick = Line((1-self.tick_length)*vect, vect)
            label = TexMobject(str(10*index))
            label.scale_to_fit_height(self.tick_length)
            label.shift((1+self.tick_length)*vect)
            speedomoeter.add(tick, label)

        needle = Polygon(
            LEFT, UP, RIGHT,
            stroke_width = 0,
            fill_opacity = 1,
            fill_color = YELLOW
        )
        needle.stretch_to_fit_width(self.needle_width)
        needle.stretch_to_fit_height(self.needle_height)
        needle.rotate(end_angle-np.pi/2)
        speedomoeter.add(needle)
        speedomoeter.needle = needle

        speedomoeter.center_offset = speedomoeter.get_center()

        speedomoeter_title = TextMobject("Speedometer")
        speedomoeter_title.to_corner(UP+LEFT)
        speedomoeter.next_to(speedomoeter_title, DOWN)

        self.speedomoeter = speedomoeter
        self.speedomoeter_title = speedomoeter_title

    def introduce_added_mobjects(self):
        speedomoeter = self.speedomoeter
        speedomoeter_title = self.speedomoeter_title

        speedomoeter.save_state()
        speedomoeter.rotate(-np.pi/2, UP)
        speedomoeter.scale_to_fit_height(self.car.get_height()/4)
        speedomoeter.move_to(self.car)
        speedomoeter.shift((self.car.get_width()/4)*RIGHT)

        self.play(speedomoeter.restore, run_time = 2)
        self.play(Write(speedomoeter_title, run_time = 1))

    def get_added_movement_anims(self):
        needle = self.speedomoeter.needle
        center = self.speedomoeter.get_center() - self.speedomoeter.center_offset
        return [
            Rotating(
                needle, 
                about_point = center,
                radians = -np.pi/2,
                run_time = 10,
                rate_func = there_and_back
            )
        ]

    # def construct(self):
    #     self.add(self.speedomoeter)
    #     self.play(*self.get_added_movement_anims())

class VelocityInAMomentMakesNoSense(Scene):
    def construct(self):
        randy = Randolph()
        randy.next_to(ORIGIN, DOWN+LEFT)
        words = TextMobject("Velocity in \\\\ a moment")
        words.next_to(randy, UP+RIGHT)
        randy.look_at(words)
        q_marks = TextMobject("???")
        q_marks.next_to(randy, UP)

        self.play(
            randy.change_mode, "confused",
            Write(words)
        )
        self.play(Blink(randy))
        self.play(Write(q_marks))
        self.play(Blink(randy))
        self.dither()

class SnapshotOfACar(Scene):
    def construct(self):
        car = Car()
        car.scale(1.5)
        car.move_to(3*LEFT+DOWN)
        flash_box = Rectangle(
            width = 2*SPACE_WIDTH,
            height = 2*SPACE_HEIGHT,
            stroke_width = 0,
            fill_color = WHITE,
            fill_opacity = 1,
        )
        speed_lines = VGroup(*[
            Line(point, point+0.5*LEFT)
            for point in [
                0.5*UP+0.25*RIGHT,
                ORIGIN, 
                0.5*DOWN+0.25*RIGHT
            ]
        ])
        question = TextMobject("""
            How fast is
            this car going?
        """)

        self.play(MoveCar(
            car, RIGHT+DOWN, 
            run_time = 2,
            rate_func = rush_into
        ))
        car.get_tires().highlight(GREY)
        speed_lines.next_to(car, LEFT)
        self.add(speed_lines)
        self.play(
            flash_box.set_fill, None, 0,
            rate_func = rush_from
        )
        question.next_to(car, UP, buff = LARGE_BUFF)
        self.play(Write(question, run_time = 2))
        self.dither(2)

class CompareTwoTimes(Scene):
    CONFIG = {
        "start_distance" : 30,
        "start_time" : 4,
        "end_distance" : 50,
        "end_time" : 5,
        "distance_color" : YELLOW,
        "time_color" : BLUE,
    }
    def construct(self):
        self.introduce_states()
        self.show_equation()
        self.fade_all_but_one_moment()

    def introduce_states(self):
        state1 = self.get_car_state(self.start_distance, self.start_time)
        state2 = self.get_car_state(self.end_distance, self.end_time)

        state1.to_corner(UP+LEFT)
        state2.to_corner(DOWN+LEFT)

        dividers = VGroup(
            Line(SPACE_WIDTH*LEFT, RIGHT),
            Line(RIGHT+SPACE_HEIGHT*UP, RIGHT+SPACE_HEIGHT*DOWN),
        )
        dividers.highlight(GREY)

        self.add(dividers, state1)
        self.dither()
        copied_state = state1.copy()
        self.play(copied_state.move_to, state2)
        self.play(Transform(copied_state, state2))
        self.dither(2)
        self.keeper = state1

    def show_equation(self):
        velocity = TextMobject("Velocity")
        change_over_change = TexMobject(
            "\\frac{\\text{Change in distance}}{\\text{Change in time}}"
        )
        formula = TexMobject(
            "\\frac{(%d - %d) \\text{ meters}}{(%d - %d) \\text{ seconds}}"%(
                self.end_distance, self.start_distance,
                self.end_time, self.start_time,
            )
        )
        VGroup(*list(formula[1:3]) + list(formula[4:6])).highlight(self.distance_color)
        VGroup(formula[-11], formula[-9]).highlight(self.time_color)

        down_arrow1 = TexMobject("\\Downarrow")
        down_arrow2 = TexMobject("\\Downarrow")
        group = VGroup(
            velocity, down_arrow1, 
            change_over_change, down_arrow2,
            formula,
        )
        group.arrange_submobjects(DOWN)
        group.to_corner(UP+RIGHT)

        self.play(FadeIn(
            group, submobject_mode = "lagged_start",
            run_time = 3
        ))
        self.dither(3)

    def fade_all_but_one_moment(self):
        anims = [
            ApplyMethod(mob.fade, 0.5)
            for mob in self.get_mobjects()
        ]
        anims.append(Animation(self.keeper.copy()))
        self.play(*anims)
        self.dither()

    def get_car_state(self, distance, time):
        line = Line(3*LEFT, 3*RIGHT)
        dots = map(Dot, line.get_start_and_end())
        line.add(*dots)
        car = Car()
        car.move_to(line.get_start())
        car.shift((distance/10)*RIGHT)
        front_line = car.get_front_line()

        brace = Brace(VGroup(dots[0], front_line), DOWN)
        distance_label = brace.get_text(
            str(distance), " meters"
        )
        distance_label.highlight_by_tex(str(distance), self.distance_color)
        brace.add(distance_label)
        time_label = TextMobject(
            "Time:", str(time), "seconds"
        )
        time_label.highlight_by_tex(str(time), self.time_color)
        time_label.next_to(
            VGroup(line, car), UP,
            aligned_edge = LEFT
        )

        return VGroup(line, car, front_line, brace, time_label)

class VelocityAtIndividualPointsVsPairs(GraphCarTrajectory):
    CONFIG = {
        "start_time" : 6,
        "end_time" : 3,
        "dt" : 1,
    }
    def construct(self):
        self.setup_axes(animate = False)
        distance_graph = self.graph_function(lambda t : 100*smooth(t/10.))
        distance_label = self.label_graph(
            distance_graph,
            label = "s(t)",
            proportion = 1,
            direction = DOWN+RIGHT,
            buff = SMALL_BUFF
        )
        velocity_graph = self.get_derivative_graph()
        self.play(ShowCreation(velocity_graph))
        velocity_label = self.label_graph(
            velocity_graph, 
            label = "v(t)",
            proportion = 0.5, 
            direction = UP+RIGHT,
            buff = MED_BUFF
        )
        velocity_graph.add(velocity_label)

        self.show_individual_times_to_velocity(velocity_graph)
        self.play(velocity_graph.fade, 0.6)
        self.show_two_times_on_distance()
        self.show_confused_pi_creature()

    def show_individual_times_to_velocity(self, velocity_graph):
        start_time = self.start_time
        end_time = self.end_time
        line = self.get_vertical_line_to_graph(start_time, velocity_graph)
        def line_update(line, alpha):
            time = interpolate(start_time, end_time, alpha)
            line.put_start_and_end_on(
                self.coords_to_point(time, 0),
                self.input_to_graph_point(time, graph = velocity_graph)
            )

        self.play(ShowCreation(line))
        self.dither()
        self.play(UpdateFromAlphaFunc(
            line, line_update,
            run_time = 4,
            rate_func = there_and_back
        ))
        self.dither()
        velocity_graph.add(line)

    def show_two_times_on_distance(self):
        line1 = self.get_vertical_line_to_graph(self.start_time)
        line2 = self.get_vertical_line_to_graph(self.start_time+self.dt)
        p1 = line1.get_end()
        p2 = line2.get_end()
        interim_point = p2[0]*RIGHT+p1[1]*UP
        dt_line = Line(p1, interim_point, color = MAROON_B)
        ds_line = Line(interim_point, p2, color = YELLOW)
        dt_brace = Brace(dt_line, DOWN, buff = SMALL_BUFF)
        ds_brace = Brace(ds_line, RIGHT, buff = SMALL_BUFF)
        dt_text = dt_brace.get_text("Change in time", buff = SMALL_BUFF)
        ds_text = ds_brace.get_text("Change in distance", buff = SMALL_BUFF)

        self.play(ShowCreation(VGroup(line1, line2)))
        for line, brace, text in (dt_line, dt_brace, dt_text), (ds_line, ds_brace, ds_text):
            brace.highlight(line.get_color())
            text.highlight(line.get_color())
            text.add_background_rectangle()
            self.play(
                ShowCreation(line),
                GrowFromCenter(brace),
                Write(text)
            )
            self.dither()

    def show_confused_pi_creature(self):
        randy = Randolph()
        randy.to_corner(DOWN+LEFT)
        randy.shift(2*RIGHT)

        self.play(randy.change_mode, "confused")
        self.play(Blink(randy))
        self.dither(2)
        self.play(Blink(randy))
        self.play(randy.change_mode, "erm")
        self.dither()
        self.play(Blink(randy))
        self.dither(2)





































