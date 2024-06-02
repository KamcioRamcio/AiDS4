import graph
import argparse
from timeit import default_timer as timer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--hamilton', action='store_true')
    parser.add_argument('--non-hamilton', action='store_true')
    args = parser.parse_args()

    g = None

    if args.hamilton:
        nodes = get_nodes()
        saturation = get_saturation_hamilton()
        g = graph.Graph(nodes, saturation, "hamilton")
    elif args.non_hamilton:
        nodes = get_nodes()
        saturation = 50
        g = graph.Graph(nodes, saturation, "non_hamilton")

    while True:
        
        command = get_command()
        if command == 'exit':
            break
        elif command == 'hamilton':
            nodes = get_nodes()
            saturation = get_saturation_hamilton()
            g = graph.Graph(nodes, saturation, "hamilton")
        elif command == 'non_hamilton':
            nodes = get_nodes()
            saturation = 50
            g = graph.Graph(nodes, saturation, "non_hamilton")
        elif command == 'euler':
            if g:
                status= g.is_eulerian()
                print(status)
                
            else:
                print("No graph generated yet.")
                
        elif command == 'cycle':
            if g:
                cycle = g.hamiltonian_cycle()
                if cycle:
                    for i in range(len(cycle)):
                        cycle[i] += 1
                    print("Hamiltonian cycle:", cycle)
                else:
                    print("No Hamiltonian cycle found.")
            else:
                print("No graph generated yet.")
        elif command == 'help':
            print_help()
        elif command == 'print':
            if g:
                g.print_graph()
            else:
                print("No graph generated yet.")
        elif command == 'draw':
            if g:
                g.draw("draw.tex")
            else:
                print("No graph generated yet.")
        else:
            print('Invalid command. Type "help" for a list of commands.')


def print_help():
    print('--- Help ---')
    print('hamilton - generate a hamilton graph')
    print('non_hamilton - generate a non-hamilton graph')
    print('print - print the graph')
    print('draw - draw the graph in LaTeX')
    print('euler - check if the graph is Eulerian')
    print('cycle - find a Hamiltonian cycle')
    print('exit - exit the program')


def get_command():
    return input('command> ').lower()


def get_nodes():
    while True:
        nodes_input = input('nodes> ')
        if nodes_input.isdigit():
            nodes = int(nodes_input)
            if nodes < 1:
                print("Invalid input. Please enter a positive integer.")
            else:
                return nodes
        else:
            print("Invalid input. Please enter a positive integer.")


def get_saturation_hamilton():
    while True:
        print("Please enter the saturation level of the graph (30 or 70).")
        try:
            saturation = int(input('saturation> '))
            if saturation == 30 or saturation == 70:
                return saturation
            else:
                print("Invalid input. Please enter 30 or 70.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


if __name__ == "__main__":
    main()