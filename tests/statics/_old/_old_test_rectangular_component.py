"""
Comprehensive tests for ComponentSolver using problems 2-32 to 2-44 from textbook.

These tests validate the Cartesian/Component method for solving force equilibrium
problems using scalar notation: ΣFx = 0, ΣFy = 0.
"""

import math

import pytest

from qnty.problems.rectangular_vector import RectangularVectorProblem
from qnty.spatial import _Vector

# Problem definitions - single source of truth
COMPONENT_METHOD_PROBLEMS = {
    "problem_2_32": {
        "name": "Problem 2-32",
        "description": """
        Determine the magnitude of the resultant force and its direction,
        measured counterclockwise from the positive x axis.
        """,
        "forces": {
            "F_1": _Vector(
                magnitude=200, unit="N",
                angle=-45, wrt="+y",
                name="F_1", description="Force 1 at 45° from +x"
            ),
            "F_2": _Vector(
                magnitude=-150, unit="N",
                angle=-30, wrt="+x",
                name="F_2", description="Force 2 at 30° from -x"
            ),
            "F_R": _Vector.unknown(
                name="F_R", is_resultant=True, description="Resultant Force"
            )
        },
        "expected": {
            "F_1": {
                "magnitude": 200, "unit": "N",
                "angle": -45, "wrt": "+y"
            },
            "F_2": {
                "magnitude": -150, "unit": "N",
                "angle": -30, "wrt": "+x"
            },
            "F_R": {
                "magnitude": 217, "unit": "N",
                "angle": 87, "wrt": "+x"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_33": {
        "name": "Problem 2-33",
        "description": """
        Determine the magnitude of the resultant force and its direction, measured clockwise from the positive x axis.
        """,
        "forces": {
            "F_1": _Vector(
                magnitude=400, unit="N",
                angle=30, wrt="+x",
                name="F_1", description="Force 1"
            ),
            "F_2": _Vector(
                magnitude=800, unit="N",
                angle=45, wrt="-y",
                name="F_2", description="Force 2"
            ),
            "F_R": _Vector.unknown(
                name="F_R", is_resultant=True, description="Resultant Force"
            )
        },
        "expected": {
            "F_1": {
                "magnitude": 400, "unit": "N",
                "angle": 30, "wrt": "+x"
            },
            "F_2": {
                "magnitude": 800, "unit": "N",
                "angle": 45, "wrt": "-y"
            },
            "F_R": {
                "magnitude": 983, "unit": "N",
                "angle": -21.8, "wrt": "+x"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_34": {
        "name": "Problem 2-34",
        "description": """
        Resolve F1 and F2 into their x and y components.
        """,
        "forces": {
            "F_1": _Vector(
                magnitude=400, unit="N",
                angle=-30, wrt="+y",
                name="F_1", description="Force 1"
            ),
            "F_2": _Vector(
                magnitude=250, unit="N",
                angle=-45, wrt="+x",
                name="F_2", description="Force 2"
            ),
        },
        "expected": {
            "F_1": {
                "x": 200, "y": 346.4, "unit": "N"
            },
            "F_2": {
                "x": 177, "y": -177, "unit": "N"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_35": {
        "name": "Problem 2-35",
        "description": """
        Determine the magnitude of the resultant force and its direction measured counterclockwise from the positive x axis.
        """,
        "forces": {
            "F_1": _Vector(
                magnitude=400, unit="N",
                angle=-30, wrt="+y",
                name="F_1", description="Force 1"
            ),
            "F_2": _Vector(
                magnitude=250, unit="N",
                angle=-45, wrt="+x",
                name="F_2", description="Force 2"
            ),
            "F_R": _Vector.unknown(
                name="F_R", is_resultant=True, description="Resultant Force"
            )
        },
        "expected": {
            "F_1": {
                "x": 200, "y": 346.4, "unit": "N"
            },
            "F_2": {
                "x": 177, "y": -177, "unit": "N"
            },
            "F_R": {
                "magnitude": 413, "unit": "N",
                "angle": 24.2, "wrt": "+x"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_36": {
        "name": "Problem 2-36",
        "description": """
        Resolve each force acting on the gusset plate into its and y components, and express each force as a Cartesian vector.
        """,
        "forces": {
            "F_1": _Vector(
                magnitude=900, unit="N",
                angle=0, wrt="+x",
                name="F_1", description="Force 1"
            ),
            "F_2": _Vector(
                magnitude=750, unit="N",
                angle=45, wrt="+x",
                name="F_2", description="Force 2"
            ),
            "F_3": _Vector(
                magnitude=-650, unit="N",
                angle=-36.87, wrt="-x",
                name="F_3", description="Force 3"
            ),
        },
        "expected": {
            "F_1": {
                "x": 900, "y": 0, "unit": "N"
            },
            "F_2": {
                "x": 530, "y": 530, "unit": "N"
            },
            "F_3": {
                "x": 520, "y": -390, "unit": "N"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_37": {
        "name": "Problem 2-37",
        "description": """
        Determine the magnitude of the resultant force acting on the plate and its direction, measured counterclockwise from the positive x axis.
        """,
        "forces": {
            "F_1": _Vector(
                magnitude=900, unit="N",
                angle=0, wrt="+x",
                name="F_1", description="Force 1"
            ),
            "F_2": _Vector(
                magnitude=750, unit="N",
                angle=45, wrt="+x",
                name="F_2", description="Force 2"
            ),
            "F_3": _Vector(
                magnitude=-650, unit="N",
                angle=-36.87, wrt="-x",
                name="F_3", description="Force 3"
            ),
            "F_R": _Vector.unknown(
                name="F_R", is_resultant=True, description="Resultant Force"
            )
        },
        "expected": {
            "F_1": {
                "x": 900, "y": 0, "unit": "N"
            },
            "F_2": {
                "x": 530, "y": 530, "unit": "N"
            },
            "F_3": {
                "x": 520, "y": -390, "unit": "N"
            },
            "F_R": {
                "magnitude": 1955, "unit": "N",
                "angle": 4.12, "wrt": "+x"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_38": {
        "name": "Problem 2-38",
        "description": """
        Express each of the three forces acting on the support in Cartesian vector form and determine the magnitude of the resultant force and its direction, measured clockwise from positive x axis.
        """,
        "forces": {
            "F_1": _Vector(
                magnitude=50, unit="N",
                angle=53.15, wrt="+x",
                name="F_1", description="Force 1"
            ),
            "F_2": _Vector(
                magnitude=80, unit="N",
                angle=-15, wrt="-y",
                name="F_2", description="Force 2"
            ),
            "F_3": _Vector(
                magnitude=30, unit="N",
                angle=0, wrt="+x",
                name="F_3", description="Force 3"
            ),
            "F_R": _Vector.unknown(
                name="F_R", is_resultant=True, description="Resultant Force"
            )
        },
        "expected": {
            "F_1": {
                "x": 30, "y": 40, "unit": "N"
            },
            "F_2": {
                "x": -20.71, "y": -77.3, "unit": "N"
            },
            "F_3": {
                "x": 30, "y": 0, "unit": "N"
            },
            "F_R": {
                "magnitude": 54.2, "unit": "N",
                "angle": -43.5, "wrt": "+x"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_39": {
        "name": "Problem 2-39",
        "description": """
        Determine the x and y components of F1 and F2.
        """,
        "forces": {
            "F_1": _Vector(
                magnitude=200, unit="N",
                angle=-45, wrt="+y",
                name="F_1", description="Force 1"
            ),
            "F_2": _Vector(
                magnitude=-150, unit="N",
                angle=-30, wrt="+x",
                name="F_2", description="Force 2"
            ),
        },
        "expected": {
            "F_1": {
                "x": 141, "y": 141, "unit": "N"
            },
            "F_2": {
                "x": -130, "y": 75, "unit": "N"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_40": {
        "name": "Problem 2-40",
        "description": """
        Determine the magnitude of the resultant force and its direction, measured counterclockwise from the positive x axis.
        """,
        "forces": {
            "F_1": _Vector(
                magnitude=200, unit="N",
                angle=-45, wrt="+y",
                name="F_1", description="Force 1"
            ),
            "F_2": _Vector(
                magnitude=-150, unit="N",
                angle=-30, wrt="+x",
                name="F_2", description="Force 2"
            ),
            "F_R": _Vector.unknown(
                name="F_R", is_resultant=True, description="Resultant Force"
            )
        },
        "expected": {
            "F_1": {
                "x": 141, "y": 141, "unit": "N"
            },
            "F_2": {
                "x": -130, "y": 75, "unit": "N"
            },
            "F_R": {
                "magnitude": 217, "unit": "N",
                "angle": 87, "wrt": "+x"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_41": {
        "name": "Problem 2-41",
        "description": """
        Determine the magnitude of the resultant force and its direction,
        measured counterclockwise from the positive x axis.
        """,
        "forces": {
            "F_1": _Vector(
                magnitude=4000, unit="N",
                angle=0, wrt="+x",
                name="F_1", description="Force 1"
            ),
            "F_2": _Vector(
                magnitude=5000, unit="N",
                angle=45, wrt="+x",
                name="F_2", description="Force 2"
            ),
            "F_3": _Vector(
                magnitude=8000, unit="N",
                angle=60, wrt="+F_2",
                name="F_3", description="Force 3"
            ),
            "F_R": _Vector.unknown(
                name="F_R", is_resultant=True, description="Resultant Force"
            )
        },
        "expected": {
            "F_1": {
                "magnitude": 4000, "unit": "N",
                "angle": 0, "wrt": "+x"
            },
            "F_2": {
                "magnitude": 5000, "unit": "N",
                "angle": 45, "wrt": "+x"
            },
            "F_3": {
                "magnitude": 8000, "unit": "N",
                "angle": 15, "wrt": "+y"
            },
            "F_R": {
                "magnitude": 12520, "unit": "N",
                "angle": 64.12, "wrt": "+x"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_42": {
        "name": "Problem 2-42",
        "description": """
        Express F1, F2, and F3 as Cartesian vectors.
        """,
        "forces": {
            "F_1": _Vector(
                magnitude=850, unit="N",
                angle=53.13, wrt="-y",
                name="F_1", description="Force 1"
            ),
            "F_2": _Vector(
                magnitude=625, unit="N",
                angle=-30, wrt="-y",
                name="F_2", description="Force 2"
            ),
            "F_3": _Vector(
                magnitude=750, unit="N",
                angle=45, wrt="+y",
                name="F_3", description="Force 3"
            ),
        },
        "expected": {
            "F_1": {
                "x": 680, "y": -510, "unit": "N"
            },
            "F_2": {
                "x": -312, "y": -541, "unit": "N"
            },
            "F_3": {
                "x": -530, "y": 530.3, "unit": "N"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_43": {
        "name": "Problem 2-43",
        "description": """
        Determine the magnitude of the resultant force and its direction measured counterclockwise from the positive x axis.
        """,
        "forces": {
            "F_1": _Vector(
                magnitude=850, unit="N",
                angle=53.13, wrt="-y",
                name="F_1", description="Force 1"
            ),
            "F_2": _Vector(
                magnitude=625, unit="N",
                angle=-30, wrt="-y",
                name="F_2", description="Force 2"
            ),
            "F_3": _Vector(
                magnitude=750, unit="N",
                angle=45, wrt="+y",
                name="F_3", description="Force 3"
            ),
            "F_R": _Vector.unknown(
                name="F_R", is_resultant=True, description="Resultant Force"
            )
        },
        "expected": {
            "F_1": {
                "x": 680, "y": -510, "unit": "N"
            },
            "F_2": {
                "x": -312, "y": -541, "unit": "N"
            },
            "F_3": {
                "x": -530, "y": 530.3, "unit": "N"
            },
            "F_R": {
                "magnitude": 546, "unit": "N",
                "angle": 253, "wrt": "+x"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_44": {
        "name": "Problem 2-44",
        "description": """
        Determine the magnitude of the resultant force and its direction measured counterclockwise from the positive x axis.
        """,
        "forces": {
            "F_1": _Vector(
                magnitude=40, unit="lbf",
                angle=53.13, wrt="+x",
                name="F_1", description="Force 1"
            ),
            "F_2": _Vector(
                magnitude=91, unit="lbf",
                angle=-67.4, wrt="+x",
                name="F_2", description="Force 2"
            ),
            "F_3": _Vector(
                magnitude=30, unit="lbf",
                angle=0, wrt="+x",
                name="F_3", description="Force 3"
            ),
            "F_R": _Vector.unknown(
                name="F_R", is_resultant=True, description="Resultant Force"
            )
        },
        "expected": {
            "F_1": {
                "magnitude": 40, "unit": "lbf",
                "angle": 53.13, "wrt": "+x"
            },
            "F_2": {
                "magnitude": 91, "unit": "lbf",
                "angle": -67.4, "wrt": "+x"
            },
            "F_3": {
                "magnitude": 30, "unit": "lbf",
                "angle": 0, "wrt": "+x"
            },
            "F_R": {
                "magnitude": 103, "unit": "lbf",
                "angle": -30.3, "wrt": "+x"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    # TODO: Problem 2-45 is symbolic solution only - skip for now
    "problem_2_46": {
        "name": "Problem 2-46",
        "description": """
        Determine the magnitude of the resultant force and its direction measured counterclockwise from the positive x axis.
        """,
        "forces": {
            "F_A": _Vector(
                magnitude=700, unit="N",
                angle=-30, wrt="+y",
                name="F_A", description="Force A"
            ),
            "F_B": _Vector.unknown(
                name="F_B", description="Force B"
            ),
            "F_R": _Vector(
                magnitude=1500, unit="N",
                angle=0, wrt="+y", is_resultant=True,
                name="F_R", description="Resultant Force"
            ),
        },
        "expected": {
            "F_A": {
                "magnitude": 700, "unit": "N",
                "angle": -30, "wrt": "+y"
            },
            "F_B": {
                "magnitude": 960, "unit": "N",
                "angle": -68.6, "wrt": "-x"
            },
            "F_R": {
                "magnitude": 1500, "unit": "N",
                "angle": 0, "wrt": "+y"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_47": {
        "name": "Problem 2-47",
        "description": """
        Determine the magnitude and orientation, measured counterclockwise from the positive y axis, of the resultant force acting on the bracket, if FB = 600 N and u = 20°.
        """,
        "forces": {
            "F_A": _Vector(
                magnitude=700, unit="N",
                angle=-30, wrt="+y",
                name="F_A", description="Force A"
            ),
            "F_B": _Vector(
                magnitude=600, unit="N",
                angle=-20, wrt="-x",
                name="F_B", description="Force B"
            ),
            "F_R": _Vector.unknown(
                is_resultant=True,
                name="F_R", description="Resultant Force"
            ),
        },
        "expected": {
            "F_A": {
                "magnitude": 700, "unit": "N",
                "angle": -30, "wrt": "+y"
            },
            "F_B": {
                "magnitude": 600, "unit": "N",
                "angle": -20, "wrt": "-x"
            },
            "F_R": {
                "magnitude": 839, "unit": "N",
                "angle": 14.8, "wrt": "+y"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_48": {
        "name": "Problem 2-48",
        "description": """
        Three forces act on the bracket. Determine the magnitude and direction of so that the resultant force is directed along the positive axis and has a magnitude of 800 N.
        """,
        "forces": {
            "F_1": _Vector.unknown(
                name="F_1", description="Force 1"
            ),
            "F_2": _Vector(
                magnitude=200, unit="N",
                angle=0, wrt="+y",
                name="F_2", description="Force 2"
            ),
            "F_3": _Vector(
                magnitude=180, unit="N",
                angle=-22.6, wrt="-x",
                name="F_3", description="Force 3"
            ),
            "F_R": _Vector(
                magnitude=800, unit="N",
                angle=-60, wrt="+y",
                is_resultant=True,
                name="F_R", description="Resultant Force"
            ),
        },
        "expected": {
            "F_1": {
                "magnitude": 869, "unit": "N",
                "angle": -21.3, "wrt": "+F_R"
            },
            "F_2": {
                "magnitude": 200, "unit": "N",
                "angle": 0, "wrt": "+y"
            },
            "F_3": {
                "magnitude": 180, "unit": "N",
                "angle": -22.6, "wrt": "-x"
            },
            "F_R": {
                "magnitude": 800, "unit": "N",
                "angle": -60, "wrt": "+y"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_49": {
        "name": "Problem 2-49",
        "description": """
        If and determine the magnitude and direction, measured counterclockwise from the positive x¿ axis, of the resultant force acting on the bracket.
        """,
        "forces": {
            "F_1": _Vector(
                magnitude=300, unit="N",
                angle=-70, wrt="+y",
                name="F_1", description="Force 1"
            ),
            "F_2": _Vector(
                magnitude=200, unit="N",
                angle=0, wrt="+y",
                name="F_2", description="Force 2"
            ),
            "F_3": _Vector(
                magnitude=180, unit="N",
                angle=-22.6, wrt="-x",
                name="F_3", description="Force 3"
            ),
            "F_R": _Vector.unknown(
                is_resultant=True,
                name="F_R", description="Resultant Force"
            ),
        },
        "expected": {
            "F_1": {
                "magnitude": 300, "unit": "N",
                "angle": -70, "wrt": "+y"
            },
            "F_2": {
                "magnitude": 200, "unit": "N",
                "angle": 0, "wrt": "+y"
            },
            "F_3": {
                "magnitude": 180, "unit": "N",
                "angle": -22.6, "wrt": "-x"
            },
            "F_R": {
                "magnitude": 389, "unit": "N",
                "angle": 52.7, "wrt": "+F_1"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_50": {
        "name": "Problem 2-50",
        "description": """
        Express F1, F2, and F3 as Cartesian vectors.
        """,
        "forces": {
            "F_1": _Vector(
                magnitude=15000, unit="N",
                angle=-40, wrt="+y",
                name="F_1", description="Force 1"
            ),
            "F_2": _Vector(
                magnitude=26000, unit="N",
                angle=-22.6, wrt="-x",
                name="F_2", description="Force 2"
            ),
            "F_3": _Vector(
                magnitude=36000, unit="N",
                angle=-30, wrt="+x",
                name="F_3", description="Force 3"
            ),
        },
        "expected": {
            "F_1": {
                "x": 9642, "y": 11491, "unit": "N"
            },
            "F_2": {
                "x": -24003, "y": 9992, "unit": "N"
            },
            "F_3": {
                "x": 31177, "y": -18000, "unit": "N"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_51": {
        "name": "Problem 2-51",
        "description": """
        Determine the magnitude of the resultant force and its orientation measured counterclockwise from the positive x axis.
        """,
        "forces": {
            "F_1": _Vector(
                magnitude=15000, unit="N",
                angle=-40, wrt="+y",
                name="F_1", description="Force 1"
            ),
            "F_2": _Vector(
                magnitude=26000, unit="N",
                angle=-22.6, wrt="-x",
                name="F_2", description="Force 2"
            ),
            "F_3": _Vector(
                magnitude=36000, unit="N",
                angle=-30, wrt="+x",
                name="F_3", description="Force 3"
            ),
            "F_R": _Vector.unknown(
                is_resultant=True,
                name="F_R", description="Resultant Force"
            ),
        },
        "expected": {
            "F_1": {
                "x": 9642, "y": 11491, "unit": "N"
            },
            "F_2": {
                "x": -24003, "y": 9992, "unit": "N"
            },
            "F_3": {
                "x": 31177, "y": -18000, "unit": "N"
            },
            "F_R": {
                "magnitude": 17200, "unit": "N",
                "angle": 11.7, "wrt": "+x"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_52": {
        "name": "Problem 2-52",
        "description": """
        Determine the x and y components of each force acting on the gusset plate of a bridge truss. Show that the resultant force is zero.
        """,
        "forces": {
            "F_1": _Vector(
                magnitude=-8000, unit="N",
                angle=53.13, wrt="+y",
                name="F_1", description="Force 1"
            ),
            "F_2": _Vector(
                magnitude=6000, unit="N",
                angle=53.13, wrt="+x",
                name="F_2", description="Force 2"
            ),
            "F_3": _Vector(
                magnitude=4000, unit="N",
                angle=0, wrt="-x",
                name="F_3", description="Force 3"
            ),
            "F_4": _Vector(
                magnitude=6000, unit="N",
                angle=0, wrt="-x",
                name="F_4", description="Force 4"
            ),
            "F_R": _Vector.unknown(
                is_resultant=True,
                name="F_R", description="Resultant Force"
            ),
        },
        "expected": {
            "F_1": {
                "x": 6400, "y": -4800, "unit": "N"
            },
            "F_2": {
                "x": 3600, "y": 4800, "unit": "N"
            },
            "F_3": {
                "x": -4000, "y": 0, "unit": "N"
            },
            "F_4": {
                "x": -6000, "y": 0, "unit": "N"
            },
            "F_R": {
                "x": 0, "y": 0, "unit": "N"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_53": {
        "name": "Problem 2-53",
        "description": """
        Express and F2 as Cartesian vectors.
        """,
        "forces": {
            "F_1": _Vector(
                magnitude=30000, unit="N",
                angle=-30, wrt="-y",
                name="F_1", description="Force 1"
            ),
            "F_2": _Vector(
                magnitude=26000, unit="N",
                angle=-67.4, wrt="-x",
                name="F_2", description="Force 2"
            ),
        },
        "expected": {
            "F_1": {
                "x": -15000, "y": -26000, "unit": "N"
            },
            "F_2": {
                "x": -10000, "y": 24000, "unit": "N"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_54": {
        "name": "Problem 2-54",
        "description": """
        Determine the magnitude of the resultant force and its direction measured counterclockwise from the positive x axis.
        """,
        "forces": {
            "F_1": _Vector(
                magnitude=30000, unit="N",
                angle=-30, wrt="-y",
                name="F_1", description="Force 1"
            ),
            "F_2": _Vector(
                magnitude=26000, unit="N",
                angle=-67.4, wrt="-x",
                name="F_2", description="Force 2"
            ),
            "F_R": _Vector.unknown(
                is_resultant=True,
                name="F_R", description="Resultant Force"
            ),
        },
        "expected": {
            "F_1": {
                "x": -15000, "y": -26000, "unit": "N"
            },
            "F_2": {
                "x": -10000, "y": 24000, "unit": "N"
            },
            "F_R": {
                "magnitude": 25100, "unit": "N",
                "angle": 185, "wrt": "+x"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_55": {
        "name": "Problem 2-55",
        "description": """
        Determine the magnitude of force so that the resultant force of the three forces is as small as possible. What is the magnitude of the resultant force?
        """,
        "forces": {
            "F_1": _Vector(
                magnitude=8000, unit="N",
                angle=0, wrt="+x",
                name="F_1", description="Force 1"
            ),
            "F_2": _Vector.unknown(
                angle=45, wrt="-x",
                name="F_2", description="Force 2"
            ),
            "F_3": _Vector(
                magnitude=14000, unit="N",
                angle=-30, wrt="-x",
                name="F_3", description="Force 3"
            ),
            "F_R": _Vector.unknown(
                angle=135, wrt="+x",
                is_resultant=True,
                name="F_R", description="Resultant Force"
            ),
        },
        "expected": {
            "F_1": {
                "magnitude": 8000, "unit": "N",
                "angle": 0, "wrt": "+x"
            },
            "F_2": {
                "magnitude": 2030, "unit": "N",
                "angle": 45, "wrt": "-x"
            },
            "F_3": {
                "magnitude": 14000, "unit": "N",
                "angle": -30, "wrt": "-x"
            },
            "F_R": {
                "magnitude": 7870, "unit": "N",
                "angle": 135, "wrt": "+x"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_56": {
        "name": "Problem 2-56",
        "description": """
        If the magnitude of the resultant force acting on the bracket is to be 450 N directed along the positive u axis, determine the magnitude of F1 and its direction f.
        """,
        "forces": {
            "F_1": _Vector.unknown(
                name="F_1", description="Force 1"
            ),
            "F_2": _Vector(
                magnitude=200, unit="N",
                angle=0, wrt="+x",
                name="F_2", description="Force 2"
            ),
            "F_3": _Vector(
                magnitude=260, unit="N",
                angle=22.6, wrt="-y",
                name="F_3", description="Force 3"
            ),
            "F_R": _Vector(
                magnitude=450, unit="N",
                angle=30, wrt="+x",
                is_resultant=True,
                name="F_R", description="Resultant Force"
            ),
        },
        "expected": {
            "F_1": {
                "magnitude": 474, "unit": "N",
                "angle": -10.9, "wrt": "+y"
            },
            "F_2": {
                "magnitude": 200, "unit": "N",
                "angle": 0, "wrt": "+x"
            },
            "F_3": {
                "magnitude": 260, "unit": "N",
                "angle": 22.6, "wrt": "-y"
            },
            "F_R": {
                "magnitude": 450, "unit": "N",
                "angle": 30, "wrt": "+x"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    # TODO: Problem 2-57 requires derivative/minimization

    "problem_2_59": {
        "name": "Problem 2-59",
        "description": """
        If F = 5 kN and u = 30°, determine the magnitude of the resultant force and its direction, measured counterclockwise from the positive x axis.
        """,
        "forces": {
            "F_1": _Vector(
                magnitude=6000, unit="N",
                angle=0, wrt="+x",
                name="F_1", description="Force 1"
            ),
            "F_2": _Vector(
                magnitude=5000, unit="N",
                angle=-30, wrt="+y",
                name="F_2", description="Force 2"
            ),
            "F_3": _Vector(
                magnitude=4000, unit="N",
                angle=15, wrt="+y",
                name="F_3", description="Force 3 at 15° from +y toward -x (8 kN)"
            ),
            "F_R": _Vector.unknown(
                is_resultant=True,
                name="F_R", description="Resultant Force"
            ),
        },
        "expected": {
            "F_1": {
                "magnitude": 6000, "unit": "N",
                "angle": 0, "wrt": "+x"
            },
            "F_2": {
                "magnitude": 5000, "unit": "N",
                "angle": -30, "wrt": "+y"
            },
            "F_3": {
                "magnitude": 4000, "unit": "N",
                "angle": 15, "wrt": "+y"
            },
            "F_R": {
                "magnitude": 11080, "unit": "N",
                "angle": 47.7, "wrt": "+x"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },

}


# Debug control functions
def enable_debug(problem_name, print_results=True, assert_values=True):
    """Enable debug output for a specific problem."""
    if problem_name in COMPONENT_METHOD_PROBLEMS:
        COMPONENT_METHOD_PROBLEMS[problem_name]["debug"] = {
            "print_results": print_results,
            "assert_values": assert_values
        }


def disable_debug(problem_name):
    """Disable debug output for a specific problem."""
    if problem_name in COMPONENT_METHOD_PROBLEMS:
        COMPONENT_METHOD_PROBLEMS[problem_name]["debug"] = {
            "print_results": False,
            "assert_values": True
        }


def set_debug_all(print_results=True, assert_values=True):
    """Set debug settings for all problems."""
    for problem_name in COMPONENT_METHOD_PROBLEMS:
        COMPONENT_METHOD_PROBLEMS[problem_name]["debug"] = {
            "print_results": print_results,
            "assert_values": assert_values
        }


def solve_component_problem(problem_name):
    """Solve a component method problem and return the solution."""
    spec = COMPONENT_METHOD_PROBLEMS[problem_name]

    # Create dynamic problem class with forces as class attributes
    class_attrs = {
        "name": spec["name"],
        "description": spec["description"],
    }

    # Get forces dict and add as class attributes
    forces_dict = spec["forces"]
    class_attrs.update(forces_dict)

    # Create dynamic problem class
    ProblemClass = type(f"Problem_{problem_name}", (RectangularVectorProblem,), class_attrs)

    # Solve
    problem_instance = ProblemClass()
    solution = problem_instance.solve()

    # Find resultant for return value
    resultant = None
    for force in solution.values():
        if hasattr(force, 'is_resultant') and force.is_resultant:
            resultant = force
            break

    # Get component sums with all known forces (excluding resultant)
    known_forces = [f for f in solution.values() if f.is_known and not (hasattr(f, 'is_resultant') and f.is_resultant)]

    # Calculate component sums manually
    sum_x = 0.0
    sum_y = 0.0
    for force in known_forces:
        if force.x is not None and force.x.value is not None:
            sum_x += force.x.value
        if force.y is not None and force.y.value is not None:
            sum_y += force.y.value

    # Get solution steps from problem instance
    steps = problem_instance.solution_steps

    return {
        "forces": solution,
        "resultant": resultant,
        "sum_x": sum_x,
        "sum_y": sum_y,
        "steps": steps,
    }


def verify_component_results(solution, expected, debug_config, capsys, test_name):
    """Verify component method results match expected values and optionally print them."""
    print_results = debug_config.get("print_results", False)
    assert_values = debug_config.get("assert_values", True)

    forces_dict = solution["forces"]
    resultant = solution["resultant"]
    sum_x = solution["sum_x"]
    sum_y = solution["sum_y"]
    steps = solution["steps"]

    # Verify individual forces match expected (they should be unchanged)
    for force_name, expected_values in expected.items():
        if force_name not in forces_dict:
            if print_results:
                print(f"Warning: {force_name} not found in solution")
            continue

        force = forces_dict[force_name]

        # Detect if this is a component-only problem (has x/y keys) or magnitude/angle problem
        is_component_only = "x" in expected_values and "y" in expected_values

        if is_component_only:
            # Component-only verification (x/y format)
            expected_x = expected_values["x"]
            expected_y = expected_values["y"]

            # Get actual x and y components from the force
            comp_x, comp_y = force.get_components_in_system()

            # Extract values and convert from SI to preferred unit if needed
            if comp_x and force.magnitude.preferred:
                actual_x = comp_x.magnitude(force.magnitude.preferred)
            elif comp_x:
                actual_x = comp_x.value
            else:
                actual_x = 0.0

            if comp_y and force.magnitude.preferred:
                actual_y = comp_y.magnitude(force.magnitude.preferred)
            elif comp_y:
                actual_y = comp_y.value
            else:
                actual_y = 0.0

            # Only assert if enabled for this problem
            if assert_values:
                assert pytest.approx(expected_x, rel=0.01, abs=0.5) == actual_x, \
                    f"{force_name} x-component: got {actual_x}, expected {expected_x}"
                assert pytest.approx(expected_y, rel=0.01, abs=0.5) == actual_y, \
                    f"{force_name} y-component: got {actual_y}, expected {expected_y}"
        else:
            # Magnitude/angle verification (standard format)
            expected_mag = expected_values["magnitude"]
            expected_ang_deg = expected_values["angle"]
            expected_wrt = expected_values.get("wrt", "+x")

            # Use new API: magnitude_in() handles unit conversion automatically
            actual_mag_in_preferred = force.magnitude_in(force.magnitude.preferred) if force.magnitude.preferred else force.magnitude.value

            # Use new API: angle_in() handles both unit conversion and reference system transformation
            # Pass forces_dict to support force-relative references (e.g., "+F_R")
            actual_ang_in_wrt = force.angle_in("degree", wrt=expected_wrt, forces=forces_dict)

            # Normalize angles to [0, 360) range for comparison
            actual_ang_in_wrt = actual_ang_in_wrt % 360
            expected_ang_deg_normalized = expected_ang_deg % 360

            # Only assert if enabled for this problem
            if assert_values:
                assert pytest.approx(expected_mag, rel=0.01) == actual_mag_in_preferred, \
                    f"{force_name} magnitude: got {actual_mag_in_preferred}, expected {expected_mag}"
                assert pytest.approx(expected_ang_deg_normalized, rel=0.01) == actual_ang_in_wrt, \
                    f"{force_name} angle (wrt {expected_wrt}): got {actual_ang_in_wrt}°, expected {expected_ang_deg_normalized}°"

    # Get actual resultant values
    assert resultant.magnitude is not None and resultant.magnitude.value is not None
    assert resultant.angle is not None and resultant.angle.value is not None
    actual_magnitude = resultant.magnitude.value
    actual_angle = math.degrees(resultant.angle.value)

    # Determine unit for display (check first force)
    first_force = next(iter(forces_dict.values()))
    if first_force.magnitude.preferred:
        display_unit = first_force.magnitude.preferred.symbol
    else:
        display_unit = "N"

    # Use values as-is (already in SI units)
    sum_x_display = sum_x
    sum_y_display = sum_y
    actual_magnitude_display = actual_magnitude

    # Print results if enabled
    if print_results:
        with capsys.disabled():
            print(f"\n{test_name} results:")

            # Print individual forces
            for force_name in sorted(forces_dict.keys()):
                force = forces_dict[force_name]

                # Get expected format for this force (if specified)
                force_expected = expected.get(force_name, {})
                is_component_only = "x" in force_expected and "y" in force_expected

                if is_component_only:
                    # Display x/y components for component-only problems
                    comp_x, comp_y = force.get_components_in_system()

                    # Extract values and convert from SI to preferred unit if needed
                    if comp_x and force.magnitude.preferred:
                        actual_x = comp_x.magnitude(force.magnitude.preferred)
                        comp_unit = force.magnitude.preferred.symbol
                    elif comp_x:
                        actual_x = comp_x.value
                        comp_unit = "SI"
                    else:
                        actual_x = 0.0
                        comp_unit = "SI"

                    if comp_y and force.magnitude.preferred:
                        actual_y = comp_y.magnitude(force.magnitude.preferred)
                    elif comp_y:
                        actual_y = comp_y.value
                    else:
                        actual_y = 0.0

                    print(f"  {force_name}: x={actual_x:.1f} {comp_unit}, y={actual_y:.1f} {comp_unit}")
                else:
                    # Display magnitude/angle for standard problems
                    display_wrt = force_expected.get("wrt", "+x")

                    # Use new API for conversions (pass forces_dict for force-relative references)
                    actual_ang_in_wrt = force.angle_in("degree", wrt=display_wrt, forces=forces_dict) % 360

                    if force.magnitude.preferred:
                        mag_value_in_preferred = force.magnitude_in(force.magnitude.preferred)
                        mag_unit = force.magnitude.preferred.symbol
                    else:
                        mag_value_in_preferred = force.magnitude.value
                        mag_unit = "SI"

                    # Format wrt for display
                    wrt_display = f" wrt {display_wrt}" if display_wrt != "+x" else ""
                    print(f"  {force_name}: magnitude={mag_value_in_preferred:.3f} {mag_unit}, angle={actual_ang_in_wrt:.3f}°{wrt_display}")

            # Detect if this is a component-only problem (check if any expected value has x/y format)
            is_component_only_problem = any("x" in exp_vals and "y" in exp_vals for exp_vals in expected.values())

            # Print component sums and resultant only for resultant problems
            if not is_component_only_problem:
                print("\n  Component Method Results:")
                print(f"    SigmaFx = {sum_x_display:.3f} {display_unit}")
                print(f"    SigmaFy = {sum_y_display:.3f} {display_unit}")
                print(f"    FR = {actual_magnitude_display:.3f} {display_unit}")
                print(f"    theta = {actual_angle:.2f}deg")

            if steps:
                print("\n  Solution steps:")
                for step in steps:
                    print(f"    {step}")

            # Show assertion status
            if not assert_values:
                print(f"  [NOTE: Assertions disabled for {test_name}]")


# Single parameterized test for all component method problems
@pytest.mark.parametrize("problem_name", list(COMPONENT_METHOD_PROBLEMS.keys()))
def test_component_method_problem(problem_name, capsys):
    """Test all component method problems."""
    problem_spec = COMPONENT_METHOD_PROBLEMS[problem_name]
    solution = solve_component_problem(problem_name)
    expected = problem_spec["expected"]
    debug_config = problem_spec.get("debug", {"print_results": False, "assert_values": True})
    verify_component_results(solution, expected, debug_config, capsys, problem_name)


# Example of how easy it is to add a new problem:
#
# COMPONENT_METHOD_PROBLEMS["problem_2_42"] = {
#     "name": "Problem 2-42",
#     "description": "New problem description...",
#     "forces": {
#         "F_1": ForceVector(
#             magnitude=100, unit="N",
#             angle=30, wrt="+x",
#             name="F_1", description="Force 1"
#         ),
#         "F_2": ForceVector(
#             magnitude=200, unit="N",
#             angle=120, wrt="+x",
#             name="F_2", description="Force 2"
#         ),
#     },
#     "expected": {
#         "F_1": {"magnitude": 100, "angle": 30, "unit": "N", "wrt": "+x"},
#         "F_2": {"magnitude": 200, "angle": 120, "unit": "N", "wrt": "+x"},
#     },
#     "debug": {"print_results": False, "assert_values": True},
# }
# That's it! The test will automatically pick up the new problem.
