import json
import sys
from os import path
from collections import defaultdict, deque

class Constants:
    Name = 'name'
    Prerequisites = 'prerequisites'

class ClassScheduler:
    def __init__(self, file_path):
        self.file = open(file_path)

    def build_adjacency(self) -> tuple:
        '''
        Builds adjacency list and counts indegrees for each vertex
        :return: tuple
        '''
        children = defaultdict(list)
        in_degree = defaultdict(int)
        classes = json.load(self.file)
        for course in classes:
            if Constants.Name not in course or Constants.Prerequisites not in course:
                print("Error: Missing class attribute", file=sys.stderr)
                sys.exit(1)
            name = course[Constants.Name]
            prerequisites = course[Constants.Prerequisites]
            # Count node indegree
            for prerequisite in prerequisites:
                children[prerequisite].append(name)
                in_degree[name] += 1
        return children, in_degree

    def find_base_courses(self, children : dict, in_degree : dict) -> deque:
        '''
        Finds all nodes with indegree 0 given an adjacency list and indegree count, and returns the resulting deque
        :param children: dict
        :param in_degree: dict
        :return: deque
        '''
        # If class has a node indegree of 0, it is a base/basic class
        q = deque()
        for course in children:
            if course not in in_degree:
                q.append(course)
        return q

    def find_ordering(self, children : dict, in_degree : dict) -> list:
        '''
        Performs BFS, resulting in a valid configuration/topological ordering in the returned list
        :param children:dict
        :param in_degree:dict
        :return: list
        '''
        q = self.find_base_courses(children, in_degree)
        course_sequence = []
        # topological ordering via BFS - O(V+E)
        while q:
            cur = q.popleft()
            course_sequence.append(cur)
            for child in children[cur]:
                # Decrement indegree count of every child
                in_degree[child] -= 1
                # Class is now available to be taken (added to frontier)
                if in_degree[child] == 0:
                    q.append(child)
        return course_sequence

    def print_ordering(self, courses : list) -> None:
        '''
        Prints a valid configuration/order of classes
        :param courses: list
        :return: void
        '''
        for course in courses:
            print(course)

    def schedule(self) -> None:
        '''
        Creates an adjacency list and indegree count, then finds and prints a valid course sequence.
        :return: void
        '''
        # Build Adjacency/Prerequisite List
        children, in_degree = self.build_adjacency()
        # Find Ordering
        course_sequence = self.find_ordering(children, in_degree)
        # Print Ordering
        self.print_ordering(course_sequence)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: Requires minimum 1 file as argument", file=sys.stderr)
        sys.exit(1)
    if not path.exists(sys.argv[1]):
        print("Error: File does not exist", file=sys.stderr)
        sys.exit(1)
    if not sys.argv[1].lower().endswith('.json'):
        print("Error: Only .json files can be scheduled", file=sys.stderr)
        sys.exit(1)
    print("Sequence for", sys.argv[1], ":")
    scheduler = ClassScheduler(sys.argv[1])
    scheduler.schedule()
