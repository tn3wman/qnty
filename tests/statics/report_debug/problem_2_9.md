# Engineering Calculation Report: Problem 2-9

**Generated:** 2025-11-29 15:10:14

## 1. Known Variables

<div align="center">

| Vector | $F_x$ (lbf) | $F_y$ (lbf) | $\|\vec{F}\|$ (lbf) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| $\vec{F_B}$ | 779.4 | -450.0 | 900.0 | 60.0 | -y |
| $\vec{F_R}$ | 1200.0 | 0.0 | 1200.0 | 0.0 | +x |

</div>

## 2. Unknown Variables

<div align="center">

| Vector | $F_x$ (lbf) | $F_y$ (lbf) | $\|\vec{F}\|$ (lbf) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| $\vec{F_A}$ | ? | ? | ? | ? | +x |

</div>

## 3. Equations Used

1. $|\vec{F_A}|^2 = |\vec{F_B}|^2 + |\vec{F_R}|^2 - 2 \cdot |\vec{F_B}| \cdot |\vec{F_R}| \cdot \cos(\angle(\vec{F_B}, \vec{F_R}))$

2. $\frac{\sin(\angle(\vec{F_R}, \vec{F_A}))}{|\vec{F_B}|} = \frac{\sin(\angle(\vec{F_B}, \vec{F_R}))}{|\vec{F_A}|}$

## 4. Step-by-Step Solution

**Step 1: Solve for $\angle(\vec{F_B}, \vec{F_R})$**

$$
\begin{aligned}
\angle(\vec{F_B}, \vec{F_R}) &= |\angle(\vec{-y}, \vec{F_B}) - \angle(\vec{x}, \vec{F_R})| \\
&= |60^{\circ} - 0^{\circ}| \\
&= 30^{\circ} \\
\end{aligned}
$$

**Step 2: Solve for $|\vec{F_A}|$ using Eq 1**

$$
\begin{aligned}
|\vec{F_A}| &= \sqrt{(900)^2 + (1200)^2 - 2(900)(1200)\cos(30^{\circ})} \\
&= 615.9\ \text{lbf} \\
\end{aligned}
$$

**Step 3: Solve for $\angle(\vec{F_R}, \vec{F_A})$ using Eq 2**

$$
\begin{aligned}
\angle(\vec{F_R}, \vec{F_A}) &= \sin^{-1}(900.0 \cdot \frac{\sin(30^{\circ})}{615.9}) \\
&= 46.9^{\circ} \\
\end{aligned}
$$

**Step 4: Solve for $\angle(\vec{x}, \vec{F_A})$ with respect to +x**

$$
\begin{aligned}
\angle(\vec{x}, \vec{F_A}) &= \angle(\vec{F_R}, \vec{F_A})  \text{(since } F_R \text{ is along +x)} \\
&= 46.9^{\circ} \\
\end{aligned}
$$

## 5. Summary of Results

<div align="center">

| Vector | $F_x$ (lbf) | $F_y$ (lbf) | $\|\vec{F}\|$ (lbf) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| $\vec{F_A}$ | 420.6 | 450.0 | 615.9 | 46.9 | +x |

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