# Engineering Calculation Report: Problem 2-8

**Generated:** {{GENERATED_DATETIME}}

## 1. Known Variables

<div align="center">

| Vector | $F_u$ (N) | $F_v$ (N) | $\|\vec{F}\|$ (N) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| $\vec{F_2}$ | 6000.0 | -3105.8 | 6000.0 | -30.0 | +u |

</div>

## 2. Unknown Variables

<div align="center">

| Vector | $F_u$ (N) | $F_v$ (N) | $\|\vec{F}\|$ (N) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| $\vec{F_{2u}}$ | ? | ? | ? | 0.0 | +u |
| $\vec{F_{2v}}$ | ? | ? | ? | 0.0 | +v |

</div>

## 3. Equations Used

1. $\frac{|\vec{F_{2u}}|}{\sin(\angle(\vec{F_{{2v}}}, \vec{F_{{2}}}))} = \frac{|\vec{F_{2}}|}{\sin(\angle(\vec{F_{{2u}}}, \vec{F_{{2v}}}))}$

2. $\frac{|\vec{F_{2v}}|}{\sin(\angle(\vec{F_{{2u}}}, \vec{F_{{2}}}))} = \frac{|\vec{F_{2}}|}{\sin(\angle(\vec{F_{{2u}}}, \vec{F_{{2v}}}))}$

## 4. Step-by-Step Solution

**Step 1: Solve for triangle angles**

$$
\begin{aligned}
\angle(\vec{F_{{2u}}}, \vec{F_{{2}}}) &= |\angle(\vec{u}, \vec{F_{{2u}}}) - \angle(\vec{u}, \vec{F_{{2}}})| \\
&= |0^{\circ} - -30^{\circ}| \\
&= 30^{\circ} \\
\angle(\vec{F_{{2v}}}, \vec{F_{{2}}}) &= \angle(\vec{v}, \vec{u}) - |\angle(\vec{u}, \vec{F_{{2}}})| \\
&= 75^{\circ} - 30^{\circ} \\
&= 45^{\circ} \\
\angle(\vec{F_{{2u}}}, \vec{F_{{2v}}}) &= 180^{\circ} - 30^{\circ} - 45^{\circ} \\
&= 105^{\circ} \\
\end{aligned}
$$

**Step 2: Solve for $|\vec{F_{{2u}}}|$ using Eq 1**

$$
\begin{aligned}
|\vec{F_{2u}}| &= 6000  \cdot  \frac{\sin(45^{\circ})}{\sin(105^{\circ})} \\
&= 6000\ \text{N} \\
\end{aligned}
$$

**Step 3: Solve for $|\vec{F_{{2v}}}|$ using Eq 2**

$$
\begin{aligned}
|\vec{F_{2v}}| &= 6000  \cdot  \frac{\sin(30^{\circ})}{\sin(105^{\circ})} \\
&= 3106\ \text{N} \\
\end{aligned}
$$

## 5. Summary of Results

<div align="center">

| Vector | $F_u$ (N) | $F_v$ (N) | $\|\vec{F}\|$ (N) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| $\vec{F_{2u}}$ | 6000.0 | 0.0 | 6000.0 | 0.0 | +u |
| $\vec{F_{2v}}$ | 0.0 | -3105.8 | 3105.8 | 0.0 | +v |

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