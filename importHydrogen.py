import pyomo.environ as pyo

# Create a Pyomo model
model = pyo.ConcreteModel()



# Define model parameters
model.H2inNH3 = pyo.Param(initialize=0.18)



# Define model variables
model.boatsNH3 = pyo.Var(domain=pyo.NonNegativeReals)
model.boatsCH4 = pyo.Var(domain=pyo.NonNegativeReals)


model.objective = pyo.Objective(expr=model.boatsCH4*model.volumeBoat*model.densityCH4*model.H2inCH4+model.boatsNH3*model.volumeBoat*model.densityNH3*model.H2inNH3, sense=pyo.maximize)


def maxBoats(model):
    return model.boatsNH3+model.boatsCH4 <= model.maxBoats

model.maxBoatsConstr = pyo.Constraint(rule=maxBoats)

def maxEnergy(model):
    return model.boatsNH3*model.volumeBoat*model.densityNH3*model.LHV_NH3/(1.-model.losses_NH3) + model.boatsCH4*model.volumeBoat*model.densityCH4*model.LHV_CH4/(1-model.losses_CH4) <= model.maxEnergy

model.maxEnergyConstr = pyo.Constraint(rule=maxEnergy)

def maxCO2(model):
    return model.boatsCH4*model.volumeBoat*model.densityCH4*model.CO2inCH4 <= model.maxCO2

model.maxCO2Constr = pyo.Constraint(rule=maxCO2)


solver = pyo.SolverFactory('/Users/xrixhon/Documents/Software/AMPL/gurobi')
sol = solver.solve(model)


print(model.boatsCH4.value)
print(model.boatsNH3.value)