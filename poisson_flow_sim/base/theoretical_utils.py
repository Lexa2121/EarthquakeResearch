from math import factorial


class MultiServerSystem:
    def __init__(self, n_servers, incoming_flow,
                 av_serving_time, queue_type='endless'):
        self.n_servers = n_servers
        self.incoming_flow = incoming_flow
        self.av_serving_time = av_serving_time
        self.queue_type = queue_type
        self.rho = self.incoming_flow*self.av_serving_time

        denom = sum([self.rho ** n / factorial(n) for n in range(1, self.n_servers + 1)])
        denom += self.rho ** (self.n_servers + 1) / (factorial(self.n_servers) * (self.n_servers - self.rho)) + 1
        self.p_0 = 1 / denom

    def get_state_proba(self, num_queries_in_system):
        if num_queries_in_system <= self.n_servers:
            return self.p_0*(self.rho**num_queries_in_system)/factorial(num_queries_in_system)
        else:
            queue_size = num_queries_in_system - self.n_servers
            return self.get_state_proba(self.n_servers)*(self.rho/self.n_servers)**queue_size

    @property
    def average_queue_size(self):
        l_q = (self.p_0*self.rho**(self.n_servers+1))/(self.n_servers*factorial(self.n_servers))*(1-self.rho/self.n_servers)**(-2)
        return l_q

    @property
    def average_queue_time(self):
        t_q = self.average_queue_size/self.incoming_flow
        return t_q



