SUPER_NUMS = ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹']
SUB_NUMS = ['₀', '₁', '₂', '₃', '₄', '₅', '₆', '₇', '₈', '₉']


def gcd(a, b):
    """
    Returns the Greatest Common Divisor between `a` and `b`.
    """
    while b:
        a, b = b, a % b
    return a


def get_super(integer):
    return ''.join([SUPER_NUMS[int(digit)] for digit in str(int(abs(integer)))])


def get_sub(integer):
    return ''.join([SUB_NUMS[int(digit)] for digit in str(int(abs(integer)))])


class Rational:
    """
    Represents any rational number in fraction form.
    """

    def __init__(self, numerator, denominator=1):
        """
        Initialises a rational number with the given numerator and denominator.
        """
        # Only the numerator should ever be negative.
        is_negative = numerator / denominator < 0
        self.numerator = int(abs(numerator)) * (-1 if is_negative else 1)
        self.denominator = int(abs(denominator))

    def simplest_form(self):
        simplified = Rational(self.numerator, self.denominator)
        greatest_common_divisor = gcd(self.numerator, self.denominator)
        while greatest_common_divisor > 1:
            simplified = Rational(
                simplified.numerator / greatest_common_divisor,
                simplified.denominator / greatest_common_divisor
            )
            greatest_common_divisor = gcd(
                simplified.numerator,
                simplified.denominator
            )
        return simplified

    def __eq__(self, other):
        """
        Returns True if the two given Rational numbers are equal.
        """
        return self.simplest_form().numerator == \
            other.simplest_form().numerator and \
            self.simplest_form().denominator == \
            other.simplest_form().denominator

    def __str__(self):
        """
        Returns a string representing this Rational number.
        """
        integer_component = int(abs(self.numerator) / self.denominator)
        simplified_remainder = Rational(
                abs(self.numerator) % self.denominator,
                self.denominator
        ).simplest_form()
        return (
            ('-' if self.numerator < 0 else '')
            + (
                str(integer_component) if integer_component
                or not self.numerator else ''
            )
            + (
                get_super(simplified_remainder.numerator)
                + '/'
                + get_sub(simplified_remainder.denominator)
                if simplified_remainder.numerator else ''
            )
        )

    def __add__(self, other):
        """
        Returns the addition (+) of two Rational numbers.
        Doesn't both with finding the lowest common denominator, just gets a
        common denominator.
        """
        return Rational(
            (
                self.numerator * other.denominator
                + other.numerator * self.denominator
            ),
            self.denominator * other.denominator
        )

    def __mul__(self, other):
        """
        Returns the multiplication (*) of two Rational numbers.
        """
        return Rational(
            self.numerator * other.numerator,
            self.denominator * other.denominator
        )

    def __sub__(self, other):
        """
        Returns self minus (-) other of two Rational numbers.
        """
        return self + (other * -1)

    def __truediv__(self, other):
        """
        Returns self divided by (/) other.
        """
        return self * Rational(other.denominator, other.numerator)


def test_rational():
    """
    This function will never be called during marking.
    """
    assert str(Rational(32, 11)) == '2' + SUPER_NUMS[1] + SUPER_NUMS[0] + '/' \
        + SUB_NUMS[1] + SUB_NUMS[1]
    assert str(Rational(0)) == '0'
    assert str(Rational(6, -5)) == '-1' + SUPER_NUMS[1] + '/' + SUB_NUMS[5]
    assert str(Rational(-1, 3)) == '-' + SUPER_NUMS[1] + '/' + SUB_NUMS[3]
    assert Rational(8, 2) == Rational(4)
    assert Rational(6, 9) * Rational(5, 7) == Rational(10, 21)
    assert Rational(21, 2) / Rational(16, 3) == Rational(63, 32)
    assert Rational(3, 7) + Rational(4, 7) == Rational(1)
    assert Rational(16, 9) - Rational(42) == Rational(-362, 9)
    assert str(Rational(58, 56).simplest_form()) == '1' + SUPER_NUMS[1] + '/' \
        + SUB_NUMS[2] + SUB_NUMS[8]
