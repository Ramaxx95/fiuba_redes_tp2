from mininet.topo import Topo


class Topology(Topo):

    def build(self, switches=2):

        print("[DEBUG] Creando topologia...")
        print("[DEBUG] switches = ", switches)
        if switches <= 1:
            print("[ERROR] Cantidad de switches debe ser mayor o igual a 2!")
            exit(1)

        switch_list = []
        hosts_list = []

        # Creamos los switches y los hosts
        for i in range(switches):

            print("[DEBUG] i = ", i)
            switch_list.append(self.addSwitch("s" + str(i+1)))

            if i == 0:
                hosts_list.append(self.addHost("h" + str(1)))
                hosts_list.append(self.addHost("h" + str(2)))

            else:
                hosts_list.append(self.addHost("h" + str(2**i + 1)))
                hosts_list.append(self.addHost("h" + str(2**i + 2)))

            print("[DEBUG] switch_list = ", switch_list)
            print("[DEBUG] hosts_list = ", hosts_list)
            # Unimos los hosts al nuevo switch
            self.addLink(switch_list[i], hosts_list[2*i])
            self.addLink(switch_list[i], hosts_list[2*i+1])

        # Unimos los switches
        for s in range(switches):

            if s > 0:
                self.addLink(switch_list[s-1], switch_list[s])


topos = {'topology': (lambda: Topology())}
