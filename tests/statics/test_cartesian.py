"""
Comprehensive tests for 3D Cartesian vector problems using problems 2-60 to 2-85 from textbook.

These tests validate the 3D vector operations including:
- Coordinate direction angles (α, β, γ)
- Direction cosines (cos α, cos β, cos γ)
- Transverse and azimuth angles (φ, θ)
- 3D component resolution and resultant calculation
"""

import math

import pytest

from qnty.problems.cartesian_vector import CartesianVectorProblem
from qnty.spatial import ForceVector

# Problem definitions - single source of truth
CARTESIAN_3D_PROBLEMS = {
    "problem_2_60": {
        "name": "Problem 2-60",
        "description": """
        The force F has a magnitude of 80 lb and acts within the octant shown. Determine the magnitudes of the x, y, z components of F.
        """,
        "forces": {
            "F": ForceVector(
                magnitude=80,
                unit="lbf",
                alpha=60,
                beta=45,
                name="F",
                description="Force F",
            ),
        },
        "expected": {
            "F": {
                "magnitude": 80,
                "unit": "lbf",
                "x": 40.0,
                "y": 56.6,
                "z": 40.0,  # Components
                "alpha": 60.0,
                "beta": 45.0,
                "gamma": 60.0,  # Direction angles
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_61": {
        "name": "Problem 2-61",
        "description": """
        The bolt is subjected to the force F, which has components acting along the x, y, z axes as shown. If the magnitude of F is 80 N, and and determine the magnitudes of its components.
        """,
        "forces": {
            "F": ForceVector(
                magnitude=80,
                alpha=-60,
                gamma=45,
                unit="N",
                name="F",
                description="Force F",
            ),
        },
        "expected": {
            "F": {
                "magnitude": 80,
                "unit": "N",
                "x": 40.0,
                "y": -40.0,
                "z": 56.6,  # Actual signed components
                "alpha": 60.0,
                "beta": 120.0,
                "gamma": 45.0,  # Direction angles
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_62": {
        "name": "Problem 2-62",
        "description": """
        Determine the magnitude and coordinate direction angles of the force F acting on the support. The component of F in the x-y plane is 7 kN.
        """,
        "forces": {
            "F": ForceVector(
                magnitude=8083,  # 7 kN / sin(60°) = 8.083 kN
                phi=60,  # Angle from +z axis (90° - 30° elevation)
                theta=-40,  # Azimuth angle in x-y plane (negative for -y component)
                unit="N",
                name="F",
                description="Force F",
            ),
        },
        "expected": {
            "F": {
                "magnitude": 8083,
                "unit": "N",
                "x": 5362.4,  # F * sin(60°) * cos(-40°) = 8083 * 0.866 * 0.766 = 5361
                "y": -4499.6,  # F * sin(60°) * sin(-40°) = 8083 * 0.866 * (-0.643) = -4502
                "z": 4042,  # F * cos(60°) = 8083 * 0.5 = 4041.5
                "alpha": 48.4,  # arccos(5361/8083)
                "beta": 124,  # arccos(-4502/8083)
                "gamma": 60.0,  # arccos(4042/8083)
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_63": {
        "name": "Problem 2-63",
        "description": """
        Determine the magnitude and coordinate direction angles of the resultant force.
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=80,
                unit="lbf",
                phi=60,
                theta=-40,  # φ from +z axis down, θ in x-y plane (negative = clockwise from +x)
                name="F_1",
                description="Force F1",
            ),
            "F_2": ForceVector(
                x=0, y=0, z=-130, unit="lbf", name="F_2", description="Force F2"),
            "F_R": ForceVector.unknown(name="F_R", is_resultant=True, description="Resultant Force"),
        },
        "expected": {
            "F_1": {
                "magnitude": 80,
                "unit": "lbf",
                "x": 53.1,
                "y": -44.5,
                "z": 40.0,  # From textbook solution
            },
            "F_2": {
                "x": 0,
                "y": 0,
                "z": -130,
            },
            "F_R": {
                "magnitude": 114,
                "unit": "lbf",  # Actually 113.6
                "x": 53.1,
                "y": -44.5,
                "z": -90.0,
                "alpha": 62.1,
                "beta": 113.0,
                "gamma": 142.0,  # Direction angles
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_64": {
        "name": "Problem 2-64",
        "description": """
        Specify the coordinate direction angles of and and express each force as a Cartesian vector.
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=80,
                unit="lbf",
                phi=60,
                theta=-40,  # φ from +z axis down, θ in x-y plane (negative = clockwise from +x)
                name="F_1",
                description="Force F1",
            ),
            "F_2": ForceVector(
                x=0, y=0, z=-130, unit="lbf", name="F_2", description="Force F2"),
        },
        "expected": {
            "F_1": {
                "magnitude": 80,
                "unit": "lbf",
                "x": 53.1,
                "y": -44.5,
                "z": 40.0,  # From textbook solution
                "alpha": 48.2,
                "beta": 124.0,
                "gamma": 60.0,  # Direction angles
            },
            "F_2": {
                "magnitude": 130,
                "unit": "lbf",
                "x": 0,
                "y": 0,
                "z": -130,
                "alpha": 90.0,
                "beta": 90.0,
                "gamma": 180.0,  # Direction angles
            },
        },
        "debug": {
            "print_results": True,
            "assert_values": True
        },
    },
    "problem_2_65": {
        "name": "Problem 2-65",
        "description": """
        The screw eye is subjected to the two forces shown. Express each force in Cartesian vector form and then determine the resultant force. Find the magnitude and coordinate direction angles of the resultant force.
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=300,
                unit="N",
                theta=135,
                phi=30,  # Given in problem
                name="F_1",
                description="Force F1",
            ),
            "F_2": ForceVector(
                magnitude=500,
                unit="N",
                alpha=60,
                beta=45,
                gamma=120,  # Given in problem
                name="F_2",
                description="Force F2",
            ),
            "F_R": ForceVector.unknown(name="F_R", is_resultant=True, description="Resultant Force"),
        },
        "expected": {
            "F_1": {
                "magnitude": 300,
                "unit": "N",
                "x": -106.0,
                "y": 106.0,
                "z": 260.0,  # Rounded
            },
            "F_2": {
                "magnitude": 500,
                "unit": "N",
                "x": 250.0,
                "y": 353.6,
                "z": -250.0,
            },
            "F_R": {
                "magnitude": 482,
                "unit": "N",  # Actually 481.73
                "x": 144.0,
                "y": 460.0,
                "z": 9.81,
                "alpha": 72.6,
                "beta": 17.4,
                "gamma": 88.8,  # Direction angles
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_66": {
        "name": "Problem 2-66",
        "description": """
        Determine the coordinate direction angles of F1.
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=300,
                unit="N",
                theta=135,
                phi=30,  # Given in problem
                name="F_1",
                description="Force F1",
            ),
        },
        "expected": {
            "F_1": {
                "magnitude": 300,
                "unit": "N",
                "x": -106.0,
                "y": 106.0,
                "z": 260.0,
                "alpha": 111,
                "beta": 69.3,
                "gamma": 30,  # Direction angles
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_67": {
        "name": "Problem 2-67",
        "description": """
        Determine the magnitude and coordinate direction angles of F3 so that the resultant of the three forces acts along the positive y axis and has a magnitude of 600 lb.
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=180,
                unit="lbf",
                angle=0,
                wrt="-x",
                name="F_1",
                description="Force F1",
            ),
            "F_2": ForceVector(
                magnitude=300,
                unit="lbf",
                theta=50,
                phi=120,  # 120° from +z axis gives negative z component
                name="F_2",
                description="Force F2",
            ),
            "F_3": ForceVector.unknown(name="F_3", description="Force F3"),
            "F_R": ForceVector(
                magnitude=600,
                unit="lbf",
                angle=0,
                wrt="+y",
                name="F_R", is_resultant=True, description="Resultant Force"),
        },
        "expected": {
            "F_1": {
                "magnitude": 180,
                "unit": "lbf",
                "angle": 0,
                "wrt": "-x",
                "x": -180.0,
                "y": 0.0,
                "z": 0.0,
            },
            "F_2": {
                "magnitude": 300,
                "unit": "lbf",
                "theta": 50, # from +x axis
                "phi": 120, # from +z axis
                "x": 167,
                "y": 199,
                "z": -150,
            },
            "F_3": {
                "magnitude": 428, # correct value is 428
                "unit": "lbf",
                "alpha": 88.3,
                "beta": 20.6,
                "gamma": 69.5,  # Direction angles
            },
            "F_R": {
                "magnitude": 600,
                "unit": "lbf",
                "angle": 0,
                "wrt": "+y",
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_68": {
        "name": "Problem 2-68",
        "description": """
        Determine the magnitude and coordinate direction angles of F3 so that the resultant of the three forces is zero.
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=180,
                unit="lbf",
                angle=0,
                wrt="-x",
                name="F_1",
                description="Force F1",
            ),
            "F_2": ForceVector(
                magnitude=300,
                unit="lbf",
                theta=50,
                phi=120,  # 120° from +z axis gives negative z component
                name="F_2",
                description="Force F2",
            ),
            "F_3": ForceVector.unknown(name="F_3", description="Force F3"),
            "F_R": ForceVector(
                magnitude=0,
                unit="lbf",
                angle=0,
                wrt="+y",
                name="F_R", is_resultant=True, description="Resultant Force"),
        },
        "expected": {
            "F_1": {
                "magnitude": 180,
                "unit": "lbf",
                "angle": 0,
                "wrt": "-x",
                "x": -180.0,
                "y": 0.0,
                "z": 0.0,
            },
            "F_2": {
                "magnitude": 300,
                "unit": "lbf",
                "theta": 50, # from +x axis
                "phi": 120, # from +z axis
                "x": 167,
                "y": 199,
                "z": -150,
            },
            "F_3": {
                "magnitude": 250, # correct value is 428
                "unit": "lbf",
                "alpha": 87,
                "beta": 143,
                "gamma": 53.1,  # Direction angles
            },
            "F_R": {
                "magnitude": 0,
                "unit": "lbf",
                "angle": 0,
                "wrt": "+y",
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_69": {
        "name": "Problem 2-69",
        "description": """
        Determine the magnitude and coordinate direction angles of the resultant force, and sketch this vector on the coordinate system.
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=400,
                unit="N",
                alpha=45,
                beta=60,
                gamma=120,
                name="F_1",
                description="Force F1",
            ),
            "F_2": ForceVector(
                magnitude=125,
                unit="N",
                theta=-20,
                phi=53.13,
                name="F_2",
                description="Force F2",
            ),
            "F_R": ForceVector.unknown(name="F_R", is_resultant=True, description="Resultant Force"),
        },
        "expected": {
            "F_1": {
                "magnitude": 400,
                "unit": "N",
                "alpha": 45,
                "beta": 60,
                "gamma": 120,
            },
            "F_2": {
                "magnitude": 125,
                "unit": "N",
                "theta": -20,
                "phi": 53.13,
            },
            "F_R": {
                "magnitude": 430,
                "unit": "N",  # Actually 481.73
                "alpha": 28.9,
                "beta": 67.3,
                "gamma": 107,  # Direction angles
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_70": {
        "name": "Problem 2-70",
        "description": """
        Determine the magnitude and coordinate direction angles of the resultant force, and sketch this vector on the coordinate system.
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=450,
                unit="N",
                theta=90,
                phi=143.13,  # Given in problem
                name="F_1",
                description="Force F1",
            ),
            "F_2": ForceVector(
                magnitude=525,
                unit="N",
                alpha=45,
                beta=120,
                gamma=60,  # Given in problem
                name="F_2",
                description="Force F2",
            ),
            "F_R": ForceVector.unknown(name="F_R", is_resultant=True, description="Resultant Force"),
        },
        "expected": {
            "F_1": {
                "magnitude": 450,
                "unit": "N",
                "theta": 90,
                "phi": 143.13,
            },
            "F_2": {
                "magnitude": 525,
                "unit": "N",
                "alpha": 45,
                "beta": 120,
                "gamma": 60,
            },
            "F_R": {
                "magnitude": 384,
                "unit": "N",  # Actually 481.73
                "alpha": 14.8,
                "beta": 88.9,
                "gamma": 105,  # Direction angles
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_71": {
        "name": "Problem 2-71",
        "description": """
        Specify the magnitude and coordinate direction angles a1, , of so that the resultant of the three forces acting on the bracket is Note that lies in the x–y plane.
        """,
        "forces": {
            "F_1": ForceVector.unknown(
                unit="lbf",
                name="F_1",
                description="Force F1",
            ),
            "F_2": ForceVector(
                magnitude=200,
                unit="lbf",
                angle=0,
                wrt="-y",
                name="F_2",
                description="Force F2",
            ),
            "F_3": ForceVector(
                magnitude=400,
                unit="lbf",
                angle=30,
                wrt="+y",
                name="F_3",
                description="Force F3",
            ),
            "F_R": ForceVector(
                x=0, y=0, z=-350,
                unit="lbf",
                name="F_R", is_resultant=True, description="Resultant Force"
            ),
        },
        "expected": {
            "F_1": {
                "magnitude": 429,
                "unit": "lbf",
                "alpha": 62.2,
                "beta": 110,
                "gamma": 145,  # Direction angles

            },
            "F_2": {
                "magnitude": 200,
                "unit": "lbf",
                "angle": 30,
                "wrt": "+y",
            },
            "F_3": {
                "magnitude": 400,
                "unit": "lbf",
                "angle": 0,
                "wrt": "-y",
            },
            "F_R": {
                "magnitude": 350,
                "unit": "lbf",  # Actually 481.73
                "x": 0,
                "y": 0,
                "z": -350,
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_72": {
        "name": "Problem 2-72",
        "description": """
        Two forces F1 and F2 act on the screw eye. If the resultant force FR has a magnitude of 150 lb and the coordinate direction angles shown, determine the magnitude of F2 and its coordinate direction angles.
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=80,
                unit="lbf",
                angle=0,
                wrt="+y",
                name="F_1",
                description="Force F1",
            ),
            "F_2": ForceVector.unknown(
                unit="lbf",
                name="F_2",
                description="Force F2",
            ),
            "F_R": ForceVector(
                magnitude=150,
                alpha=120,
                beta=50,
                unit="lbf",
                name="F_R", is_resultant=True, description="Resultant Force"),
        },
        "expected": {
            "F_1": {
                "magnitude": 80,
                "unit": "lbf",
                "x": 0,
                "y": 80.0,
                "z": 0,  # Rounded
            },
            "F_2": {
                "magnitude": 116,
                "unit": "lbf",
                "alpha": 130,
                "beta": 81.9,
                "gamma": 41.4,
            },
            "F_R": {
                "magnitude": 150,
                "unit": "lbf",  # Actually 481.73
                "alpha": 120,
                "beta": 50,
                "gamma": 54.52,  # Direction angles
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_73": {
        "name": "Problem 2-73",
        "description": """
        Express each force in Cartesian vector form.
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=90,
                unit="N",
                theta=0,
                phi=53.13,  # Given in problem
                name="F_1",
                description="Force F1",
            ),
            "F_2": ForceVector(
                magnitude=150,
                unit="N",
                theta=45,
                phi=30,
                name="F_2",
                description="Force F2",
            ),
            "F_3": ForceVector(
                magnitude=200,
                unit="N",
                theta=0,
                phi=0,
                name="F_3",
                description="Force F3",
            ),
        },
        "expected": {
            "F_1": {
                "magnitude": 90,
                "unit": "N",
                "x": 72,
                "y": 0,
                "z": 54,  # Rounded
            },
            "F_2": {
                "magnitude": 150,
                "unit": "N",
                "x": 53,
                "y": 53,
                "z": 130,
            },
            "F_3": {
                "magnitude": 200,
                "unit": "N",  # Actually 481.73
                "x": 0,
                "y": 0,
                "z": 200,
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_74": {
        "name": "Problem 2-74",
        "description": """
        Determine the magnitude and coordinate direction angles of the resultant force, and sketch this vector on the coordinate system.
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=90,
                unit="N",
                theta=0,
                phi=53.13,  # Given in problem
                name="F_1",
                description="Force F1",
            ),
            "F_2": ForceVector(
                magnitude=150,
                unit="N",
                theta=45,
                phi=30,
                name="F_2",
                description="Force F2",
            ),
            "F_3": ForceVector(
                magnitude=200,
                unit="N",
                theta=0,
                phi=0,
                name="F_3",
                description="Force F3",
            ),
            "F_R": ForceVector.unknown(name="F_R", is_resultant=True, description="Resultant Force"),
        },
        "expected": {
            "F_1": {
                "magnitude": 90,
                "unit": "N",
                "x": 72,
                "y": 0,
                "z": 54,  # Rounded
            },
            "F_2": {
                "magnitude": 150,
                "unit": "N",
                "x": 53,
                "y": 53,
                "z": 130,
            },
            "F_3": {
                "magnitude": 200,
                "unit": "N",  # Actually 481.73
                "x": 0,
                "y": 0,
                "z": 200,
            },
            "F_R": {
                "magnitude": 407,
                "unit": "N",
                "alpha": 72.1,
                "beta": 82.5,
                "gamma": 19.5,  # Direction angles
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_75": {
        "name": "Problem 2-75",
        "description": """
        The spur gear is subjected to the two forces caused by contact with other gears. Express each force as a Cartesian vector.
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=50,
                unit="lbf",
                theta=90,
                phi=163.74,  # Given in problem
                name="F_1",
                description="Force F1",
            ),
            "F_2": ForceVector(
                magnitude=180,
                unit="lbf",
                alpha=60,
                beta=135,
                gamma=60,  # Given in problem
                name="F_2",
                description="Force F2",
            ),
        },
        "expected": {
            "F_1": {
                "magnitude": 50,
                "unit": "lbf",
                "x": 0,
                "y": 14,
                "z": -48,  # Rounded
            },
            "F_2": {
                "magnitude": 180,
                "unit": "lbf",
                "x": 90.0,
                "y": -127,
                "z": 90,
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_76": {
        "name": "Problem 2-76",
        "description": """
        The spur gear is subjected to the two forces caused by contact with other gears. Express each force as a Cartesian vector.
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=50,
                unit="lbf",
                theta=90,
                phi=163.74,  # Given in problem
                name="F_1",
                description="Force F1",
            ),
            "F_2": ForceVector(
                magnitude=180,
                unit="lbf",
                alpha=60,
                beta=135,
                gamma=60,  # Given in problem
                name="F_2",
                description="Force F2",
            ),
            "F_R": ForceVector.unknown(name="F_R", is_resultant=True, description="Resultant Force"),
        },
        "expected": {
            "F_1": {
                "magnitude": 50,
                "unit": "lbf",
                "x": 0,
                "y": 14,
                "z": -48,  # Rounded
            },
            "F_2": {
                "magnitude": 180,
                "unit": "lbf",
                "x": 90.0,
                "y": -127,
                "z": 90,
            },
            "F_R": {
                "unit": "lbf",
                "x": 90.0,
                "y": -113,
                "z": 42,  # Rounded
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_77": {
        "name": "Problem 2-77",
        "description": """
        Determine the magnitude and coordinate direction angles of the resultant force, and sketch this vector on the coordinate system.
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=400,
                unit="N",
                theta=-20,
                phi=60,  # Given in problem
                name="F_1",
                description="Force F1",
            ),
            "F_2": ForceVector(
                magnitude=500,
                unit="N",
                alpha=60,
                beta=60,
                gamma=135,  # Given in problem
                name="F_2",
                description="Force F2",
            ),
            "F_R": ForceVector.unknown(name="F_R", is_resultant=True, description="Resultant Force"),
        },
        "expected": {
            "F_1": {
                "magnitude": 400,
                "unit": "N",
                "theta": -20,
                "phi": 60,
            },
            "F_2": {
                "magnitude": 500,
                "unit": "N",
                "alpha": 60,
                "beta": 60,
                "gamma": 135,
            },
            "F_R": {
                "magnitude": 610,
                "unit": "N",  # Actually 481.73
                "alpha": 19.4,
                "beta": 77.5,
                "gamma": 105,  # Direction angles
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_78": {
        "name": "Problem 2-78",
        "description": """
        The two forces F1 and F2 acting at A have a resultant force of FR = 5 - 100k6 lb. Determine the magnitude and coordinate direction angles of F2.
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=60,
                unit="lbf",
                theta=150,
                phi=140,  # Given in problem
                name="F_1",
                description="Force F1",
            ),
            "F_2": ForceVector.unknown(
                unit="lbf",
                name="F_2",
                description="Force F2",
            ),
            "F_R": ForceVector(
                unit="lbf",
                x=0,
                y=0,
                z=-100,
                name="F_R", is_resultant=True, description="Resultant Force"),
        },
        "expected": {
            "F_1": {
                "magnitude": 60,
                "unit": "lbf",
                "theta": 150,
                "phi": 140,
            },
            "F_2": {
                "magnitude": 66.4,
                "unit": "lbf",
                "alpha": 59.8,
                "beta": 107,
                "gamma": 144,
            },
            "F_R": {
                "magnitude": 100,
                "unit": "lbf",
                "x": 0.0,
                "y": 0.0,
                "z": -100,
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_79": {
        "name": "Problem 2-79",
        "description": """
        Determine the coordinate direction angles of the force F1 and indicate them on the figure.
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=60,
                unit="lbf",
                theta=150,
                phi=140,  # Given in problem
                name="F_1",
                description="Force F1",
            ),
        },
        "expected": {
            "F_1": {
                "magnitude": 60,
                "unit": "lbf",
                "alpha": 124,
                "beta": 71.3,
                "gamma": 140,
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_80": {
        "name": "Problem 2-80",
        "description": """
        The bracket is subjected to the two forces shown. Express each force in Cartesian vector form and then determine the resultant force Find the magnitude and coordinate direction angles of the resultant force.
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=250,
                unit="N",
                theta=65,
                phi=125,  # Given in problem
                name="F_1",
                description="Force F1",
            ),
            "F_2": ForceVector(
                magnitude=400,
                unit="N",
                alpha=120,
                beta=45,
                gamma=60,  # Given in problem
                name="F_2",
                description="Force F2",
            ),
            "F_R": ForceVector.unknown(name="F_R", is_resultant=True, description="Resultant Force"),
        },
        "expected": {
            "F_1": {
                "magnitude": 250,
                "unit": "N",
                "x": 86.5,
                "y": 186,
                "z": -143,  # Rounded
            },
            "F_2": {
                "magnitude": 400,
                "unit": "N",
                "x": -200,
                "y": 283,
                "z": 200,
            },
            "F_R": {
                "magnitude": 485,
                "unit": "N",  # Actually 481.73
                "x": -113,
                "y": 468,
                "z": 56.6,
                "alpha": 104,
                "beta": 15.1,
                "gamma": 83.3,  # Direction angles
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_81": {
        "name": "Problem 2-81",
        "description": """
        If the coordinate direction angles for are , and , determine the magnitude and coordinate direction angles of the resultant force acting on the eyebolt.  b3 = 60°
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=700,
                unit="lbf",
                theta=30,
                phi=90,  # Given in problem
                name="F_1",
                description="Force F1",
            ),
            "F_2": ForceVector(
                magnitude=600,
                unit="lbf",
                theta=90,
                phi=53.13,  # Given in problem
                name="F_2",
                description="Force F2",
            ),
            "F_3": ForceVector(
                magnitude=800,
                unit="lbf",
                alpha=120,
                beta=60,
                gamma=45,  # Given in problem
                name="F_3",
                description="Force F3",
            ),
            "F_R": ForceVector.unknown(name="F_R", is_resultant=True, description="Resultant Force"),
        },
        "expected": {
            "F_1": {
                "magnitude": 700,
                "unit": "lbf",
                "theta": 30,
                "phi": 90,
            },
            "F_2": {
                "magnitude": 600,
                "unit": "lbf",
                "theta": 90,
                "phi": 53.13,
            },
            "F_3": {
                "magnitude": 800,
                "unit": "lbf",
                "alpha": 120,
                "beta": 60,
                "gamma": 45,
            },
            "F_R": {
                "magnitude": 1553.16,
                "unit": "lbf",  # Actually 481.73
                "alpha": 82.4,
                "beta": 37.6,
                "gamma": 53.4,  # Direction angles
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_82": {
        "name": "Problem 2-82",
        "description": """
        If the coordinate direction angles for are , and , determine the magnitude and coordinate direction angles of the resultant force acting on the eyebolt.  b3 = 45°
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=700,
                unit="lbf",
                theta=30,
                phi=90,  # Given in problem
                name="F_1",
                description="Force F1",
            ),
            "F_2": ForceVector(
                magnitude=600,
                unit="lbf",
                theta=90,
                phi=53.13,  # Given in problem
                name="F_2",
                description="Force F2",
            ),
            "F_3": ForceVector(
                magnitude=800,
                unit="lbf",
                alpha=120,
                beta=45,
                gamma=60,  # Given in problem
                name="F_3",
                description="Force F3",
            ),
            "F_R": ForceVector.unknown(name="F_R", is_resultant=True, description="Resultant Force"),
        },
        "expected": {
            "F_1": {
                "magnitude": 700,
                "unit": "lbf",
                "theta": 30,
                "phi": 90,
            },
            "F_2": {
                "magnitude": 600,
                "unit": "lbf",
                "theta": 90,
                "phi": 53.13,
            },
            "F_3": {
                "magnitude": 800,
                "unit": "lbf",
                "alpha": 120,
                "beta": 45,
                "gamma": 60,
            },
            "F_R": {
                "magnitude": 1602.52,
                "unit": "lbf",  # Actually 481.73
                "alpha": 82.6,
                "beta": 29.4,
                "gamma": 61.7,  # Direction angles
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    # TODO: Problem 2-83 has two possible solutions
    # "problem_2_83": {
    #     "name": "Problem 2-83",
    #     "description": """
    #     If the direction of the resultant force acting on the eyebolt is defined by the unit vector , determine the coordinate direction angles of and the magnitude of FR.
    #     """,
    #     "forces": {
    #         "F_1": ForceVector(
    #             magnitude=700,
    #             unit="lbf",
    #             theta=30,
    #             phi=90,  # Given in problem
    #             name="F_1",
    #             description="Force F1",
    #         ),
    #         "F_2": ForceVector(
    #             magnitude=600,
    #             unit="lbf",
    #             theta=90,
    #             phi=53.13,  # Given in problem
    #             name="F_2",
    #             description="Force F2",
    #         ),
    #         "F_3": ForceVector.unknown(
    #             magnitude=800,
    #             unit="lbf",
    #             name="F_3",
    #             description="Force F3",
    #         ),
    #         "F_R": ForceVector.unknown(
    #             theta=90,
    #             phi=60,
    #             name="F_R", is_resultant=True, description="Resultant Force"),
    #     },
    #     "expected": {
    #         "F_1": {
    #             "magnitude": 700,
    #             "unit": "lbf",
    #             "theta": 30,
    #             "phi": 90,
    #         },
    #         "F_2": {
    #             "magnitude": 600,
    #             "unit": "lbf",
    #             "theta": 90,
    #             "phi": 53.13,
    #         },
    #         "F_3": {
    #             "magnitude": 800,
    #             "unit": "lbf",
    #             "alpha": 139,
    #             "beta": 45,
    #             "gamma": 60,
    #         },
    #         "F_R": {
    #             "magnitude": 1602.52,
    #             "unit": "lbf",  # Actually 481.73
    #             "alpha": 82.6,
    #             "beta": 29.4,
    #             "gamma": 61.7,  # Direction angles
    #         },
    #     },
    #     "debug": {
    #         "print_results": False,
    #         "assert_values": True
    #     },
    # },
    "problem_2_84": {
        "name": "Problem 2-84",
        "description": """
        The pole is subjected to the force F, which has components acting along the x, y, z axes as shown. If the magnitude of F is 3 kN, , and , determine the magnitudes of its three components.
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=3000,
                unit="N",
                beta=30,
                gamma=75,  # Given in problem
                name="F_1",
                description="Force F1",
            ),
        },
        "expected": {
            "F_1": {
                "magnitude": 3000,
                "unit": "N",
                "x": 1283,
                "y": 2598,
                "z": 776,  # Rounded
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    # TODO: ValueError: magnitude must be specified when using coordinate direction angles
    # "problem_2_85": {
    #     "name": "Problem 2-85",
    #     "description": """
    #     The pole is subjected to the force F which has components and . If , determine the magnitudes of F and Fy.  Fx = 1.5 kN
    #     """,
    #     "forces": {
    #         "F_1": ForceVector(
    #             unit="N",
    #             x=1500,
    #             z=1250,
    #             beta=75,
    #             name="F_1",
    #             description="Force F1",
    #         ),
    #     },
    #     "expected": {
    #         "F_1": {
    #             "magnitude": 2020,
    #             "unit": "N",
    #             "x": 1500,
    #             "y": 523,
    #             "z": 1250,  # Rounded
    #         },
    #     },
    #     "debug": {
    #         "print_results": False,
    #         "assert_values": True
    #     },
    # },
}


def assert_force_magnitude(force: ForceVector, expected_mag: float, expected_unit: str, tolerance: float = 0.5):
    """Assert force magnitude matches expected value in the expected unit."""
    assert force.magnitude is not None, f"Force {force.name} magnitude is None"
    assert force.magnitude.value is not None, f"Force {force.name} magnitude value is None"

    # Validate that the force's preferred unit matches the expected unit (compare by symbol or name)
    if force.magnitude.preferred:
        actual_unit_symbol = force.magnitude.preferred.symbol
        actual_unit_name = force.magnitude.preferred.name
        # Allow matching by either symbol (e.g., "lbf") or name (e.g., "pound_force")
        unit_matches = (actual_unit_symbol == expected_unit) or (actual_unit_name == expected_unit)
        assert unit_matches, f"Force {force.name} unit mismatch: expected '{expected_unit}', got '{actual_unit_symbol}' (name: '{actual_unit_name}')"

    # Use new API: magnitude_in() handles unit conversion automatically
    actual_mag = force.magnitude_in(force.magnitude.preferred) if force.magnitude.preferred else force.magnitude.value

    assert abs(actual_mag - expected_mag) < tolerance, f"Force {force.name} magnitude: expected {expected_mag} {expected_unit}, got {actual_mag:.3f} {expected_unit}"


def assert_force_component(component: float | None, expected: float, comp_name: str, force_name: str, expected_unit: str, tolerance: float = 0.5):
    """Assert force component matches expected value in the expected unit."""
    assert component is not None, f"Force {force_name} component {comp_name} is None"
    assert abs(component - expected) < tolerance, f"Force {force_name} {comp_name}: expected {expected} {expected_unit}, got {component:.3f} {expected_unit}"


def assert_direction_angle(angle_qty, expected_deg: float, angle_name: str, force_name: str, tolerance: float = 0.5):
    """Assert direction angle matches expected value in degrees."""
    assert angle_qty is not None, f"Force {force_name} angle {angle_name} is None"
    assert angle_qty.value is not None, f"Force {force_name} angle {angle_name} value is None"

    # Convert to degrees for comparison
    actual_deg = math.degrees(angle_qty.value)

    assert abs(actual_deg - expected_deg) < tolerance, f"Force {force_name} {angle_name}: expected {expected_deg}°, got {actual_deg:.1f}°"


@pytest.mark.parametrize("problem_key", list(CARTESIAN_3D_PROBLEMS.keys()))
def test_cartesian_3d_problem(problem_key):
    """Test 3D Cartesian vector problems."""
    spec = CARTESIAN_3D_PROBLEMS[problem_key]

    if spec["debug"]["print_results"]:
        print(f"\n{'=' * 80}")
        print(f"Testing: {spec['name']}")
        print(f"{'=' * 80}")
        print(spec["description"])

    # Extract forces and expected values
    forces_dict = spec["forces"]
    expected = spec["expected"]

    # Create dynamic problem class with forces as class attributes
    class_attrs = {
        "name": spec["name"],
        "description": spec["description"],
    }

    # Add forces as class attributes
    class_attrs.update(forces_dict)

    # Create dynamic problem class
    ProblemClass = type(f"Problem_{problem_key}", (CartesianVectorProblem,), class_attrs)

    # Create problem instance
    problem = ProblemClass()

    # Check if this problem requires solving (has any unknown forces)
    has_unknowns = any(not f.is_known for f in forces_dict.values())

    if has_unknowns:
        # Solve for unknown forces (could be resultant or individual forces)
        result = problem.solve()

        if spec["debug"]["print_results"]:
            print("\n--- Solution Steps ---")
            for step in problem.solution_steps:
                if "description" in step:
                    print(f"\n{step['description']}")
                if "equations" in step:
                    for eq in step["equations"]:
                        print(f"  {eq}")
                if "components" in step:
                    for comp in step["components"]:
                        print(f"  {comp}")

        # Verify results
        if spec["debug"]["assert_values"]:
            for force_name, expected_values in expected.items():
                solved_force = result[force_name]
                expected_unit = expected_values.get("unit", "N")

                if spec["debug"]["print_results"]:
                    print(f"\n--- Verification: {force_name} ---")

                # Check magnitude if specified
                if "magnitude" in expected_values:
                    assert_force_magnitude(solved_force, expected_values["magnitude"], expected_unit)
                    if spec["debug"]["print_results"]:
                        mag_val = (solved_force.magnitude_in(solved_force.magnitude.preferred)
                                   if solved_force.magnitude and solved_force.magnitude.preferred
                                   else solved_force.magnitude.value if solved_force.magnitude else 0.0)
                        print(f"  Magnitude: {mag_val:.3f} {expected_unit} ✓")

                # Check components if specified
                if "x" in expected_values:
                    assert solved_force.x is not None and solved_force.x.value is not None and solved_force.x.preferred is not None
                    x_val = solved_force.x.value / solved_force.x.preferred.si_factor
                    assert_force_component(x_val, expected_values["x"], "x", force_name, expected_unit)
                    if spec["debug"]["print_results"]:
                        print(f"  Fx: {x_val:.3f} {expected_unit} ✓")

                if "y" in expected_values:
                    assert solved_force.y is not None and solved_force.y.value is not None and solved_force.y.preferred is not None
                    y_val = solved_force.y.value / solved_force.y.preferred.si_factor
                    assert_force_component(y_val, expected_values["y"], "y", force_name, expected_unit)
                    if spec["debug"]["print_results"]:
                        print(f"  Fy: {y_val:.3f} {expected_unit} ✓")

                if "z" in expected_values:
                    assert solved_force.z is not None and solved_force.z.value is not None and solved_force.z.preferred is not None
                    z_val = solved_force.z.value / solved_force.z.preferred.si_factor
                    assert_force_component(z_val, expected_values["z"], "z", force_name, expected_unit)
                    if spec["debug"]["print_results"]:
                        print(f"  Fz: {z_val:.3f} {expected_unit} ✓")

                # Check direction angles if specified
                if "alpha" in expected_values:
                    assert_direction_angle(solved_force.alpha, expected_values["alpha"], "α", force_name, tolerance=1.0)
                    if spec["debug"]["print_results"] and solved_force.alpha and solved_force.alpha.value is not None:
                        print(f"  α: {math.degrees(solved_force.alpha.value):.1f}° ✓")

                if "beta" in expected_values:
                    assert_direction_angle(solved_force.beta, expected_values["beta"], "β", force_name, tolerance=1.0)
                    if spec["debug"]["print_results"] and solved_force.beta and solved_force.beta.value is not None:
                        print(f"  β: {math.degrees(solved_force.beta.value):.1f}° ✓")

                if "gamma" in expected_values:
                    assert_direction_angle(solved_force.gamma, expected_values["gamma"], "γ", force_name, tolerance=1.0)
                    if spec["debug"]["print_results"] and solved_force.gamma and solved_force.gamma.value is not None:
                        print(f"  γ: {math.degrees(solved_force.gamma.value):.1f}° ✓")

    else:
        # Just verify given forces have correct components
        if spec["debug"]["print_results"]:
            print("\n--- Force Properties ---")

        if spec["debug"]["assert_values"]:
            for force_name, force in problem.forces.items():
                if force_name in expected:
                    expected_values = expected[force_name]
                    expected_unit = expected_values.get("unit", "N")

                    if spec["debug"]["print_results"]:
                        print(f"\n--- {force_name} ---")

                    # Check and print magnitude
                    if "magnitude" in expected_values:
                        mag_val = force.magnitude_in(force.magnitude.preferred) if force.magnitude and force.magnitude.preferred else force.magnitude.value if force.magnitude else None
                        if mag_val is not None:
                            assert_force_magnitude(force, expected_values["magnitude"], expected_unit)
                            if spec["debug"]["print_results"]:
                                print(f"  Magnitude: {mag_val:.3f} {expected_unit} ✓")

                    if "x" in expected_values and force.x:
                        assert force.x.value is not None and force.x.preferred is not None
                        x_val = force.x.value / force.x.preferred.si_factor
                        assert_force_component(x_val, expected_values["x"], "x", force_name, expected_unit)
                        if spec["debug"]["print_results"]:
                            print(f"  Fx: {x_val:.3f} {expected_unit} ✓")

                    if "y" in expected_values and force.y:
                        assert force.y.value is not None and force.y.preferred is not None
                        y_val = force.y.value / force.y.preferred.si_factor
                        assert_force_component(y_val, expected_values["y"], "y", force_name, expected_unit)
                        if spec["debug"]["print_results"]:
                            print(f"  Fy: {y_val:.3f} {expected_unit} ✓")

                    if "z" in expected_values and force.z:
                        assert force.z.value is not None and force.z.preferred is not None
                        z_val = force.z.value / force.z.preferred.si_factor
                        assert_force_component(z_val, expected_values["z"], "z", force_name, expected_unit)
                        if spec["debug"]["print_results"]:
                            print(f"  Fz: {z_val:.3f} {expected_unit} ✓")

                    if "alpha" in expected_values and force.alpha:
                        assert_direction_angle(force.alpha, expected_values["alpha"], "α", force_name)
                        if spec["debug"]["print_results"] and force.alpha.value is not None:
                            print(f"  α: {math.degrees(force.alpha.value):.1f}° ✓")

                    if "beta" in expected_values and force.beta:
                        assert_direction_angle(force.beta, expected_values["beta"], "β", force_name)
                        if spec["debug"]["print_results"] and force.beta.value is not None:
                            print(f"  β: {math.degrees(force.beta.value):.1f}° ✓")

                    if "gamma" in expected_values and force.gamma:
                        assert_direction_angle(force.gamma, expected_values["gamma"], "γ", force_name)
                        if spec["debug"]["print_results"] and force.gamma.value is not None:
                            print(f"  γ: {math.degrees(force.gamma.value):.1f}° ✓")


if __name__ == "__main__":
    # Run tests with detailed output
    for problem_key in CARTESIAN_3D_PROBLEMS.keys():
        problem = CARTESIAN_3D_PROBLEMS[problem_key]
        problem["debug"]["print_results"] = True
        test_cartesian_3d_problem(problem_key)
        problem["debug"]["print_results"] = False
