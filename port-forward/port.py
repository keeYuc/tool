import subprocess as sbp
import getopt
import sys


class PortForward():
    def __init__(self):
        self.namespace = 'gcp'
        self.container = 'seo'
        self.port_to = 9009
        self.port_default = 9000
        self.get_params()

    def run(self):
        self.__kill_other()
        self.__build_port_forward()

    def __find_container(self):
        proc = sbp.run(
            args=['kubectl get pods -n {}|grep {} | grep -v grep'.format(self.namespace, self.container)], shell=True, universal_newlines=True, stdout=sbp.PIPE)
        for i in proc.stdout.splitlines():
            line = i.split()
            if line[0].startswith('{}-stable'.format(self.container)) and line[2] == 'Running':
                return line[0]

    def __kill_other(self):
        proc = sbp.run(
            args=['ps aux|grep {}:{}|grep -v grep'.format(self.port_to, self.port_default)], shell=True, universal_newlines=True, stdout=sbp.PIPE)
        for i in proc.stdout.splitlines():
            pid = i.split()[1]
            print('old port',i)
            print('wanto kill :', pid)
            sbp.call(['kill {}'.format(pid)], shell=True)

    def __show_new(self):
        proc = sbp.run(
            args=['ps aux|grep {}:{}|grep -v grep'.format(self.port_to, self.port_default)], shell=True, universal_newlines=True, stdout=sbp.PIPE)
        for i in proc.stdout.splitlines():
            print(i)

    def __build_port_forward(self):
        id = self.__find_container()
        if id != None:
            sbp.call(
                args=['nohup kubectl -n {} port-forward --address 0.0.0.0 {}  {}:{} >>log.log 2>&1 &'.format(self.namespace, id, self.port_to, self.port_default)], shell=True)
            self.__show_new()

    def get_params(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'n:c:p:')
        except BaseException() as err:
            print(err)
            sys.exit()
        for opt, arg in opts:
            if opt == '-n':
                self.namespace = arg
            elif opt == '-c':
                self.container = arg
            elif opt == '-p':
                self.port_to = arg


if __name__ == '__main__':
    PortForward().run()
