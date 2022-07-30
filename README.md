# GE_LAB

## **Clone**

```bash
git https://github.com/rafadls/GE_LAB.git
cd GE_LAB
```

## **resources**

You can get the [resources]([myLib/README.md](https://drive.google.com/file/d/1LxKXb73UsiJJiof2Gpx2r2O6wlajICQl/view?usp=sharing)) used in the thesis. The file it is .zip format, so you must extract the folder resources/ and place it on the code's path.

## **RUN**

```bash
python -m <problem module> --experiment_name=<name output folder> --parameters=<pareameters file> --algorithm=<GE algorithm>
```

## **Li-Ion Battery: equilibrium**
### **Drag coefficient**

```bash
python -m problems.LIB.CI.cdrag --experiment_name='results/cdrag' --parameters='parameters/LIB/CI/cdrag.yml' --algorithm='SGE'
```


### **Friction factor**

```bash
python -m problems.LIB.CI.ff --experiment_name='results/ff' --parameters='parameters/LIB/CI/ff.yml' --algorithm='SGE'
```

### **Nusselt number**

```bash
python -m problems.LIB.CI.n --experiment_name='results/n' --parameters='parameters/LIB/CI/n.yml' --algorithm='SGE'
```

## **Li-Ion Battery: border condition*

### **V**

```bash
python -m problems.LIB.BC.v --experiment_name='results/v' --parameters='parameters/LIB/BC/v.yml' --algorithm='SGE'
```


### **T**

```bash
python -m problems.LIB.BC.t --experiment_name='results/t' --parameters='parameters/LIB/BC/t.yml' --algorithm='SGE'
```

### **P**

```bash
python -m problems.LIB.BC.p --experiment_name='results/p' --parameters='parameters/LIB/BC/p.yml' --algorithm='SGE'
```

## **Li-Ion Battery: Fluid temperature*

### **V**

```bash
python -m problems.LIB.TF.tf --experiment_name='results/tf' --parameters='parameters/LIB/TF/tf.yml' --algorithm='SGE'
```
