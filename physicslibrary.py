class PU():

    #Physical Units

    def __init__(self, value, unit):
        self.value = value
        self.unit = unit
        self.numerators = {}
        self.denominators = {}
        self.split_units_to_dimensions()

    def split_units_to_dimensions(self):
        dimension = ""
        power = 1
        seen_numerators = []
        seen_denominators = []
        adding_denominators = False
        for i in range(0,len(self.unit)):
            try:
                int(self.unit[i])
                continue
            except ValueError:
                pass
            if self.unit[i] not in "*/^":
                dimension += self.unit[i]
            if self.unit[i] in "*/^" or i == len(self.unit)-1:
                if dimension != "":
                    if self.unit[i] == "^" and i < len(self.unit):
                        power = int(self.unit[i+1])
                    if not adding_denominators:
                        if dimension not in seen_numerators:
                            self.numerators[dimension] = power
                            seen_numerators.append(dimension)
                        else:
                            self.numerators[dimension] += power
                    else:
                        if dimension not in seen_denominators:
                            self.denominators[dimension] = power
                            seen_denominators.append(dimension)
                        else:
                            self.denominators[dimension] += power
                    if power > 1:
                        power = 1
                    dimension = ""
                if self.unit[i] == "/" and adding_denominators is False:
                    adding_denominators = True
                
        self.cancel_dimensions()

    def __str__(self):
        return str(self.value) + " " + self.unit

    def __add__(self, other):
        if type(self) == type(other):
            if self.numerators == other.numerators and self.denominators == other.denominators:
                new_value = self.value + other.value
                return PU(new_value, self.unit)
            else:
                raise TypeError("Incompatible dimensions for sum operation.")
        else:
            new_value = self.value + other
            return PU(new_value, self.unit)

    def __sub__(self, other):
        if type(self) == type(other):
            if self.numerators == other.numerators and self.denominators == other.denominators:
                new_value = self.value - other.value
                return PU(new_value, self.unit)
            else:
                raise TypeError("Incompatible dimensions for subtraction operation.")
        else:
            new_value = self.value - other
            return PU(new_value, self.unit)

    def __mul__(self, other):
        if type(self) == type(other):
            new_value = self.value * other.value
            new_unit = PU(new_value, self.unit)
            new_unit.combine_dimensions(other.numerators, other.denominators)
            if len(new_unit.numerators) == 0 and len(new_unit.denominators) == 0:
                return new_value
            else:
                return new_unit
        else:
            new_value = self.value * other
            return PU(new_value, self.unit)

    def __truediv__(self, other):
        if type(self) == type(other):
            new_value = self.value / other.value
            new_unit = PU(new_value, self.unit)
            # args are passed to combine_dimensions() in reverse order, because a/b / c/d = a/b * d/c
            new_unit.combine_dimensions(other.denominators, other.numerators)
            if len(new_unit.numerators) == 0 and len(new_unit.denominators) == 0:
                return new_value
            else:
                return new_unit
        else:
            new_value = self.value / other
            return PU(new_value, self.unit)

    def combine_dimensions(self, received_numerators, received_denominators):
        for dimension in received_numerators:
            if dimension in self.numerators:
                self.numerators[dimension] += received_numerators[dimension]
            else:
                self.numerators[dimension] = received_numerators[dimension]
        for dimension in received_denominators:
            if dimension in self.denominators:
                self.denominators[dimension] += received_denominators[dimension]
            else:
                self.denominators[dimension] = received_denominators[dimension]
        self.cancel_dimensions()


    def cancel_dimensions(self):
        self.unit = ""

        # Canceling out numerators that are being divided
        for dimension in list(self.numerators):
            power = int(self.numerators[dimension])
            for i in range(0, power):
                if dimension in self.numerators and dimension in self.denominators:
                    if self.numerators[dimension] > 1:
                        self.numerators[dimension] -= 1
                    else:
                        del self.numerators[dimension]
                    if self.denominators[dimension] > 1:
                        self.denominators[dimension] -= 1
                    else:
                        del self.denominators[dimension]
                if dimension not in self.numerators and dimension not in self.denominators:
                    break

        # Constructing new unit marking from the final dimensions
            if dimension in self.numerators:
                if self.unit != "" and self.unit[-1] != "*":
                    self.unit += "*"
                if self.numerators[dimension] == 1:
                    self.unit += str(dimension)
                else:
                    self.unit += str(dimension) + "^" + str(self.numerators[dimension])
        if len(self.denominators) > 0:
            self.unit += "/"
            for dimension in self.denominators:
                if self.unit[-1] not in "/*":
                    self.unit += "*"
                if self.denominators[dimension] == 1:
                    self.unit += str(dimension)
                else:
                    self.unit += str(dimension) + "^" + str(self.denominators[dimension])

    def get_scalar(self):
        return self.value




def main():
    diameter_pipe = PU(300, "m") * (0.001)
    print("Pipe diameter:", diameter_pipe)
    length_pipe = PU(300, "m")
    print("Pipe length:", length_pipe)
    temperature_water = PU(20, "C")
    density_water = PU(998.21, "kg") / (PU(1, "m") * PU(1, "m") * PU(1, "m"))
    viscosity_water = PU(0.001, "kg*m") / PU(1, "m^2*s")
    v_water = PU(2.5, "m") / PU(1, "s")
    print("Fluid, water. Temperature:", temperature_water, ", density:", density_water, ",")
    print("viscosity:", viscosity_water, ", average velocity:", v_water)
    print("\nAssumptions: i) No pump, ii) no difference in pressure at the ends of balance boundary,")
    print("iii) no difference in altitude, iv) no change in kinetic energy, pipe is straight and")
    print("v) no local friction coefficients.")
    print("\nIn summary: pressure drop depends only on:")
    print("-Water density")
    print("-Distance traveled (length of the pipe)")
    print("-Pipe diameter")
    print("-Darcy friction factor (64/Re)\n\n")
    reynolds_number = (v_water * diameter_pipe * density_water)/viscosity_water
    print("Reynolds number:", reynolds_number)
    print("Flow highly turbulent, friction factor from the Moody chart.")
    print("Pipe material, smooth --> friction factor approximately 0.012")
    print("Total losses: density_water*(0.012*(length_pipe / diameter_pipe))*((v_water^2)/2")
    partA = length_pipe / diameter_pipe
    partB = v_water*v_water
    total = density_water*(partB/2)*(0.012*partA)
    print("=", total)



main()