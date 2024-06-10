from mininet.topo import Topo


# usg: sudo mn --custom 'topology.py' --topo topology,switches ...
class Topology(Topo):

    def __init__(self, switches=2):

        Topo.__init__(self, switches)

        print("[DEBUG] Creando topologia...")
        print("[DEBUG] switches = ", switches)
        if switches <= 1:
            print("[ERROR] Cantidad de switches debe ser mayor o igual a 2!")
            exit(1)

        switch_list = []
        hosts_list = []

        # Creamos los switches
        for i in range(switches):

            print("[DEBUG] i = ", i)
            switch_list.append(self.addSwitch("s" + str(i+1)))

            # Unimos los switches de manera line
            if i > 0:
                self.addLink(switch_list[i - 1], switch_list[i])

        # Creamos los hosts
        hosts_list.append(self.addHost("h1"))
        hosts_list.append(self.addHost("h2"))
        hosts_list.append(self.addHost("h3"))
        hosts_list.append(self.addHost("h4"))

        print("[DEBUG] switch_list = ", switch_list)
        print("[DEBUG] hosts_list = ", hosts_list)

        # Unimos los hosts al primer y ultimo switch
        self.addLink(switch_list[0], hosts_list[0])
        self.addLink(switch_list[0], hosts_list[1])
        self.addLink(switch_list[switches - 1], hosts_list[2])
        self.addLink(switch_list[switches - 1], hosts_list[3])


topos = {'topology': Topology}
