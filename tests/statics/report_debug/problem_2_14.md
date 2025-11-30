# Engineering Calculation Report: Problem 2-14

**Generated:** 2025-11-30 06:35:50

## 1. Known Variables

<div align="center">

| Vector | $F_a$ (lbf) | $F_b$ (lbf) | $\|\vec{F}\|$ (lbf) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| $\vec{F_a}$ | 30.0 | 0.0 | 30.0 | 0.0 | +a |

</div>

## 2. Unknown Variables

<div align="center">

| Vector | $F_a$ (lbf) | $F_b$ (lbf) | $\|\vec{F}\|$ (lbf) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| F | ? | ? | ? | 80.0 | -b |
| $\vec{F_b}$ | ? | ? | ? | 0.0 | -b |

</div>

## 3. Equations Used

1. $\frac{|\vec{F_b}|}{\sin(\angle(\vec{F_a}, \vec{F}))} = \frac{|\vec{F_a}|}{\sin(\angle(\vec{F_b}, \vec{F}))}$

2. $\frac{|\vec{F}|}{\sin(\angle(\vec{F_a}, \vec{F_b}))} = \frac{|\vec{F_a}|}{\sin(\angle(\vec{F_b}, \vec{F}))}$

## 4. Step-by-Step Solution

**Step 1: Solve for triangle angles**

$$
\begin{aligned}
\angle(\vec{F_b}, \vec{F}) &= |\angle(\vec{-b}, \vec{F_b}) - \angle(\vec{-b}, \vec{F})| \\
&= |0^{\circ} - 80^{\circ}| \\
&= 80^{\circ} \\
\angle(\vec{F_a}, \vec{F}) &= \angle(\vec{a}, \vec{-b}) - |\angle(\vec{-b}, \vec{F})| \\
&= 140^{\circ} - 80^{\circ} \\
&= 60^{\circ} \\
\angle(\vec{F_a}, \vec{F_b}) &= 180^{\circ} - 80^{\circ} - 60^{\circ} \\
&= 40^{\circ} \\
\end{aligned}
$$

**Step 2: Solve for $|\vec{F_b}|$ using Eq 1**

$$
\begin{aligned}
|\vec{F_b}| &= 30  \cdot  \frac{\sin(60^{\circ})}{\sin(80^{\circ})} \\
&= 26\ \text{lbf} \\
\end{aligned}
$$

**Step 3: Solve for $|\vec{F}|$ using Eq 2**

$$
\begin{aligned}
|\vec{F}| &= 30  \cdot  \frac{\sin(40^{\circ})}{\sin(80^{\circ})} \\
&= 20\ \text{lbf} \\
\end{aligned}
$$

## 5. Summary of Results

<div align="center">

| Vector | $F_a$ (lbf) | $F_b$ (lbf) | $\|\vec{F}\|$ (lbf) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| F | 30.0 | -26.4 | 19.6 | 80.0 | -b |
| $\vec{F_b}$ | 0.0 | -26.4 | 26.4 | 0.0 | -b |

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