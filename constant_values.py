##Constant on workers
heures_travail_ouvrier = 8
paye_ouvier_jour = 300
paye_ouvrier_par_heure = paye_ouvier_jour/heures_travail_ouvrier
max_ouvrier_infra = 4

##Constant on prices
prix_aerien = 500
prix_semi_aerien = 750 
prix_fourreau = 900

##Constant on time
temps_aerien = 2
temps_semi_aerien = 4 
temps_fourreau = 5

##Constants in simulation form
EQUIPPEMENT_PRICE =  {"aerien" : prix_aerien, "fourreau" : prix_fourreau, "semi-aerien" : prix_semi_aerien}
TIME_TO_FIX = {"aerien" : temps_aerien, "fourreau" : temps_fourreau, "semi-aerien" : temps_semi_aerien}
WORKER_PAY_PER_8H = paye_ouvier_jour         # euros
MAX_WORKERS_PER_INFRA = max_ouvrier_infra
PHASES = [0.4, 0.2, 0.2, 0.2]
