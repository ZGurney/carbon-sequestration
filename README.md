# Tiny forests project

Developed by [Zinzan Gurney](mailto:z.gurney@reply.com) . Updated on 23 February 2024. Code in [GitHub repository](https://github.com/ZGurney/carbon-sequestration). Methodology described below:

## Calculating carbon sequestered by tiny forests:

1. Green weight (above ground): `green_weight_above_ground = coefficient * height * diameter^2`
	- If `diameter < 11`, `coefficient = 0.25`
	- If `diameter >= 11, coefficient = 0.15`
	- Need to convert diameter (inches), height (feet), weight (pounds) to metric equivalent
1. Green weight (total): `green_weight_total = 1.2 * green_weight_above_ground`
	- The root system weighs about 20% as much as the above-ground weight of the tree.
2. Dry weight: `dry_weight = 0.725 * green_weight_total`
	- The average tree is 72.5% dry matter and 27.5% moisture.
3. Carbon content: `carbon_content = 0.5 * dry_weight`
	- The average carbon content is generally 50% of the tree’s total volume.
4. CO2 captured: `co2_captured = co2_carbon_ratio * carbon_content`
	- `carbon_atomic_weight = 12.00`
	- `oxygen_atomic_weight = 16.00`
	- `co2_weight = carbon_atomic_weight + 2*oxygen_atomic_weight`
	- `co2_carbon_ratio = co2_weight / carbon_atomic_weight`
5. CO2 captured per year: `annual_co2_captured = co2_captured / tree_age`
6. Calculate CO2 captured per year for one tiny forest: `tiny_forest_co2_captured = 600 * annual_co2_captured`
	- [600 trees in one tiny forest](https://earthwatch.org.uk/program/tiny-forest/)
7. Calculate CO2 captured per year for all tiny forests:
`all_tiny_forests_co2_captured = num_tiny_forests * tiny_forest_co2_captured`

## Calculating employee footprint
- Total employee emissions: `employee_emissions = num_employees * average_emissions_per_capita`
- 4.7 tonnes of CO2e emissions per UK resident: `average_emissions_per_capita = 4.7` in 2022 based on [Statista](https://www.statista.com/statistics/1299198/co2-emissions-per-capita-united-kingdom/)
	- Note: calculating emissions of a firm would best be done using the [GHG protocol framework](https://ghgprotocol.org)