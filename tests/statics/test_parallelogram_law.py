import pytest

from qnty.problems.parallelogram_law import ParallelogramLawProblem
from qnty.spatial.coordinate_system import CoordinateSystem
from qnty.spatial import ForceVector

# Problem definitions - single source of truth
FORCE_VECTOR_PROBLEMS = {
    "problem_2_1": {
        "name": "Problem 2-1",
        "description": """
        If theta=60 degrees and F=450 N, determine the magnitude of the resultant force
        and its direction, measured counterclockwise from the positive x axis.
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=450, unit="N",
                angle=60, wrt="+x",
                name="F_1", description="Force 1"
            ),
            "F_2": ForceVector(
                magnitude=700, unit="N",
                angle=15, wrt="-x",
                name="F_2", description="Force 2"
            ),
            "F_R": ForceVector.unknown(
                "F_R", is_resultant=True
            ),
        },
        "expected": {
            "F_1": {
                "magnitude": 450, "unit": "N",
                "angle": 60, "wrt": "+x"
            },
            "F_2": {
                "magnitude": 700, "unit": "N",
                "angle": 15, "wrt": "-x"
            },
            "F_R": {
                "magnitude": 497.014, "unit": "N",
                "angle": 155.192, "wrt": "+x"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_2": {
        "name": "Problem 2-2",
        "description": """
        If the magnitude of the resultant force is to be 500 N, directed along the positive y axis,
        determine the magnitude of force F and its direction theta.
        """,
        "forces": {
            "F_1": ForceVector.unknown("F_1"),
            "F_2": ForceVector(
                magnitude=700, unit="N",
                angle=15, wrt="-x", 
                name="F_2", description="Force 2"
            ),
            "F_R": ForceVector(
                magnitude=500, unit="N",
                angle=90, wrt="+x",
                name="F_R", description="Resultant Force",is_resultant=True
            ),
        },
        "expected": {
            "F_1": {
                "magnitude": 959.778, "unit": "N",
                "angle": 45.212, "wrt": "+x"
            },
            "F_2": {
                "magnitude": 700, "unit": "N",
                "angle": 15, "wrt": "-x"
            },
            "F_R": {
                "magnitude": 500, "unit": "N",
                "angle": 90, "wrt": "+x"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_3": {
        "name": "Problem 2-3",
        "description": """
        Determine the magnitude of the resultant force F_R = F_1 + F_2 and its direction,
        measured counterclockwise from the positive x axis.
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=250, unit="lbf",
                angle=60, wrt="+x",
                name="F_1", description="Force 1"
            ),
            "F_2": ForceVector(
                magnitude=375, unit="lbf",
                angle=315, wrt="+x",
                name="F_2", description="Force 2"
            ),
            "F_R": ForceVector.unknown("F_R", is_resultant=True),
        },
        "expected": {
            "F_1": {"magnitude": 250, "angle": 60, "unit": "lbf", "wrt": "+x"},
            "F_2": {"magnitude": 375, "angle": 315, "unit": "lbf", "wrt": "+x"},
            "F_R": {"magnitude": 393.188, "angle": 352.891, "unit": "lbf", "wrt": "+x"},
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_4": {
        "name": "Problem 2-4",
        "description": """
        The vertical force F acts downward at A on the two-membered frame.
        Determine the magnitudes of the two components of F directed along the axes of AB and AC.
        Set F = 500 N.
        """,
        "forces": {
            "F_AB": ForceVector.unknown("F_AB", angle=225, unit="N"),  # Known angle, unknown magnitude
            "F_AC": ForceVector.unknown("F_AC", angle=330, unit="N"),  # Known angle, unknown magnitude
            "F": ForceVector(
                magnitude=500, angle=270, unit="N",
                name="F", description="Resultant (vertical downward)",
                is_resultant=True
            ),
        },
        "expected": {
            "F_AB": {"magnitude": 448, "angle": 225, "unit": "N", "wrt": "+x"},
            "F_AC": {"magnitude": 366, "angle": 330, "unit": "N", "wrt": "+x"},
            "F": {"magnitude": 500, "angle": 270, "unit": "N", "wrt": "+x"},
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_5": {
        "name": "Problem 2-5",
        "description": """
        Solve Prob. 2-4 with F = 350 lb.
        """,
        "forces": {
            "F_AB": ForceVector.unknown("F_AB", angle=225, unit="lbf"),  # Known angle, unknown magnitude
            "F_AC": ForceVector.unknown("F_AC", angle=330, unit="lbf"),  # Known angle, unknown magnitude
            "F": ForceVector(
                magnitude=350, angle=270, unit="lbf",
                name="F", description="Resultant (vertical downward)",
                is_resultant=True
            ),
        },
        "expected": {
            "F_AB": {"magnitude": 314, "angle": 225, "unit": "lbf", "wrt": "+x"},
            "F_AC": {"magnitude": 256, "angle": 330, "unit": "lbf", "wrt": "+x"},
            "F": {"magnitude": 350, "angle": 270, "unit": "lbf", "wrt": "+x"},
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_6": {
        "name": "Problem 2-6",
        "description": """
        Determine the magnitude of the resultant force F_R = F_1 + F_2 and its direction,
        measured clockwise from the positive u axis.
        Note: u-v coordinate system with 75° between axes (u at 0°, v at 75°).
        """,
        "coordinate_system": CoordinateSystem.from_angle_between(
            "x", "y", axis1_angle=0, angle_between=75
        ),
        "forces": lambda coord_sys: {
            "F_1": ForceVector(
                magnitude=4000, angle=-30, wrt="+y", unit="N",
                name="F_1", description="Force 1",
                coordinate_system=coord_sys
            ),
            "F_2": ForceVector(
                magnitude=6000, angle=-30, wrt="+x", unit="N",
                name="F_2", description="Force 2",
                coordinate_system=coord_sys
            ),
            "F_R": ForceVector.unknown("F_R", wrt="+x", is_resultant=True, unit="N", coordinate_system=coord_sys),
        },
        "expected": {
            "F_1": {"magnitude": 4000, "angle": -30, "unit": "N", "wrt": "+y"},
            "F_2": {"magnitude": 6000, "angle": -30, "unit": "N", "wrt": "+x"},
            "F_R": {"magnitude": 8026, "angle": -1.22, "unit": "N", "wrt": "+x"},
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_7": {
        "name": "Problem 2-7",
        "description": """
        Resolve the force F_1 into components acting along the u and v axes and determine the magnitudes of the components.
        Note: u-v coordinate system with 75° between axes (u at 0°, v at 75°).
        """,
        "coordinate_system": CoordinateSystem.from_angle_between(
            "u", "v", axis1_angle=0, angle_between=75),
        "forces": lambda coord_sys: {
            "F_1": ForceVector(
                magnitude=4000, angle=45, unit="N",
                name="F_1", description="Force 1 at 45°",
                coordinate_system=coord_sys
            ),
        },
        "expected": {
            "F_1": {"magnitude": 4000, "angle": 45, "unit": "N", "wrt": "+x"},
            # From solution manual: F_1u = 2.07 kN, F_1v = 2.93 kN
            "F_1_components": {"u": 2070, "v": 2930, "unit": "N"},
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_8": {
        "name": "Problem 2-8",
        "description": """
        Resolve the force F_2 into components acting along the u and v axes and determine the magnitudes of the components.
        Note: u-v coordinate system with 75° between axes (u at 0°, v at 75°).
        """,
        "coordinate_system": CoordinateSystem.from_angle_between(
            "u", "v", axis1_angle=0, angle_between=75),
        "forces": lambda coord_sys: {
            "F_2": ForceVector(
                magnitude=6000, angle=330, unit="N",
                name="F_2", description="Force 2 at 330°",
                coordinate_system=coord_sys
            ),
        },
        "expected": {
            "F_2": {"magnitude": 6000, "angle": 330, "unit": "N", "wrt": "+x"},
            "F_2_components": {"u": 6000, "v": -3106, "unit": "N"},
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_9": {
        "name": "Problem 2-9",
        "description": """
        If the resultant force acting on the support is to be 1200 lb, directed horizontally to the right,
        determine the force F in rope A and the corresponding angle theta.
        """,
        "forces": {
            "F_A": ForceVector.unknown("F_A"),
            "F_B": ForceVector(
                magnitude=900, angle=330, unit="lbf",
                name="F_B", description="Force B"),
            "F_R": ForceVector(
                magnitude=1200, angle=0, unit="lbf",
                name="F_R", description="Resultant Force", is_resultant=True),
        },
        "expected": {
            "F_A": {"magnitude": 615.94, "angle": 46.936, "unit": "lbf", "wrt": "+x"},
            "F_B": {"magnitude": 900, "angle": 330, "unit": "lbf", "wrt": "+x"},
            "F_R": {"magnitude": 1200, "angle": 0, "unit": "lbf", "wrt": "+x"},
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_10": {
        "name": "Problem 2-10",
        "description": """
        Determine the magnitude of the resultant force and its direction,
        measured counterclockwise from the positive x axis.
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=800, unit="lbf",
                angle=-40, wrt="+y",
                name="F_1", description="Force 1 at 50° above horizontal"
            ),
            "F_2": ForceVector(
                magnitude=500, unit="lbf",
                angle=-35, wrt="+x",
                name="F_2", description="Force 2"
            ),
            "F_R": ForceVector.unknown("F_R", is_resultant=True),
        },
        "expected": {
            "F_1": {
                "magnitude": 800, "unit": "lbf",
                "angle": -40, "wrt": "+y"
            },
            "F_2": {
                "magnitude": 500, "unit": "lbf",
                "angle": -35, "wrt": "+x"
            },
            "F_R": {
                "magnitude": 979.655, "unit": "lbf",
                "angle": 19.440, "wrt": "+x"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_11": {
        "name": "Problem 2-11",
        "description": """
        The plate is subjected to the two forces at A and B as shown. If theta = 60°,
        determine the magnitude of the resultant of these two forces and its direction
        measured clockwise from the horizontal.
        """,
        "forces": {
            "F_A": ForceVector(
                magnitude=8000, unit="N",
                angle=-60, wrt="+y",
                name="F_A", description="Force A"
            ),
            "F_B": ForceVector(
                magnitude=6000, unit="N",
                angle=40, wrt="-y",
                name="F_B", description="Force B"
            ),
            "F_R": ForceVector.unknown("F_R", is_resultant=True),
        },
        "expected": {
            "F_A": {
                "magnitude": 8000, "unit": "N",
                "angle": -60, "wrt": "+y"
            },
            "F_B": {
                "magnitude": 6000, "unit": "N",
                "angle": 40, "wrt": "-y"
            },
            "F_R": {
                "magnitude": 10800, "unit": "N",
                "angle": -3.16, "wrt": "+x"
            },  # 3.16° clockwise from horizontal = 356.84° CCW
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_12": {
        "name": "Problem 2-12",
        "description": """
        Determine the angle of theta for connecting member A to the plate so that the
        resultant force of F_A and F_B is directed horizontally to the right. Also, what is
        the magnitude of the resultant force?
        """,
        "forces": {
            "F_A": ForceVector.unknown("F_A", magnitude=8000, wrt="+y",unit="N"),
            "F_B": ForceVector(
                magnitude=6000, unit="N",
                angle=40, wrt="-y",
                name="F_B", description="Force B"
            ),
            "F_R": ForceVector.unknown("F_R", angle=0, wrt="+x", unit="N", is_resultant=True),
        },
        "expected": {
            "F_A": {"magnitude": 8000, "angle": -54.9, "wrt": "+y", "unit": "N"},
            "F_B": {"magnitude": 6000, "angle": 40, "wrt": "-y", "unit": "N"},
            "F_R": {"magnitude": 10400, "angle": 0, "unit": "N"},
        },
        "debug": {
            "print_results": False,
            "assert_values": True,
        },
    },
    "problem_2_13": {
        "name": "Problem 2-13",
        "description": """
        The force acting on the gear tooth is Resolve this force into two components acting along the lines aa and bb.
        """,
        "coordinate_system": CoordinateSystem.from_angle_between(
            "x", "y", axis1_angle=0, angle_between=40),
        "forces": lambda coord_sys: {
            "F_A": ForceVector.unknown("F_A", angle=0, wrt="+x", unit="lbf", coordinate_system=coord_sys),
            "F_B": ForceVector.unknown("F_B", angle=0, wrt="-y", unit="lbf", coordinate_system=coord_sys),
            "F_R": ForceVector(magnitude=-20, unit="lbf", name="F_R", angle=80, wrt="+y", is_resultant=True, coordinate_system=coord_sys),
        },
        "expected": {
            "F_A": {"magnitude": 30.6, "angle": 0, "wrt": "+x", "unit": "lbf"},
            "F_B": {"magnitude": 26.9, "angle": 0, "wrt": "-y", "unit": "lbf"},
            "F_R": {"magnitude": -20, "angle": 80, "wrt": "+y", "unit": "lbf"},
        },
        "debug": {
            "print_results": True,
            "assert_values": True,
        },
    },
    "problem_2_14": {
        "name": "Problem 2-14",
        "description": """
        The component of force F acting along line aa is required to be 30 lb. Determine the magnitude of F and its component along line bb.
        """,
        "coordinate_system": CoordinateSystem.from_angle_between(
            "x", "y", axis1_angle=0, angle_between=40),
        "forces": lambda coord_sys: {
            "F_A": ForceVector(name="F_A", magnitude=30, angle=0, wrt="+x", unit="lbf", coordinate_system=coord_sys),
            "F_B": ForceVector.unknown("F_B", angle=0, wrt="-y", unit="lbf", coordinate_system=coord_sys),
            "F_R": ForceVector.unknown(unit="lbf", name="F_R", angle=80, wrt="+y", is_resultant=True, coordinate_system=coord_sys),
        },
        "expected": {
            "F_A": {"magnitude": 30, "angle": 0, "wrt": "+x", "unit": "lbf"},
            "F_B": {"magnitude": 26.4, "angle": 0, "wrt": "-y", "unit": "lbf"},
            "F_R": {"magnitude": -19.6, "angle": 80, "wrt": "+y", "unit": "lbf"},
        },
        "debug": {
            "print_results": True,
            "assert_values": True,
        },
    },
    "problem_2_15": {
        "name": "Problem 2-15",
        "description": """
        Force F acts on the frame such that its component acting along member is 650 lb, directed from towards , and the component acting along member is 500 lb, directed from towards . Determine the magnitude of F and its direction u. Set f = 60°.
        """,
        "forces": {
            "F_AB": ForceVector(name="F_AB", magnitude=650, angle=60, wrt="-x", unit="lbf"),
            "F_BC": ForceVector(name="F_BC", magnitude=500, angle=-45, wrt="+x", unit="lbf"),
            "F_R": ForceVector.unknown(unit="lbf", name="F_R",is_resultant=True),
        },
        "expected": {
            "F_AB": {"magnitude": 650, "angle": 60, "wrt": "-x", "unit": "lbf"},
            "F_BC": {"magnitude": 500, "angle": -45, "wrt": "+x", "unit": "lbf"},
            "F_R": {"magnitude": 916.91, "angle": 91.8, "wrt": "-x", "unit": "lbf"},
        },
        "debug": {
            "print_results": False,
            "assert_values": True,
        },
    },
    "problem_2_16": {
        "name": "Problem 2-16",
        "description": """
        Force F acts on the frame such that its component acting along member AB is 650 lb, directed from B towards A. Determine the required angle and the component acting along member BC. Set and u = 30°.
        """,
        "forces": {
            "F_BA": ForceVector(name="F_BA", magnitude=650, angle=-30, wrt="+F_R", unit="lbf"),
            "F_BC": ForceVector.unknown(name="F_BC", angle=-45, wrt="+x", unit="lbf"),
            "F_R": ForceVector(magnitude=850, wrt="-x", unit="lbf", name="F_R",is_resultant=True),
        },
        "expected": {
            "F_BA": {"magnitude": 650, "angle": 33.5, "wrt": "-x", "unit": "lbf"},
            "F_BC": {"magnitude": 433.64, "angle": -45, "wrt": "+x", "unit": "lbf"},
            "F_R": {"magnitude": 850, "angle": 63.5, "wrt": "-x", "unit": "lbf"},
        },
        "debug": {
            "print_results": False,
            "assert_values": True,
        },
    },
    "problem_2_17": {
        "name": "Problem 2-17",
        "description": """
        Determine the magnitude and direction of the resultant of the three forces by first finding the resultant F' = F1 + F2 and then forming FR = F' + F3.
        """,
        "forces": {
            "F_1": ForceVector(name="F_1", magnitude=30, angle=-36.87, wrt="-x", unit="N"),
            "F_2": ForceVector(name="F_2", magnitude=20, angle=-20, wrt="-y", unit="N"),
            "F_3": ForceVector(name="F_3", magnitude=50, angle=0, wrt="+x", unit="N"),
            "F_R": ForceVector.unknown(unit="N", name="F_R",is_resultant=True),
        },
        "expected": {
            "F_1": {"magnitude": 30, "angle": -36.87, "wrt": "-x", "unit": "N"},
            "F_2": {"magnitude": 20, "angle": -20, "wrt": "-y", "unit": "N"},
            "F_3": {"magnitude": 50, "angle": 0, "wrt": "+x", "unit": "N"},
            "F_R": {"magnitude": 19.2, "angle": -2.37, "wrt": "+x", "unit": "N"},
        },
        "debug": {
            "print_results": False,
            "assert_values": True,
        },
    },
    "problem_2_18": {
        "name": "Problem 2-18",
        "description": """
        Determine the magnitude and direction of the resultant of the three forces by first finding the resultant F' = F2 + F3 and then forming FR = F' + F1.
        """,
        "forces": {
            "F_1": ForceVector(name="F_1", magnitude=30, angle=-36.87, wrt="-x", unit="N"),
            "F_2": ForceVector(name="F_2", magnitude=20, angle=-20, wrt="-y", unit="N"),
            "F_3": ForceVector(name="F_3", magnitude=50, angle=0, wrt="+x", unit="N"),
            "F_R": ForceVector.unknown(unit="N", name="F_R",is_resultant=True),
        },
        "expected": {
            "F_1": {"magnitude": 30, "angle": -36.87, "wrt": "-x", "unit": "N"},
            "F_2": {"magnitude": 20, "angle": -20, "wrt": "-y", "unit": "N"},
            "F_3": {"magnitude": 50, "angle": 0, "wrt": "+x", "unit": "N"},
            "F_R": {"magnitude": 19.2, "angle": -2.37, "wrt": "+x", "unit": "N"},
        },
        "debug": {
            "print_results": False,
            "assert_values": True,
        },
    },
    "problem_2_19": {
        "name": "Problem 2-19",
        "description": """
        Determine the design angle for strut AB so that the 400-lb horizontal force has a component of 500 lb directed from A towards C. What is the component of force acting along member AB? Take f = 40°.
        """,
        "forces": {
            "F_AB": ForceVector.unknown(name="F_AB", wrt="+x", unit="lbf"),
            "F_AC": ForceVector(name="F_AC", magnitude=500, angle=-40, wrt="+F_AB", unit="lbf"),
            "F_R": ForceVector(magnitude=400, angle=0, wrt="-x",unit="lbf", name="F_R",is_resultant=True),
        },
        "expected": {
            "F_AB": {"magnitude": -621.15, "angle": -53.5, "wrt": "+x", "unit": "lbf"},
            "F_AC": {"magnitude": 500, "angle": -93.5, "wrt": "+x", "unit": "lbf"},
            "F_R": {"magnitude": 400, "angle": 0, "wrt": "-x", "unit": "lbf"},
        },
        "debug": {
            "print_results": False,
            "assert_values": True,
        },
    },
    "problem_2_20": {
        "name": "Problem 2-20",
        "description": """
        Determine the design angle between struts AB and AC so that the 400-lb horizontal force has a component of 600 lb which acts up to the left, in the same direction as from B towards A. Take u = 30°.
        """,
        "forces": {
            "F_AB": ForceVector(name="F_AB", magnitude=-600, angle=-30, wrt="+x", unit="lbf"),
            "F_AC": ForceVector.unknown(name="F_AC", unit="lbf"),
            "F_R": ForceVector(magnitude=400, angle=0, wrt="-x",unit="lbf", name="F_R",is_resultant=True),
        },
        "expected": {
            "F_AB": {"magnitude": -600, "angle": -30, "wrt": "+x", "unit": "lbf"},
            "F_AC": {"magnitude": 322.97, "angle": -38.3, "wrt": "-F_AB", "unit": "lbf"},
            "F_R": {"magnitude": 400, "angle": 0, "wrt": "-x", "unit": "lbf"},
        },
        "debug": {
            "print_results": False,
            "assert_values": True,
        },
    },
    "problem_2_21": {
        "name": "Problem 2-21",
        "description": """
        Determine the magnitude and direction of the resultant force, FR measured counterclockwise from the positive x axis. Solve the problem by first finding the resultant F′ = F1 + F2 and then forming FR = F′ + F3.
        """,
        "forces": {
            "F_1": ForceVector(name="F_1", magnitude=400, angle=90, wrt="+F_2", unit="N"),
            "F_2": ForceVector(name="F_2", magnitude=200, angle=150, wrt="-y", unit="N"),
            "F_3": ForceVector(name="F_3", magnitude=300, angle=0, wrt="-y", unit="N"),
            "F_R": ForceVector.unknown(unit="N", name="F_R",is_resultant=True),
        },
        "expected": {
            "F_1": {"magnitude": 400, "angle": 240, "wrt": "-y", "unit": "N"},
            "F_2": {"magnitude": 200, "angle": 150, "wrt": "-y", "unit": "N"},
            "F_3": {"magnitude": 300, "angle": 0, "wrt": "-y", "unit": "N"},
            "F_R": {"magnitude": 257.05, "angle": 163.45, "wrt": "+x", "unit": "N"},
        },
        "debug": {
            "print_results": False,
            "assert_values": True,
        },
    },
    "problem_2_22": {
        "name": "Problem 2-22",
        "description": """
        Determine the magnitude and direction of the resultant force, measured counterclockwise from the positive x axis. Solve l by first finding the resultant F′ = F2 + F3 and then forming FR = F′ + F1.
        """,
        "forces": {
            "F_1": ForceVector(name="F_1", magnitude=400, angle=90, wrt="+F_2", unit="N"),
            "F_2": ForceVector(name="F_2", magnitude=200, angle=150, wrt="-y", unit="N"),
            "F_3": ForceVector(name="F_3", magnitude=300, angle=0, wrt="-y", unit="N"),
            "F_R": ForceVector.unknown(unit="N", name="F_R",is_resultant=True),
        },
        "expected": {
            "F_1": {"magnitude": 400, "angle": 90, "wrt": "+F_2", "unit": "N"},
            "F_2": {"magnitude": 200, "angle": 150, "wrt": "-y", "unit": "N"},
            "F_3": {"magnitude": 300, "angle": 0, "wrt": "-y", "unit": "N"},
            "F_R": {"magnitude": 257.05, "angle": 163.45, "wrt": "+x", "unit": "N"},
        },
        "debug": {
            "print_results": False,
            "assert_values": True,
        },
    },
    "problem_2_23": {
        "name": "Problem 2-23",
        "description": """
        Two forces act on the screw eye. If F_1 = 400 N and F_2 = 600 N, determine the angle theta
        (0° ≤ theta ≤ 180°) between them, so that the resultant force has a magnitude of F_R = 800 N.
        """,
        "forces": {
            "F_1": ForceVector.unknown(magnitude=400, unit="N", name="F_1", description="Force 1"),
            "F_2": ForceVector.unknown(magnitude=600, unit="N", name="F_2", description="Force 2"),
            "F_R": ForceVector.unknown(magnitude=800, unit="N", name="F_R", is_resultant=True),
        },
        "expected": {
            "F_1": {"magnitude": 400, "angle": 75.5, "wrt": "+F_2", "unit": "N"},
            "F_2": {"magnitude": 600, "angle": -75.5, "wrt": "+F_1", "unit": "N"},
            "F_R": {"magnitude": 800, "angle": 0, "unit": "N"}
        },
        "debug": {
            "print_results": False,
            "assert_values": True,
        },
    },
    # TODO: Prolem 2-24 is symbolic
    "problem_2_25": {
        "name": "Problem 2-25",
        "description": """
        If F1 = 30 lb and F2 = 40 lb, determine the angles u and f so that the resultant force is directed along the positive x axis and has a magnitude of FR = 60 lb.
        """,
        "forces": {
            "F_1": ForceVector.unknown(
                magnitude=30, unit="lbf",
                name="F_1", description="Force 1 at 50° above horizontal"
            ),
            "F_2": ForceVector.unknown(
                magnitude=40, unit="lbf",
                name="F_2", description="Force 2"
            ),
            "F_R": ForceVector(
                magnitude=60, unit="lbf",
                angle=0, wrt="+x",
                name="F_R", is_resultant=True
            ),
        },
        "expected": {
            "F_1": {"magnitude": 30, "angle": 36.3, "wrt": "+x", "unit": "lbf"},
            "F_2": {"magnitude": 40, "angle": -26.4, "wrt": "+x", "unit": "lbf"},
            "F_R": {"magnitude": 60, "angle": 0, "wrt": "+x", "unit": "lbf"},
        },
        "debug": {
            "print_results": False,
            "assert_values": True,
        },
    },
    "problem_2_26": {
        "name": "Problem 2-26",
        "description": """
        Determine the magnitude and direction u of FA so that the resultant force is directed along the positive x axis and has a magnitude of 1250 N.
        """,
        "forces": {
            "F_A": ForceVector.unknown(
                name="F_A", description="Force A"
            ),
            "F_B": ForceVector(
                magnitude=800, unit="N",
                angle=-30, wrt="+x",
                name="F_B", description="Force B"
            ),
            "F_R": ForceVector(
                magnitude=1250, unit="N",
                angle=0, wrt="+x",
                name="F_R", is_resultant=True
            ),
        },
        "expected": {
            "F_A": {"magnitude": 686, "angle": -54.3, "wrt": "+y", "unit": "N"},
            "F_B": {"magnitude": 800, "angle": -30, "wrt": "+x", "unit": "N"},
            "F_R": {"magnitude": 1250, "angle": 0, "wrt": "+x", "unit": "N"},
        },
        "debug": {
            "print_results": False,
            "assert_values": True,
        },
    },
    "problem_2_27": {
        "name": "Problem 2-27",
        "description": """
        Determine the magnitude and direction, measured counterclockwise from the positive x axis, of the resultant force acting on the ring at O, if FA = 750 N and u = 45°.
        """,
        "forces": {
            "F_A": ForceVector(
                magnitude=750, unit="N",
                angle=-45, wrt="+y",
                name="F_A", description="Force A"
            ),
            "F_B": ForceVector(
                magnitude=800, unit="N",
                angle=-30, wrt="+x",
                name="F_B", description="Force B"
            ),
            "F_R": ForceVector.unknown(
                name="F_R", is_resultant=True
            ),
        },
        "expected": {
            "F_A": {"magnitude": 750, "angle": -45, "wrt": "+y", "unit": "N"},
            "F_B": {"magnitude": 800, "angle": -30, "wrt": "+x", "unit": "N"},
            "F_R": {"magnitude": 1230, "angle": 6.08, "wrt": "+x", "unit": "N"},
        },
        "debug": {
            "print_results": False,
            "assert_values": True,
        },
    },
    "problem_2_28": {
        "name": "Problem 2-28",
        "description": """
        Determine the magnitude of force F so that the resultant FR of the three forces is as small as possible. What is the minimum magnitude of FR?.
        """,
        "forces": {
            "F_1": ForceVector(name="F_1", magnitude=8000, angle=0, wrt="-y", unit="N"),
            "F_2": ForceVector(name="F_2", magnitude=6000, angle=0, wrt="+x", unit="N"),
            "F_3": ForceVector.unknown(name="F_3", angle=30, wrt="-y", unit="N"),
            "F_R": ForceVector.unknown(unit="N", angle=90, wrt="+F_3",name="F_R",is_resultant=True),
        },
        "expected": {
            "F_1": {"magnitude": 8000, "angle": 0, "wrt": "-y", "unit": "N"},
            "F_2": {"magnitude": 6000, "angle": 0, "wrt": "+x", "unit": "N"},
            "F_3": {"magnitude": 1196, "angle": 30, "wrt": "-y", "unit": "N"},
            "F_R": {"magnitude": 9928, "angle": 90, "wrt": "+F_3", "unit": "N"},
        },
        "debug": {
            "print_results": False,
            "assert_values": True,
        },
    },
    "problem_2_29": {
        "name": "Problem 2-29",
        "description": """
        If the resultant force of the two tugboats is , directed along the positive axis, determine the required magnitude of force FB and its direction u.
        """,
        "forces": {
            "F_A": ForceVector(
                magnitude=2000, unit="N",
                angle=30, wrt="+x",
                name="F_A", description="Force A"
            ),
            "F_B": ForceVector.unknown(
                name="F_B", description="Force B"
            ),
            "F_R": ForceVector(
                magnitude=3000, unit="N",
                angle=0, wrt="+x",
                name="F_R", is_resultant=True
            ),
        },
        "expected": {
            "F_A": {"magnitude": 2000, "angle": 30, "wrt": "+x", "unit": "N"},
            "F_B": {"magnitude": 1615, "angle": -38.3, "wrt": "+x", "unit": "N"},
            "F_R": {"magnitude": 3000, "angle": 0, "wrt": "+x", "unit": "N"},
        },
        "debug": {
            "print_results": False,
            "assert_values": True,
        },
    },
    "problem_2_30": {
        "name": "Problem 2-30",
        "description": """
        If and , determine the magnitude of the resultant force of the two tugboats and its direction measured clockwise from the positive x axis.
        """,
        "forces": {
            "F_A": ForceVector(
                magnitude=2000, unit="N",
                angle=30, wrt="+x",
                name="F_A", description="Force A"
            ),
            "F_B": ForceVector(
                magnitude=3000, unit="N",
                angle=-45, wrt="+x",
                name="F_B", description="Force B"
            ),
            "F_R": ForceVector.unknown(
                name="F_R", is_resultant=True
            ),
        },
        "expected": {
            "F_A": {"magnitude": 2000, "angle": 30, "wrt": "+x", "unit": "N"},
            "F_B": {"magnitude": 3000, "angle": -45, "wrt": "+x", "unit": "N"},
            "F_R": {"magnitude": 4013, "angle": -16.2, "wrt": "+x", "unit": "N"},
        },
        "debug": {
            "print_results": False,
            "assert_values": True,
        },
    },
    "problem_2_31": {
        "name": "Problem 2-31",
        "description": """
        If the resultant force of the two tugboats is required to be directed towards the positive axis, and is to be a minimum, determine the magnitude of and and the angle u.
        """,
        "forces": {
            "F_A": ForceVector(
                magnitude=2000, unit="N",
                angle=30, wrt="+x",
                name="F_A", description="Force A"
            ),
            "F_B": ForceVector.unknown(
                angle=-90, wrt="+F_R",
                name="F_B", description="Force B"
            ),
            "F_R": ForceVector.unknown(
                angle=0, wrt="+x",
                name="F_R", is_resultant=True
            ),
        },
        "expected": {
            "F_A": {"magnitude": 2000, "angle": 30, "wrt": "+x", "unit": "N"},
            "F_B": {"magnitude": 1000, "angle": -90, "wrt": "+x", "unit": "N"},
            "F_R": {"magnitude": 1730, "angle": 0, "wrt": "+x", "unit": "N"},
        },
        "debug": {
            "print_results": False,
            "assert_values": True,
        },
    },
}

# Debug control functions
def enable_debug(problem_name, print_results=True, assert_values=True):
    """Enable debug output for a specific problem."""
    if problem_name in FORCE_VECTOR_PROBLEMS:
        FORCE_VECTOR_PROBLEMS[problem_name]["debug"] = {"print_results": print_results, "assert_values": assert_values}


def disable_debug(problem_name):
    """Disable debug output for a specific problem."""
    if problem_name in FORCE_VECTOR_PROBLEMS:
        FORCE_VECTOR_PROBLEMS[problem_name]["debug"] = {"print_results": False, "assert_values": True}


def set_debug_all(print_results=True, assert_values=True):
    """Set debug settings for all problems."""
    for problem_name in FORCE_VECTOR_PROBLEMS:
        FORCE_VECTOR_PROBLEMS[problem_name]["debug"] = {"print_results": print_results, "assert_values": assert_values}


def solve_force_vector_problem(problem_name):
    """Solve a force vector problem and return the solution."""
    spec = FORCE_VECTOR_PROBLEMS[problem_name]

    # Create dynamic problem class with forces as class attributes
    class_attrs = {
        "name": spec["name"],
        "description": spec["description"],
    }

    # Get coordinate system if specified
    coord_system = spec.get("coordinate_system", CoordinateSystem.standard())

    # Get forces - check if it's a callable (lambda) or dict
    forces_spec = spec["forces"]
    if callable(forces_spec):
        # Call the lambda with the coordinate system to get the forces
        forces_dict: dict[str, ForceVector] = forces_spec(coord_system)  # type: ignore[assignment]
    else:
        # Legacy: forces is a dict, update their coordinate systems
        forces_dict: dict[str, ForceVector] = {}
        for force_name, force in forces_spec.items():
            # Update the force's coordinate system
            force.coordinate_system = coord_system
            forces_dict[force_name] = force

    # Add force vectors directly as class attributes
    class_attrs.update(forces_dict)

    # Create dynamic problem class
    ProblemClass = type(f"Problem_{problem_name}", (ParallelogramLawProblem,), class_attrs)

    # Solve
    problem_instance = ProblemClass()
    solution = problem_instance.solve()

    return solution


def verify_force_vector_results(solution, expected, debug_config, capsys, test_name):
    """Verify force vector results match expected values and optionally print them."""
    print_results = debug_config.get("print_results", False)
    assert_values = debug_config.get("assert_values", True)

    for force_name, expected_values in expected.items():
        # Handle component checking (e.g., "F_1_components")
        if force_name.endswith("_components"):
            base_force_name = force_name.replace("_components", "")
            if base_force_name not in solution:
                if print_results:
                    print(f"Warning: {base_force_name} not found in solution")
                continue

            force = solution[base_force_name]
            comp1, comp2 = force.get_components_in_system()

            if comp1 is None or comp2 is None:
                if print_results:
                    print(f"Warning: Could not compute components for {base_force_name}")
                continue

            # Get expected components
            axis1_label = force.coordinate_system.axis1_label
            axis2_label = force.coordinate_system.axis2_label
            expected_comp1 = expected_values.get(axis1_label)
            expected_comp2 = expected_values.get(axis2_label)

            # Convert to preferred units
            actual_comp1 = comp1.value / comp1.preferred.si_factor if comp1.preferred else comp1.value
            actual_comp2 = comp2.value / comp2.preferred.si_factor if comp2.preferred else comp2.value

            # Assert if enabled
            if assert_values and expected_comp1 is not None and expected_comp2 is not None:
                assert pytest.approx(expected_comp1, rel=0.01) == actual_comp1, \
                    f"{base_force_name} {axis1_label}-component: got {actual_comp1}, expected {expected_comp1}"
                assert pytest.approx(expected_comp2, rel=0.01) == actual_comp2, \
                    f"{base_force_name} {axis2_label}-component: got {actual_comp2}, expected {expected_comp2}"

            # Print components if enabled
            if print_results:
                with capsys.disabled():
                    unit_symbol = comp1.preferred.symbol if comp1.preferred else "SI"
                    print(f"  {base_force_name} components:")
                    print(f"    {axis1_label}: {actual_comp1:.3f} {unit_symbol}")
                    print(f"    {axis2_label}: {actual_comp2:.3f} {unit_symbol}")

            continue

        # Regular force checking
        if force_name not in solution:
            if print_results:
                print(f"Warning: {force_name} not found in solution")
            continue

        force = solution[force_name]
        expected_mag = expected_values["magnitude"]
        expected_ang_deg = expected_values["angle"]
        expected_wrt = expected_values.get("wrt", "+x")  # Default to "+x" if not specified

        # Use new API: magnitude_in() handles unit conversion automatically
        actual_mag_in_preferred = force.magnitude_in(force.magnitude.preferred) if force.magnitude.preferred else force.magnitude.value

        # Use new API: angle_in() handles both unit conversion and reference system transformation
        # Pass solution dict to support force-relative references (e.g., "-F_AB")
        actual_ang_in_wrt = force.angle_in("degree", wrt=expected_wrt, forces=solution)

        # Normalize angles to [0, 360) range for comparison
        actual_ang_in_wrt = actual_ang_in_wrt % 360
        expected_ang_deg_normalized = expected_ang_deg % 360

        # Only assert if enabled for this problem
        if assert_values:
            assert pytest.approx(expected_mag, rel=0.01) == actual_mag_in_preferred, \
                f"{force_name} magnitude: got {actual_mag_in_preferred}, expected {expected_mag}"
            assert pytest.approx(expected_ang_deg_normalized, rel=0.01) == actual_ang_in_wrt, \
                f"{force_name} angle (wrt {expected_wrt}): got {actual_ang_in_wrt}°, expected {expected_ang_deg_normalized}°"

    # Print results only if enabled for this problem
    if print_results:
        with capsys.disabled():
            print(f"\n{test_name} results:")
            for force_name in sorted(solution.keys()):
                force = solution[force_name]

                # Get expected wrt for this force (if specified)
                force_expected = expected.get(force_name, {})
                display_wrt = force_expected.get("wrt", "+x")  # Default to "+x"

                # Use new API for conversions (pass solution for force-relative references)
                actual_ang_in_wrt = force.angle_in("degree", wrt=display_wrt, forces=solution) % 360

                if force.magnitude.preferred:
                    mag_value_in_preferred = force.magnitude_in(force.magnitude.preferred)
                    mag_unit = force.magnitude.preferred.symbol
                else:
                    mag_value_in_preferred = force.magnitude.value
                    mag_unit = "SI"

                # Format wrt for display
                wrt_display = f" wrt {display_wrt}" if display_wrt != "+x" else ""
                print(f"  {force_name}: magnitude={mag_value_in_preferred:.3f} {mag_unit}, angle={actual_ang_in_wrt:.3f}°{wrt_display}")

                # Print components if non-standard coordinate system
                if not force.coordinate_system.is_orthogonal or force.coordinate_system.axis1_label != "x":
                    comp1, comp2 = force.get_components_in_system()
                    if comp1 is not None and comp2 is not None:
                        axis1_label = force.coordinate_system.axis1_label
                        axis2_label = force.coordinate_system.axis2_label
                        comp1_val = comp1.value / comp1.preferred.si_factor if comp1.preferred else comp1.value
                        comp2_val = comp2.value / comp2.preferred.si_factor if comp2.preferred else comp2.value
                        unit_symbol = comp1.preferred.symbol if comp1.preferred else "SI"
                        print(f"    {axis1_label}: {comp1_val:.3f} {unit_symbol}, {axis2_label}: {comp2_val:.3f} {unit_symbol}")

            # Show assertion status
            if not assert_values:
                print(f"  [NOTE: Assertions disabled for {test_name}]")


# Single parameterized test for all force vector problems
@pytest.mark.parametrize("problem_name", list(FORCE_VECTOR_PROBLEMS.keys()))
def test_force_vector_problem(problem_name, capsys):
    """Test all force vector equilibrium problems."""
    problem_spec = FORCE_VECTOR_PROBLEMS[problem_name]
    solution = solve_force_vector_problem(problem_name)
    expected = problem_spec["expected"]
    debug_config = problem_spec.get("debug", {"print_results": False, "assert_values": True})
    verify_force_vector_results(solution, expected, debug_config, capsys, problem_name)


# Example of how easy it is to add a new problem:
#
# FORCE_VECTOR_PROBLEMS["problem_2_3"] = {
#     "name": "Problem 2-3",
#     "description": "Three force equilibrium problem...",
#     "forces": {
#         "F_1": ForceVector(magnitude=300, angle=30, unit="N", name="F_1", description="Force 1"),
#         "F_2": ForceVector.unknown("F_2"),  # Unknown force to solve for
#         "F_3": ForceVector(magnitude=400, angle=210, unit="N", name="F_3", description="Force 3"),
#         "F_R": ForceVector(magnitude=0, angle=0, unit="N", name="F_R", description="Resultant Force", is_resultant=True),
#     },
#     "expected": {
#         "F_1": {"magnitude": 300, "angle": 30},
#         "F_2": {"magnitude": 450.5, "angle": 120.7},
#         "F_3": {"magnitude": 400, "angle": 210},
#         "F_R": {"magnitude": 0, "angle": 0},
#     },
#     "debug": {"print_results": False, "assert_values": True},
# }
# That's it! The test will automatically pick up the new problem.
