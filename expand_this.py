ADDITION_SYMBOL = '+'
SUBTRACTION_SYMBOL = '-'
MULTIPLICATION_SYMBOL = '*'
EXPONENTIATION_SYMBOL = '^'
OPERATORS = (ADDITION_SYMBOL, SUBTRACTION_SYMBOL, MULTIPLICATION_SYMBOL, \
    EXPONENTIATION_SYMBOL)


class Polynomial:
    def __init__(self, terms, pronumeral):
        # Terms must be a dictionary, with the keys being the integer power to
        # which the value (the coefficient) is raised.
        self.terms = terms
        self.pronumeral = pronumeral

    def __repr__(self):
        # If the polynomial is empty, return zero...
        non_zero = False
        for value in self.terms.values():
            if value:
                non_zero = True
                break
        if not non_zero:
            return '0'

        string_terms = []
        for key in sorted(self.terms.keys(), reverse=True):
            if self.terms[key]:
                string_terms.append(
                    str(self.terms[key]) + self.pronumeral + '^' + str(key)
                )
        full_powers_string = ' + '.join(string_terms).replace('+ -', '- ')
        return ' + '.join(string_terms).replace('+ -', '- ').replace('^1', '')\
            .replace(self.pronumeral + '^0', '')\
            .replace('1' + self.pronumeral, self.pronumeral)

    @property
    def degree(self):
        degree = 0
        for power in self.terms.keys():
            if power > degree:
                degree = power
        return degree

    # All maths methods assume both self and other have the same pronumeral.

    def __add__(self, other):
        new_degree = self.degree if self.degree > other.degree else other.degree
        new_polynomial = Polynomial({}, self.pronumeral)

        for power in range(new_degree + 1):
            if power in self.terms or power in other.terms:
                new_polynomial.terms[power] = self.terms.get(power, 0) + \
                    other.terms.get(power, 0)

        return new_polynomial

    def __sub__(self, other):
        return self + Polynomial({0:-1}, self.pronumeral) * other

    def __mul__(self, other):
        polynomials_to_add = []

        for own_power, own_coefficient in self.terms.items():
            polynomial_to_add = Polynomial({}, self.pronumeral)

            for other_power, other_coefficient in other.terms.items():
                # As own_power is constant through this, this will not write
                # over any of the same things.
                polynomial_to_add.terms[own_power + other_power] = \
                    own_coefficient * other_coefficient

            polynomials_to_add.append(polynomial_to_add)

        new_polynomial = Polynomial({}, self.pronumeral)

        for polynomial in polynomials_to_add:
            new_polynomial += polynomial

        return new_polynomial

    def __pow__(self, other):
        if list(other.terms.keys()) != [0]:
            raise ValueError(
                'can only raise Polynomials to Polynomials with only a '
                'constant term.'
            )

        new_polynomial = Polynomial({0: 1}, self.pronumeral)

        for _ in range(other.terms[0]):
            new_polynomial *= self

        return new_polynomial


reverse_polish_sequence = input('RPN: ').split()
memory = []


for item in reverse_polish_sequence:
    # Perhaps it is an integer...
    try:
        int(item)
    except ValueError:
        pass
    else:
        # Assume x is the pronumeral for now...
        memory.append(Polynomial({0:int(item)}, 'x'))
        continue

    # Or perhaps it is a operator...
    if item in OPERATORS:
        second_term = memory.pop(-1)
        first_term = memory.pop(-1)
        if item == ADDITION_SYMBOL:
            memory.append(first_term + second_term)
        elif item == SUBTRACTION_SYMBOL:
            memory.append(first_term - second_term)
        elif item == MULTIPLICATION_SYMBOL:
            memory.append(first_term * second_term)
        elif item == EXPONENTIATION_SYMBOL:
            memory.append(first_term ** second_term)
        continue

    # Failing all that, it must be a pronumeral.
    memory.append(Polynomial({1:1}, item))
    for polynomial in memory:
        # Update all the pronumerals set previously...
        polynomial.pronumeral = item


print(memory[0])
