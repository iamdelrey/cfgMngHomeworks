import importlib.util
import sys

def get_module_dependencies(module_name):
    dependencies = set()
    if module_name in sys.modules:
        module = sys.modules[module_name]
    else:
        module_spec = importlib.util.find_spec(module_name)
        if module_spec is None:
            return dependencies
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)

    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type(sys)):
            dependencies.add(obj.__name__)

    return dependencies

def generate_dependency_graph(package_name):
    graph = ['digraph dependencies {']
    visited = set()

    def traverse_dependencies(package):
        if package in visited:
            return
        visited.add(package)

        dependencies = get_module_dependencies(package)
        for dependency in dependencies:
            graph.append(f'  "{package}" -> "{dependency}";')
            traverse_dependencies(dependency)

    traverse_dependencies(package_name)
    graph.append('}')

    return '\n'.join(graph)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python dependency_graph.py <package_name>')
        sys.exit(1)

    package_name = sys.argv[1]
    graph = generate_dependency_graph(package_name)
    print(graph)