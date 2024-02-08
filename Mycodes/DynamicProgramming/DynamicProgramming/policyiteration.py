import numpy as np
from environment import GraphicDisplay, Env


class PolicyIteration:
    def __init__(self, env):
        # ȯ�濡 ���� ��ü ����
        self.env = env
        # ��ġ�Լ��� 2���� ����Ʈ�� �ʱ�ȭ
        self.value_table = [[0.0] * env.width for _ in range(env.height)]
        # �� �� �� �� ������ Ȯ���� ��å �ʱ�ȭ
        self.policy_table = [[[0.25, 0.25, 0.25, 0.25]] * env.width
                            for _ in range(env.height)]
        # ��ħ ������ ����
        self.policy_table[2][2] = []
        # ������
        self.discount_factor = 0.9

    # ���� ��� �������� ���� ���� ��ġ�Լ��� ����ϴ� ��å ��
    def policy_evaluation(self):
        # ���� ��ġ�Լ� �ʱ�ȭ
        next_value_table = [[0.00] * self.env.width
                           for _ in range(self.env.height)]

        # ��� ���¿� ���ؼ� ���� ���������� ���
        for state in self.env.get_all_states():
            value = 0.0
            # ��ħ ������ ��ġ �Լ� = 0
            if state == [2, 2]:
                next_value_table[state[0]][state[1]] = value
                continue

            # ���� ��� ������
            for action in self.env.possible_actions:
                next_state = self.env.state_after_action(state, action)
                reward = self.env.get_reward(state, action)
                next_value = self.get_value(next_state)
                value += (self.get_policy(state)[action] *
                          (reward + self.discount_factor * next_value))

            next_value_table[state[0]][state[1]] = value

        self.value_table = next_value_table

    # ���� ��ġ �Լ��� ���ؼ� Ž�� ��å ����
    def policy_improvement(self):
        next_policy = self.policy_table
        for state in self.env.get_all_states():
            if state == [2, 2]:
                continue
            
            value_list = []
            # ��ȯ�� ��å �ʱ�ȭ
            result = [0.0, 0.0, 0.0, 0.0]

            # ��� �ൿ�� ���ؼ� [���� + (������ * ���� ���� ��ġ�Լ�)] ���
            for index, action in enumerate(self.env.possible_actions):
                next_state = self.env.state_after_action(state, action)
                reward = self.env.get_reward(state, action)
                next_value = self.get_value(next_state)
                value = reward + self.discount_factor * next_value
                value_list.append(value)

            # ���� ������ �ִ��� �ൿ�鿡 ���� Ž�� ��å ����
            max_idx_list = np.argwhere(value_list == np.amax(value_list))
            max_idx_list = max_idx_list.flatten().tolist()
            prob = 1 / len(max_idx_list)

            for idx in max_idx_list:
                result[idx] = prob

            next_policy[state[0]][state[1]] = result

        self.policy_table = next_policy

    # Ư�� ���¿��� ��å�� ���� �������� �ൿ�� ��ȯ
    def get_action(self, state):
        policy = self.get_policy(state)
        policy = np.array(policy)
        return np.random.choice(4, 1, p=policy)[0]

    # ���¿� ���� ��å ��ȯ
    def get_policy(self, state):
        return self.policy_table[state[0]][state[1]]

    # ��ġ �Լ��� ���� ��ȯ
    def get_value(self, state):
        return self.value_table[state[0]][state[1]]


if __name__ == "__main__":
    env = Env()
    policy_iteration = PolicyIteration(env)
    grid_world = GraphicDisplay(policy_iteration)
    grid_world.mainloop()
