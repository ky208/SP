#-----------------------------------------------------
#
# Filename  : visualize.py
#
#-----------------------------------------------------
# This file retrives all variables in the storage and plots a barplot

class VariableBarPlot:
    def __init__(self, variable_values):
        self.variable_values = variable_values

    def plot(self):
        max_value = max(max(values) for values in self.variable_values.values())
        scale_factor = 10  # Scale of the chart

        for variable, values in self.variable_values.items():
            print(f'{variable}:')
            for value in values:
                scaled_value = int(round(value * scale_factor / max_value))
                bar = '*' * scaled_value
                print(f'    {value: 5.2f} | {bar}')
            print()

