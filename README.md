# GE_LAB

## **Clone**

```bash
git https://github.com/rafadls/GE_LAB.git
cd GE_LAB
```
## **RUN**

```bash
python -m <problem module> --experiment_name=<name output folder> --parameters=<pareameters file> --algorithm=<GE algorithm>
```
## **Li-Ion Battery: equilibrium**
### **Drag coefficient**

```bash
python -m problems.LIB_Simulation.All.cdrag --experiment_name='results/cdrag' --parameters='parameters/LIB_Simulation/All/cdrag.yml' --algorithm='SGE'
```
### **Friction factor**

```bash
python -m problems.LIB_Simulation.All.ff --experiment_name='results/ff' --parameters='parameters/LIB_Simulation/All/ff.yml' --algorithm='SGE'
```
### **Nusselt number**

```bash
python -m problems.LIB_Simulation.All.n --experiment_name='results/n' --parameters='parameters/LIB_Simulation/All/n.yml' --algorithm='SGE'
```

## **Li-Ion Battery: Discharge and cooling down**

### **Hcomb**

```bash
python -m problems.LIB_Real.Hcomb --experiment_name='results/Hcomb' --parameters='parameters/LIB_Real/Hcomb.yml' --algorithm='SGE'
```

### **dV_dT**

```bash
python -m problems.LIB_Real.dV_dT --experiment_name='results/dV_dT' --parameters='parameters/LIB_Real/dV_dT.yml' --algorithm='SGE'
```
