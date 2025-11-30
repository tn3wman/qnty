# Engineering Calculation Report: Problem 2-5

**Generated:** 2025-11-30 16:55:38

## 1. Known Variables

<div align="center">

| Vector | $F_x$ (lbf) | $F_y$ (lbf) | $\|\vec{F}\|$ (lbf) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| $\vec{F_R}$ | 0.0 | -350.0 | 350.0 | 270.0 | +x |

</div>

## 2. Unknown Variables

<div align="center">

| Vector | $F_x$ (lbf) | $F_y$ (lbf) | $\|\vec{F}\|$ (lbf) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| $\vec{F_{AB}}$ | ? | ? | ? | 225.0 | +x |
| $\vec{F_{AC}}$ | ? | ? | ? | 330.0 | +x |

</div>

## 3. Equations Used

1. $\frac{|\vec{F_{AB}}|}{\sin(\angle(\vec{F_{AC}}, \vec{F_{R}}))} = \frac{|\vec{F_{R}}|}{\sin(\angle(\vec{F_{AB}}, \vec{F_{AC}}))}$

2. $\frac{|\vec{F_{AC}}|}{\sin(\angle(\vec{F_{AB}}, \vec{F_{R}}))} = \frac{|\vec{F_{R}}|}{\sin(\angle(\vec{F_{AB}}, \vec{F_{AC}}))}$

## 4. Step-by-Step Solution

**Step 1: Solve for triangle angles**

$$
\begin{aligned}
\angle(\vec{F_{AB}}, \vec{F_{R}}) &= |\angle(\vec{x}, \vec{F_{AB}}) - \angle(\vec{x}, \vec{F_{R}})| \\
&= |225^{\circ} - 270^{\circ}| \\
&= 45^{\circ} \\
\angle(\vec{F_{AC}}, \vec{F_{R}}) &= |\angle(\vec{x}, \vec{F_{AC}}) - \angle(\vec{x}, \vec{F_{R}})| \\
&= |330^{\circ} - 270^{\circ}| \\
&= 60^{\circ} \\
\angle(\vec{F_{AB}}, \vec{F_{AC}}) &= 180^{\circ} - 45^{\circ} - 60^{\circ} \\
&= 75^{\circ} \\
\end{aligned}
$$

**Step 2: Solve for $|\vec{F_{AB}}|$ using Eq 1**

$$
\begin{aligned}
|\vec{F_{AB}}| &= 350  \cdot  \frac{\sin(60^{\circ})}{\sin(75^{\circ})} \\
&= 314\ \text{lbf} \\
\end{aligned}
$$

**Step 3: Solve for $|\vec{F_{AC}}|$ using Eq 2**

$$
\begin{aligned}
|\vec{F_{AC}}| &= 350  \cdot  \frac{\sin(45^{\circ})}{\sin(75^{\circ})} \\
&= 256\ \text{lbf} \\
\end{aligned}
$$

## 5. Summary of Results

<div align="center">

| Vector | $F_x$ (lbf) | $F_y$ (lbf) | $\|\vec{F}\|$ (lbf) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| $\vec{F_{AB}}$ | -221.9 | -221.9 | 313.8 | 225.0 | +x |
| $\vec{F_{AC}}$ | 221.9 | -128.1 | 256.2 | 330.0 | +x |

</div>


---

## Disclaimer

While every effort has been made to ensure the accuracy and reliability of the calculations provided, we do not guarantee that the information is complete, up-to-date, or suitable for any specific purpose. Users must independently verify the results and assume full responsibility for any decisions or actions taken based on its output. Use of this calculator is entirely at your own risk, and we expressly disclaim any liability for errors or omissions in the information provided.

**Report Details:**
- **Generated Date:** November 30, 2025
- **Generated Using:** Qnty Library
- **Version:** Beta (Independent verification required for production use)

**Signatures:**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Calculated By | _________________ | _________________ | _______ |
| Reviewed By | _________________ | _________________ | _______ |
| Approved By | _________________ | _________________ | _______ |

*Report generated using qnty library*