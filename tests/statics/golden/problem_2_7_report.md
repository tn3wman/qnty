# Engineering Calculation Report: Problem 2-7

**Generated:** {{GENERATED_DATETIME}}

## 1. Known Variables

<div align="center">

| Vector | $F_u$ (N) | $F_v$ (N) | $\|\vec{F}\|$ (N) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| $\vec{F_1}$ | 2070.6 | 2928.2 | 4000.0 | -30.0 | +v |

</div>

## 2. Unknown Variables

<div align="center">

| Vector | $F_u$ (N) | $F_v$ (N) | $\|\vec{F}\|$ (N) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| $\vec{F_{1u}}$ | ? | ? | ? | 0.0 | +u |
| $\vec{F_{1v}}$ | ? | ? | ? | 0.0 | +v |

</div>

## 3. Equations Used

1. $\frac{|\vec{F_{1u}}|}{\sin(\angle(\vec{F_{{1v}}}, \vec{F_{{1}}}))} = \frac{|\vec{F_{1}}|}{\sin(\angle(\vec{F_{{1u}}}, \vec{F_{{1v}}}))}$

2. $\frac{|\vec{F_{1v}}|}{\sin(\angle(\vec{F_{{1u}}}, \vec{F_{{1}}}))} = \frac{|\vec{F_{1}}|}{\sin(\angle(\vec{F_{{1u}}}, \vec{F_{{1v}}}))}$

## 4. Step-by-Step Solution

**Step 1: Solve for triangle angles**

$$
\begin{aligned}
\angle(\vec{F_{{1u}}}, \vec{F_{{1}}}) &= \angle(\vec{u}, \vec{v}) - |\angle(\vec{v}, \vec{F_{{1}}})| \\
&= 75^{\circ} - 30^{\circ} \\
&= 45^{\circ} \\
\angle(\vec{F_{{1v}}}, \vec{F_{{1}}}) &= |\angle(\vec{v}, \vec{F_{{1v}}}) - \angle(\vec{v}, \vec{F_{{1}}})| \\
&= |0^{\circ} - -30^{\circ}| \\
&= 30^{\circ} \\
\angle(\vec{F_{{1u}}}, \vec{F_{{1v}}}) &= 180^{\circ} - 45^{\circ} - 30^{\circ} \\
&= 105^{\circ} \\
\end{aligned}
$$

**Step 2: Solve for $|\vec{F_{{1u}}}|$ using Eq 1**

$$
\begin{aligned}
|\vec{F_{1u}}| &= 4000  \cdot  \frac{\sin(30^{\circ})}{\sin(105^{\circ})} \\
&= 2071\ \text{N} \\
\end{aligned}
$$

**Step 3: Solve for $|\vec{F_{{1v}}}|$ using Eq 2**

$$
\begin{aligned}
|\vec{F_{1v}}| &= 4000  \cdot  \frac{\sin(45^{\circ})}{\sin(105^{\circ})} \\
&= 2928\ \text{N} \\
\end{aligned}
$$

## 5. Summary of Results

<div align="center">

| Vector | $F_u$ (N) | $F_v$ (N) | $\|\vec{F}\|$ (N) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| $\vec{F_{1u}}$ | 2070.6 | 0.0 | 2070.6 | 0.0 | +u |
| $\vec{F_{1v}}$ | 0.0 | 2928.2 | 2928.2 | 0.0 | +v |

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