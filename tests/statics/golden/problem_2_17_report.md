# Engineering Calculation Report: Problem 2-17

**Generated:** {{GENERATED_DATETIME}}

## 1. Known Variables

<div align="center">

| Vector | $F_x$ (N) | $F_y$ (N) | $\|\vec{F}\|$ (N) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| $\vec{F_1}$ | -24.0 | 18.0 | 30.0 | -36.9 | -x |
| $\vec{F_2}$ | -6.8 | -18.8 | 20.0 | -20.0 | -y |
| $\vec{F_3}$ | 50.0 | 0.0 | 50.0 | 0.0 | +x |

</div>

## 2. Unknown Variables

<div align="center">

| Vector | $F_x$ (N) | $F_y$ (N) | $\|\vec{F}\|$ (N) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| $\vec{F_R}$ | ? | ? | ? | ? | +x |

</div>

## 3. Equations Used

1. $|F'|^2 = |\vec{F_1}|^2 + |\vec{F_2}|^2 + 2 \cdot |\vec{F_1}| \cdot |\vec{F_2}| \cdot \cos(\angle(\vec{F_1}, \vec{F_2}))$

2. $\frac{\sin(\angle(\vec{F_1}, \vec{F'}))}{|\vec{F_2}|} = \frac{\sin(\angle(\vec{F_1}, \vec{F_2}))}{|F'|}$

3. $|\vec{F_R}|^2 = |F'|^2 + |\vec{F_3}|^2 + 2 \cdot |F'| \cdot |\vec{F_3}| \cdot \cos(\angle(\vec{F'}, \vec{F_3}))$

4. $\frac{\sin(\angle(\vec{F'}, \vec{F_R}))}{|\vec{F_3}|} = \frac{\sin(\angle(\vec{F'}, \vec{F_3}))}{|\vec{F_R}|}$

## 4. Step-by-Step Solution

**Step 1: Solve for $\angle(\vec{F_1}, \vec{F_2})$**

$$
\begin{aligned}
\angle(\vec{F_1}, \vec{F_2}) &= \angle(\vec{y}, \vec{F_1}) + |\angle(\vec{-y}, \vec{F_2})| \\
&= (90^{\circ} - |\angle(\vec{-x}, \vec{F_1})|) + 20^{\circ} \\
&= (90^{\circ} - 37^{\circ}) + 20^{\circ} \\
&= 53^{\circ} + 20^{\circ} \\
&= 73^{\circ} \\
\end{aligned}
$$

**Step 2: Solve for $|\vec{F'}|$ using Eq 1**

$$
\begin{aligned}
|F'| &= \sqrt{(30.0)^2 + (20.0)^2 + 2(30.0)(20.0)\cos(73^{\circ})} \\
&= 30.9\ \text{N} \\
\end{aligned}
$$

**Step 3: Solve for $\angle(\vec{F_1}, \vec{F'})$ using Eq 2**

$$
\begin{aligned}
\angle(\vec{F_1}, \vec{F'}) &= \sin^{-1}(20.0 \cdot \frac{\sin(73^{\circ})}{30.9}) \\
&= 38.3^{\circ} \\
\end{aligned}
$$

**Step 4: Solve for $\angle(\vec{x}, \vec{F'})$ with respect to +x**

$$
\begin{aligned}
\angle(\vec{x}, \vec{F'}) &= \angle(\vec{x}, \vec{-x}) + \angle(\vec{-x}, \vec{F_1}) + \angle(\vec{F_1}, \vec{F'}) \\
&= 180.0^{\circ} + -36.9^{\circ} + 38.3^{\circ} \\
&= 181.5^{\circ} \\
\end{aligned}
$$

**Step 5: Solve for $\angle(\vec{F'}, \vec{F_3})$**

$$
\begin{aligned}
\angle(\vec{F'}, \vec{F_3}) &= |\angle(\vec{-x}, \vec{F'})| \\
&= |181^{\circ} - 180^{\circ}| \\
&= 1^{\circ} \\
\end{aligned}
$$

**Step 6: Solve for $|\vec{F_R}|$ using Eq 3**

$$
\begin{aligned}
|\vec{F_R}| &= \sqrt{(30.9)^2 + (50.0)^2 + 2(30.9)(50.0)\cos(1^{\circ})} \\
&= 19.2\ \text{N} \\
\end{aligned}
$$

**Step 7: Solve for $\angle(\vec{F'}, \vec{F_R})$ using Eq 4**

$$
\begin{aligned}
\angle(\vec{F'}, \vec{F_R}) &= \sin^{-1}(50.0 \cdot \frac{\sin(1^{\circ})}{19.2}) \\
&= 176.2^{\circ} \\
\end{aligned}
$$

**Step 8: Solve for $\angle(\vec{x}, \vec{F_R})$ with respect to +x**

$$
\begin{aligned}
\angle(\vec{x}, \vec{F_R}) &= \angle(\vec{x}, \vec{F'}) + \angle(\vec{F'}, \vec{F_R}) - 360^{\circ} \\
&= 181.5^{\circ} + 176.2^{\circ} - 360^{\circ} \\
&= -2.4^{\circ} \\
\end{aligned}
$$

## 5. Summary of Results

<div align="center">

| Vector | $F_x$ (N) | $F_y$ (N) | $\|\vec{F}\|$ (N) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| $\vec{F_R}$ | 19.2 | -0.8 | 19.2 | -2.4 | +x |

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