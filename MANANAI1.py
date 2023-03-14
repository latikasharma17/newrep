# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 16:17:49 2023

@author: MANAN GOYAL
"""

class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        
    def get_neighbors(self, var):
        return [v for v in self.variables if v != var and self.are_connected(var, v)]
        
    def are_connected(self, var1, var2):
        return (var1, var2) in self.constraints or (var2, var1) in self.constraints
    
    def remove_inconsistent_values(self, var1, var2):
        removed = False
        for x in self.domains[var1]:
            if all(not self.are_connected(x, y) or any((x, z) in self.constraints and z in self.domains[y] for z in self.domains[y]) for y in self.get_neighbors(var2)):
                self.domains[var1].remove(x)
                removed = True
        return removed
    
    def constraint_propagation(self, var):
        queue = self.get_neighbors(var)
        while queue:
            curr_var = queue.pop(0)
            if self.remove_inconsistent_values(curr_var, var):
                queue.extend(self.get_neighbors(curr_var))
                
    def backtracking_search(self):
        return self.backtrack({})
    
    def backtrack(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                if self.backtrack(assignment):
                    return assignment
                del assignment[var]
        return None
    
    def select_unassigned_variable(self, assignment):
        unassigned_vars = [v for v in self.variables if v not in assignment]
        return unassigned_vars[0]
    
    def order_domain_values(self, var):
        return self.domains[var]
    
    def is_consistent(self, var, value, assignment):
        new_assignment = assignment.copy()
        new_assignment[var] = value
        for v, val in new_assignment.items():
            if (v, var) in self.constraints and val >= value:
                return False
            if (var, v) in self.constraints and val <= value:
                return False
        return True
    

# Define the variables and their domains
variables = ['A', 'B', 'C']
domains = {'A': [1, 2, 3], 'B': [1, 2, 3], 'C': [1, 2, 3]}

# Define the constraints
constraints = [('A', 'B'), ('B', 'C')]

# Create the CSP
csp = CSP(variables, domains, constraints)

# Call the backtracking search algorithm
result = csp.backtracking_search()
print(result)

# Implement constraint propagation whenever a variable is assigned
for var in csp.variables:
    if var in result:
        csp.constraint_propagation(var)

# Print the updated domains after constraint propagation
print(csp.domains)
