import sys
import requests
from graphviz import Digraph
import re


def get_python_package_dependencies(package_name):
    print(package_name)
    response = requests.get(f'https://pypi.org/pypi/{package_name}/json')

    if response.status_code != 200:
        print(f"Ошибка: Невозможно получить информацию о пакете '{package_name}'")
        return []

    data = response.json()
    dependencies = data.get('info', {}).get('requires_dist', [])

    return dependencies


def extract_package_name(dependency):
    match = re.match(r"([a-zA-Z0-9_-]+).*", dependency)
    if match:
        return match.group(1).strip()
    return None


def take_in_quotes(string):
    if "-" in string:
        return f"\"{string}\""
    return string


def generate_dependency_graph_python(package_name, graph):
    dependencies = get_python_package_dependencies(package_name)

    print(graph.body)
    if dependencies:
        if len(graph.body) > 40:
            return
        for dependency in dependencies:
            if "extra" in dependency:
                continue
            # print(dependency)
            dependency_name = extract_package_name(dependency)

            if dependency_name:
                # prevent loops
                if f"\t{take_in_quotes(package_name)} -> {take_in_quotes(dependency_name)}\n" in graph.body:
                    print("continued")
                    continue
                graph.edge(package_name, dependency_name)
                generate_dependency_graph_python(dependency_name, graph)


def get_nodejs_package_dependencies(package_name):
    print(package_name)
    response = requests.get(f'https://registry.npmjs.org/{package_name}')

    if response.status_code != 200:
        print(f"Ошибка: Невозможно получить информацию о пакете '{package_name}'")
        return []

    data = response.json()
    version = data.get('dist-tags', {}).get('latest', None)
    dependencies = data.get('versions', {}).get(version, {}).get('dependencies', {})
    return list(dependencies.keys())


def generate_dependency_graph_nodejs(package_name, graph):
    dependencies = get_nodejs_package_dependencies(package_name)

    if dependencies:
        for dependency in dependencies:
            if f"\t{take_in_quotes(package_name)} -> {take_in_quotes(dependency)}\n" in graph.body:
                print("continued")
                continue
            graph.edge(package_name, dependency)
            generate_dependency_graph_nodejs(dependency, graph)


def main():
    if len(sys.argv) != 3:
        print("Использование: python depGraph.py <python|nodejs> <имя_пакета>")
        sys.exit(1)

    package_type = sys.argv[1]
    package_name = sys.argv[2]

    if package_type == 'python':
        graph = Digraph(comment='Dependency Graph (Python)')
        generate_dependency_graph_python(package_name, graph)
    elif package_type == 'nodejs':
        graph = Digraph(comment='Dependency Graph (Node.js)')
        generate_dependency_graph_nodejs(package_name, graph)
    else:
        print("Неподдерживаемый тип пакета. Используйте 'python' или 'nodejs'.")
        sys.exit(1)

    graph.render('deps.dot', view=True)
    print(graph)


if __name__ == "__main__":
    main()