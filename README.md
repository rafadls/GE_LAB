# GE_LAB

## **Clone**

```bash
git https://github.com/rafadls/GE_LAB.git
cd GE_LAB
```

## **resources**

You can get the [resources]([myLib/README.md](https://drive.google.com/file/d/1LxKXb73UsiJJiof2Gpx2r2O6wlajICQl/view?usp=sharing)) used in the thesis.

## **RUN**

```bash
python -m <problem module> --experiment_name=<name output folder> --parameters=<pareameters file> --algorithm=<GE algorithm>
```

## **Li-Ion Battery: equilibrium**
### **Drag coefficient**
* Normal
```bash
python -m problems.LIB_Simulation.All.cdrag --experiment_name='results/cdrag' --parameters='parameters/LIB_Simulation/All/cdrag.yml' --algorithm='SGE'
```
* Simple
```bash
python -m problems.LIB_Simulation.All_simple.cdrag --experiment_name='results/cdrag_simple' --parameters='parameters/LIB_Simulation/All_simple/cdrag.yml' --algorithm='SGE'
```
* Simplest
```bash
python -m problems.LIB_Simulation.All_simplest.cdrag --experiment_name='results/cdrag_simplest' --parameters='parameters/LIB_Simulation/All_simplest/cdrag.yml' --algorithm='SGE'
```

### **Friction factor**
* Normal
```bash
python -m problems.LIB_Simulation.All.ff --experiment_name='results/ff' --parameters='parameters/LIB_Simulation/All/ff.yml' --algorithm='SGE'
```
* Simple
```bash
python -m problems.LIB_Simulation.All_simple.ff --experiment_name='results/ff_simple' --parameters='parameters/LIB_Simulation/All_simple/ff.yml' --algorithm='SGE'
```
* Simplest
```bash
python -m problems.LIB_Simulation.All_simplest.ff --experiment_name='results/ff_simplest' --parameters='parameters/LIB_Simulation/All_simplest/ff.yml' --algorithm='SGE'
```

### **Nusselt number**
* Normal
```bash
python -m problems.LIB_Simulation.All.n --experiment_name='results/n' --parameters='parameters/LIB_Simulation/All/n.yml' --algorithm='SGE'
```
* Simple
```bash
python -m problems.LIB_Simulation.All_simple.n --experiment_name='results/n_simple' --parameters='parameters/LIB_Simulation/All_simple/n.yml' --algorithm='SGE'
```
* Simplest
```bash
python -m problems.LIB_Simulation.All_simplest.n --experiment_name='results/n_simplest' --parameters='parameters/LIB_Simulation/All_simplest/n.yml' --algorithm='SGE'
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
