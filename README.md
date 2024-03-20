# Tiny forests project

Developed by [AIM Reply](https://www.reply.com/aim-reply/en/) (Zinzan Gurney). Updated on 20 March 2024. Code in [GitHub repository](https://github.com/ZGurney/carbon-sequestration). Methodology described below:

## Calculating carbon sequestered by tiny forests:

1. Before starting, need to convert metric to imperial equivalent as algorithm is based on imperial units.
	- Diameter (centimetres to inches), 
	- Height (metres to feet), 
	- Weight (kilogramme to pounds)

2. Green weight (above ground): `green_weight_above_ground = coefficient * height * diameter^2`
	- If `diameter < 11`, `coefficient = 0.25`
	- If `diameter >= 11, coefficient = 0.15`
3. Green weight (total): `green_weight_total = 1.2 * green_weight_above_ground`
	- The root system weighs about 20% as much as the above-ground weight of the tree.
4. Dry weight: `dry_weight = 0.725 * green_weight_total`
	- The average tree is 72.5% dry matter and 27.5% moisture.
5. Carbon content: `carbon_content = 0.5 * dry_weight`
	- The average carbon content is generally 50% of the tree’s total volume.
6. CO2 captured: `co2_captured = co2_carbon_ratio * carbon_content`
	- `carbon_atomic_weight = 12.00`
	- `oxygen_atomic_weight = 16.00`
	- `co2_weight = carbon_atomic_weight + 2*oxygen_atomic_weight`
	- `co2_carbon_ratio = co2_weight / carbon_atomic_weight`
7. CO2 captured per year: `annual_co2_captured = co2_captured / tree_age`
8. Calculate CO2 captured per year for one tiny forest: `tiny_forest_co2_captured = 600 * annual_co2_captured`
	- [600 trees in one tiny forest](https://earthwatch.org.uk/program/tiny-forest/)
9. Calculate CO2 captured per year for all tiny forests:
`all_tiny_forests_co2_captured = num_tiny_forests * tiny_forest_co2_captured`

## Calculating employee footprint
- Total employee emissions: `employee_emissions = num_employees * average_emissions_per_capita`
- 4.7 tonnes of CO2e emissions per UK resident: `average_emissions_per_capita = 4.7` in 2022 based on [Statista](https://www.statista.com/statistics/1299198/co2-emissions-per-capita-united-kingdom/)
	- Note: calculating emissions of a firm would best be done using the [GHG protocol framework](https://ghgprotocol.org)