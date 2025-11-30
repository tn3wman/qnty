# Engineering Calculation Report: Problem 2-13

**Generated:** {{GENERATED_DATETIME}}

## 1. Known Variables

<div align="center">

| Vector | $F_a$ (lbf) | $F_b$ (lbf) | $\|\vec{F}\|$ (lbf) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| F | 30.6 | -26.9 | 20.0 | 80.0 | -b |

</div>

## 2. Unknown Variables

<div align="center">

| Vector | $F_a$ (lbf) | $F_b$ (lbf) | $\|\vec{F}\|$ (lbf) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| $\vec{F_a}$ | ? | ? | ? | 0.0 | +a |
| $\vec{F_b}$ | ? | ? | ? | 0.0 | -b |

</div>

## 3. Equations Used

1. $\frac{|\vec{F_{a}}|}{\sin(\angle(\vec{F_{{b}}}, \vec{F}))} = \frac{|\vec{F}|}{\sin(\angle(\vec{F_{{a}}}, \vec{F_{{b}}}))}$

2. $\frac{|\vec{F_{b}}|}{\sin(\angle(\vec{F_{{a}}}, \vec{F}))} = \frac{|\vec{F}|}{\sin(\angle(\vec{F_{{a}}}, \vec{F_{{b}}}))}$

## 4. Step-by-Step Solution

**Step 1: Solve for triangle angles**

$$
\begin{aligned}
\angle(\vec{F_{{a}}}, \vec{F}) &= \angle(\vec{a}, \vec{-b}) - |\angle(\vec{-b}, \vec{F})| \\
&= 140^{\circ} - 80^{\circ} \\
&= 60^{\circ} \\
\angle(\vec{F_{{b}}}, \vec{F}) &= |\angle(\vec{-b}, \vec{F_{{b}}}) - \angle(\vec{-b}, \vec{F})| \\
&= |0^{\circ} - 80^{\circ}| \\
&= 80^{\circ} \\
\angle(\vec{F_{{a}}}, \vec{F_{{b}}}) &= 180^{\circ} - 60^{\circ} - 80^{\circ} \\
&= 40^{\circ} \\
\end{aligned}
$$

**Step 2: Solve for $|\vec{F_{{a}}}|$ using Eq 1**

$$
\begin{aligned}
|\vec{F_{a}}| &= 20  \cdot  \frac{\sin(80^{\circ})}{\sin(40^{\circ})} \\
&= 31\ \text{lbf} \\
\end{aligned}
$$

**Step 3: Solve for $|\vec{F_{{b}}}|$ using Eq 2**

$$
\begin{aligned}
|\vec{F_{b}}| &= 20  \cdot  \frac{\sin(60^{\circ})}{\sin(40^{\circ})} \\
&= 27\ \text{lbf} \\
\end{aligned}
$$

## 5. Summary of Results

<div align="center">

| Vector | $F_a$ (lbf) | $F_b$ (lbf) | $\|\vec{F}\|$ (lbf) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| $\vec{F_a}$ | 30.6 | 0.0 | 30.6 | 0.0 | +a |
| $\vec{F_b}$ | 0.0 | -26.9 | 26.9 | 0.0 | -b |

</div>


---

## Disclaimer

While every effort has been made to ensure the accuracy and reliability of the calculations provided, we do not guarantee that the information is complete, up-to-date, or suitable for any specific purpose. Users must independently verify the results and assume full responsibility for any decisions or actions taken based on its output. Use of this calculator is entirely at your own risk, and we expressly disclaim any liability for errors or omissions in the information provided.

**Report Details:**
- **Generated Date:** {{GENERATED_DATE}}
- **Generated Using:** Qnty Library
- **Version:** Beta (Independent verification required for production use)

**Signatures:**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Calculated By | _________________ | _________________ | _______ |
| Reviewed By | _________________ | _________________ | _______ |
| Approved By | _________________ | _________________ | _______ |

*Report generated using qnty library*