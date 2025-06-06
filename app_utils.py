""" 상세코드 부분 ***
***
본 python code는 장호원 씨가 제출한 코드를 기반으로 하였습니다.
다만 코드 구현상의 문제(특히 자료형의 차이로 인한 비효율성)로 상당부분 수정이 가해졌음을 밝힙니다.
크게 수정이 가해진 부분은 다음과 같습니다:
1. 먼저, 주어진 자료가 트리가 아닌 방향 그래프에 가까우므로 이에 맞춰 root 변수는 제거하였습니다.
2. 원래 문제와는 달리 "어려운 정도의 합" 등은 구할 필요가 없으므로 관련 코드를 제거하여 간결화하였습니다.
"""

import heapq
from collections import deque


class CurriculumManagement:
    """ 과목 목록(subjects)과 선이수 관계(relations)를 바탕으로 최적의 커리큘럼 도출 """

    def __init__(self, subjects, relations):
        self.subjects = subjects
        self.relations = relations.values.tolist()

        self.parents = {subject_id: [] for subject_id in subjects.index}
        self.children = {subject_id: [] for subject_id in subjects.index}

        for pre, post in self.relations:
            self.parents[post].append(pre)
            self.children[pre].append(post)

    def is_acyclic(self):
        """ 사이클이 존재하는지 판단. 있으면 True """

        # 만약 특정 marker일 때 marker가 같은 칸에 도착했다면, 그건 사이클이 존재한다는 것이다.

        visited = {subject_id: 0 for subject_id in self.subjects.index}
        marker = 1

        for subject_id in self.subjects.index:

            if visited[subject_id]:
                continue

            queue = deque([subject_id])

            while queue:

                now = queue.popleft()
                if visited[now] == marker:
                    return True
                if visited[now]:
                    continue

                visited[now] = marker

                queue.extend(self.children[now])

            marker += 1

        return False

    def easier_order(self):
        """ 쉬운 과목을 최대한 먼저 배치하는 최적의 커리큘럼을 제안 """

        # visited:
        visited = {subject_id: False for subject_id in self.subjects.index}

        min_heap = []
        for subject_id in self.subjects.index:
            if not self.parents[subject_id]:
                visited[subject_id] = True
                heapq.heappush(min_heap, (self.subjects.loc[subject_id, "difficulty"], subject_id))

        # order: 주어진 문제의 정답
        order = [None] * len(self.subjects.index)
        i = 0

        while min_heap:
            print(min_heap)
            _, subject_id = heapq.heappop(min_heap)
            order[i] = subject_id
            i += 1

            for next_id in self.children[subject_id]:

                if visited[next_id]:
                    continue

                can_learn_next = True
                for condition in self.parents[next_id]:
                    if not visited[condition]:
                        can_learn_next = False
                        break
                if can_learn_next:
                    visited[next_id] = True
                    heapq.heappush(min_heap, (self.subjects.loc[next_id, "difficulty"], next_id))

        return order
