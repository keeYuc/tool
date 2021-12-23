import subprocess as sbp
import getopt
import sys


class PortForward():
    def __init__(self):
        self.namespace = 'gcp'
        self.container = 'crawler'
        self.shell_default = 'sh'
        self.get_params()

    def run(self):
        self.__run_exec()

    def __find_container(self):
        proc = sbp.run(
            args=['kubectl get pods -n {}|grep {} | grep -v grep'.format(self.namespace, self.container)], shell=True, universal_newlines=True, stdout=sbp.PIPE)
        pods = []
        for i in proc.stdout.splitlines():
            line = i.split()
            if line[0].startswith('{}-stable'.format(self.container)) and line[2] == 'Running':
                print(i)
                pods.append(line[0])
        if len(pods) == 1:
            return pods[0]
        elif len(pods) == 0:
            print(
                'exit no Running pod -n {} -c {}'.format(self.namespace, self.container))
            sys.exit()
        else:
            while True:
                print('check a index for Running pod   0,1.....')
                index = int(input())
                if index < 0 or index > len(pods)-1:
                    print('index out of range please check')
                else:
                    return pods[index]

    def __run_exec(self):
        id = self.__find_container()
        sbp.call('kubectl exec -it {} -n {} -c {} {}'.format(id,
                 self.namespace, self.container, self.shell_default), shell=True)

    def get_params(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'n:c:s:')
        except BaseException() as err:
            print(err)
            sys.exit()
        for opt, arg in opts:
            if opt == '-n':
                self.namespace = arg
            elif opt == '-c':
                self.container = arg
            elif opt == '-s':
                self.shell_default = arg


if __name__ == '__main__':
    PortForward().run()
