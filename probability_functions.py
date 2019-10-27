from math import inf, factorial, exp, sqrt, pi, e

# General functions
def mean(values):
    sum = 0
    for value in values:
        sum += value
    return sum / len(values)


def find_min_and_max(values):
    minimum = inf
    maximum = 0
    for value in values:
        if value < minimum:
            minimum = value
        if value > maximum:
            maximum = value
    return minimum, maximum


def distribution_around_center(values, mu):
    lt_mu = []
    gt_mu = []
    for value in values:
        if value < mu:
            lt_mu.append(value)
        elif value > mu:
            gt_mu.append(value)
    return lt_mu, gt_mu



# Probability functions
def binomial_coefficient(k, n):
    return ( factorial(n) / (factorial(k)*factorial(n-k)) )


def p_binomial(k, n, p):
    return ( binomial_coefficient(k, n)*(p**k)*( (1-p)**(n-k) ) )

# Calculates probability "more than k from n"
def p_cumulative_binomial(k, n, p):
    gt_k = k
    k = n
    p_gt_k = 0
    while k > gt_k:
        p_k = p_binomial(k, n, p)
        print("For "+ str(k) +", probability is:" + str(p_k))
        p_gt_k += p_k
        k -= 1
    return p_gt_k


def p_poisson(mean, k):
    return ( (mean**k)*exp(-mean) ) / factorial(k)

def fx_gaussian_psd(x, mu, sigma):
    return ( 1 / (sqrt(2 * pi * sigma**2))) * (e ** -(((x - mu)**2) / (2 * sigma**2)))


# Statistical functions
def variance(values, sample=False):
    n = len(values)
    if sample:
        n -= 1
    mu = mean(values)
    numerator = 0
    for i in range(0, n):
        numerator += (values[i]-mu)**2
    var = numerator / n
    return var


def standard_deviation(values, sample=False):
    var_values = variance(values, sample)
    return sqrt(var_values)


def covariance(x, y, sample=False):
    if len(x) != len(y):
        print("Given sets X and Y are of different sizes")
        return
    else:
        n = len(x)
        if sample:
            n -= 1
    mu_x = mean(x)
    mu_y = mean(y)
    numerator = 0
    for i in range(0, n):
        numerator += (x[i]-mu_x) * (y[i]-mu_y)
    cov = numerator / n
    return cov

def pearson_correlation_coefficient(x_values, y_values):
    pass

def regression_coefficients(x, y):
    if len(x) != len(y):
        print("Given sets X and Y are of different sizes")
        return
    else:
        n = len(x)
    mu_x = mean(x)
    mu_y = mean(y)
    numerator = 0
    for i in range(0, n):
        numerator += (x[i]-mu_x) * (y[i]-mu_y)
    denominator = 0
    for i in range(0, n):
        denominator += (x[i]-mu_x)**2
    b1 = numerator / denominator
    b0 = mu_y - b1*mu_x
    return [b0, b1]
