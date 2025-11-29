# Engineering Calculation Report: Problem 2-11

**Generated:** 2025-11-29 15:48:04

## 1. Known Variables

<div align="center">

| Vector | $F_x$ (N) | $F_y$ (N) | $\|\vec{F}\|$ (N) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| $\vec{F_A}$ | 6928.2 | 4000.0 | 8000.0 | -60.0 | +y |
| $\vec{F_B}$ | 3856.7 | -4596.3 | 6000.0 | 40.0 | -y |

</div>

## 2. Unknown Variables

<div align="center">

| Vector | $F_x$ (N) | $F_y$ (N) | $\|\vec{F}\|$ (N) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| $\vec{F_R}$ | ? | ? | ? | ? | +x |

</div>

## 3. Equations Used

1. $|\vec{F_R}|^2 = |\vec{F_A}|^2 + |\vec{F_B}|^2 + 2 \cdot |\vec{F_A}| \cdot |\vec{F_B}| \cdot \cos(\angle(\vec{F_A}, \vec{F_B}))$

2. $\frac{\sin(\angle(\vec{F_B}, \vec{F_R}))}{|\vec{F_A}|} = \frac{\sin(\angle(\vec{F_A}, \vec{F_B}))}{|\vec{F_R}|}$

## 4. Step-by-Step Solution

**Step 1: Solve for $\angle(\vec{F_A}, \vec{F_B})$**

$$
\begin{aligned}
\angle(\vec{F_A}, \vec{F_B}) &= |\angle(\vec{y}, \vec{F_A}) - \angle(\vec{-y}, \vec{F_B})| \\
&= |-60^{\circ} - 40^{\circ}| \\
&= 100^{\circ} \\
\end{aligned}
$$

**Step 2: Solve for $|\vec{F_R}|$ using Eq 1**

$$
\begin{aligned}
|\vec{F_R}| &= \sqrt{(8000.0)^2 + (6000.0)^2 + 2(8000.0)(6000.0)\cos(100^{\circ})} \\
&= 10801.4\ \text{N} \\
\end{aligned}
$$

**Step 3: Solve for $\angle(\vec{F_B}, \vec{F_R})$ using Eq 2**

$$
\begin{aligned}
\angle(\vec{F_B}, \vec{F_R}) &= \sin^{-1}(8000.0 \cdot \frac{\sin(100^{\circ})}{10801.4}) \\
&= 46.8^{\circ} \\
\end{aligned}
$$

**Step 4: Solve for $\angle(\vec{x}, \vec{F_R})$ with respect to +x**

$$
\begin{aligned}
\angle(\vec{x}, \vec{F_R}) &= \angle(\vec{x}, \vec{-y}) + \angle(\vec{-y}, \vec{F_B}) + \angle(\vec{F_B}, \vec{F_R}) \\
&= -90.0^{\circ} + 40.0^{\circ} + 46.8^{\circ} \\
&= -3.2^{\circ} \\
\end{aligned}
$$

## 5. Summary of Results

<div align="center">

| Vector | $F_x$ (N) | $F_y$ (N) | $\|\vec{F}\|$ (N) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| $\vec{F_R}$ | 10784.9 | -596.3 | 10801.4 | -3.2 | +x |

</div>


---

## Disclaimer

While every effort has been made to ensure the accuracy and reliability of the calculations provided, we do not guarantee that the information is complete, up-to-date, or suitable for any specific purpose. Users must independently verify the results and assume full responsibility for any decisions or actions taken based on its output. Use of this calculator is entirely at your own risk, and we expressly disclaim any liability for errors or omissions in the information provided.

**Report Details:**
- **Generated Date:** November 29, 2025
- **Generated Using:** Qnty Library
- **Version:** Beta (Independent verification required for production use)

**Signatures:**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Calculated By | _________________ | _________________ | _______ |
| Reviewed By | _________________ | _________________ | _______ |
| Approved By | _________________ | _________________ | _______ |

*Report generated using qnty library*