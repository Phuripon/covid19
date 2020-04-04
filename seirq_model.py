def to_beta(R0, durations, N):
    """
    R0: Basic Reproductive Number
    Return beta: per capita rate at which individuals make effective contact
    (Probability that individuals make effective contact that result in transmission per time unit)
    """
    return (R0 / N) / durations


def seiqr_equations(y0,
                    t,
                    beta_I,
                    beta_Q,
                    alpha,
                    epsilon_E,
                    epsilon_I,
                    gamma):
    """
    Modified version of SEIQR eqations (include Q compartment)
    """
    S, E, I, Q, R, CI, CQ = y0
    dS = -beta_I * S * I - beta_Q * S * Q
    dE = beta_I * S * I + beta_Q * S * Q - alpha * E
    dI = (1 - epsilon_E) * alpha * E - epsilon_I * I - gamma * I
    dQ = epsilon_E * alpha * E + epsilon_I * I - gamma * Q
    dR = gamma * (I + Q)
    dCI = alpha * E
    dCQ = epsilon_E * E + epsilon_I * I
    return dS, dE, dI, dQ, dR, dCI, dCQ


N = 1000000
I0 = 1

y0 = [N, 0, I0, 0, 0, 0, 0]

t = 1
dInc = 5.2
dInf = 2.3
epsilon = 0
alpha = 1 / dInc
gamma = 1 / dInf
beta_I = to_beta(N=N, durations=dInf, R0=22)
beta_Q = to_beta(N=N, durations=dInf, R0=22)

dy = seiqr_equations(y0=y0,
                     t=t,
                     beta_I=beta_I,
                     beta_Q=beta_Q,
                     alpha=alpha,
                     epsilon_E=epsilon,
                     epsilon_I=0.5,
                     gamma=gamma)

sum(dy[0:5])